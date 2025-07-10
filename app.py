from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import openpyxl
from openpyxl.styles import Font, Alignment
import os
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos do banco de dados
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Integer, default=0)
    valor_custo = db.Column(db.Float, default=0.0)
    compatibilidade = db.Column(db.Text)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    valor_total = db.Column(db.Float, default=0.0)
    tipo_pagamento = db.Column(db.String(50))
    parcelas = db.Column(db.Integer, default=1)
    cliente = db.Column(db.String(200))
    produtos_vendidos = db.relationship('ItemVenda', backref='venda', lazy=True)

class ItemVenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, default=1)
    valor_unitario = db.Column(db.Float, default=0.0)
    produto = db.relationship('Produto')

# Criar banco de dados
with app.app_context():
    db.create_all() 

# Rotas principais
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estoque')
def estoque():
    produtos = Produto.query.all()
    return render_template('estoque.html', produtos=produtos)

@app.route('/vendas')
def vendas():
    vendas = Venda.query.order_by(Venda.data_venda.desc()).all()
    produtos = Produto.query.all()
    return render_template('vendas_simples.html', vendas=vendas, produtos=produtos)

@app.route('/relatorios')
def relatorios():
    return render_template('relatorios.html')

@app.route('/teste')
def teste():
    return render_template('teste_vendas.html')

@app.route('/vendas-simples')
def vendas_simples():
    return render_template('vendas_simples.html')

# API para produtos
@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    return jsonify([{
        'id': p.id,
        'nome': p.nome,
        'quantidade': p.quantidade,
        'valor_custo': p.valor_custo,
        'compatibilidade': p.compatibilidade
    } for p in produtos])

@app.route('/api/produtos', methods=['POST'])
def adicionar_produto():
    data = request.json
    produto = Produto(
        nome=data['nome'],
        quantidade=data['quantidade'],
        valor_custo=data['valor_custo'],
        compatibilidade=data['compatibilidade']
    )
    db.session.add(produto)
    db.session.commit()
    return jsonify({'success': True, 'id': produto.id})

@app.route('/api/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    produto = Produto.query.get_or_404(id)
    data = request.json
    produto.nome = data['nome']
    produto.quantidade = data['quantidade']
    produto.valor_custo = data['valor_custo']
    produto.compatibilidade = data['compatibilidade']
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'success': True})

# API para vendas
@app.route('/api/vendas', methods=['POST'])
def registrar_venda():
    data = request.json
    
    # Criar venda
    venda = Venda(
        valor_total=data['valor_total'],
        tipo_pagamento=data['tipo_pagamento'],
        parcelas=data.get('parcelas', 1),
        cliente=data.get('cliente', '')
    )
    db.session.add(venda)
    db.session.flush()  # Para obter o ID da venda
    
    # Adicionar itens da venda e atualizar estoque
    for item_data in data['itens']:
        produto = Produto.query.get(item_data['produto_id'])
        if produto and produto.quantidade >= item_data['quantidade']:
            # Criar item da venda
            item_venda = ItemVenda(
                venda_id=venda.id,
                produto_id=produto.id,
                quantidade=item_data['quantidade'],
                valor_unitario=produto.valor_custo
            )
            db.session.add(item_venda)
            
            # Atualizar estoque
            produto.quantidade -= item_data['quantidade']
        else:
            db.session.rollback()
            return jsonify({'success': False, 'error': 'Estoque insuficiente'})
    
    db.session.commit()
    return jsonify({'success': True, 'id': venda.id})

@app.route('/api/vendas')
def get_vendas():
    vendas = Venda.query.order_by(Venda.data_venda.desc()).all()
    return jsonify([{
        'id': v.id,
        'data_venda': v.data_venda.strftime('%d/%m/%Y %H:%M'),
        'valor_total': v.valor_total,
        'tipo_pagamento': v.tipo_pagamento,
        'parcelas': v.parcelas,
        'cliente': v.cliente,
        'produtos': [{
            'nome': iv.produto.nome,
            'quantidade': iv.quantidade,
            'valor_unitario': iv.valor_unitario
        } for iv in v.produtos_vendidos]
    } for v in vendas])

# Relatório Excel
@app.route('/api/relatorio/<data>')
def gerar_relatorio(data):
    try:
        data_relatorio = datetime.strptime(data, '%Y-%m-%d').date()
    except:
        return jsonify({'error': 'Data inválida'})
    
    vendas = Venda.query.filter(
        db.func.date(Venda.data_venda) == data_relatorio
    ).order_by(Venda.data_venda).all()
    
    # Criar planilha Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Relatório {data_relatorio.strftime('%d/%m/%Y')}"
    
    # Cabeçalhos
    headers = ['Horário', 'Valor', 'Produto(s)', 'Tipo de Pagamento', 'Cliente']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')
    
    # Dados
    row = 2
    for venda in vendas:
        # Preparar lista de produtos
        produtos_str = []
        for item in venda.produtos_vendidos:
            produtos_str.append(f"{item.produto.nome} ({item.quantidade})")
        
        # Tipo de pagamento com parcelas se aplicável
        tipo_pagamento = venda.tipo_pagamento
        if venda.tipo_pagamento == 'Parcelamento' and venda.parcelas > 1:
            tipo_pagamento = f"Parcelamento ({venda.parcelas}x)"
        
        ws.cell(row=row, column=1, value=venda.data_venda.strftime('%d/%m/%Y %H:%M'))
        ws.cell(row=row, column=2, value=f"R$ {venda.valor_total:.2f}")
        ws.cell(row=row, column=3, value=", ".join(produtos_str))
        ws.cell(row=row, column=4, value=tipo_pagamento)
        ws.cell(row=row, column=5, value=venda.cliente or '')
        row += 1
    
    # Ajustar largura das colunas
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Salvar em buffer
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name=f"relatorio_vendas_{data_relatorio.strftime('%d_%m_%Y')}.xlsx",
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == '__main__':
    app.run(debug=True) 