# 📱 Sistema de Gerenciamento de Estoque - Assistência de Celular

Sistema completo e otimizado para gerenciamento de estoque e vendas de assistência de celular, desenvolvido em Python com Flask.

## 🚀 Funcionalidades Principais

### 1. 📦 Gerenciamento de Estoque
- ✅ Cadastro de produtos com nome, quantidade, valor de custo e compatibilidade
- ✅ Edição e exclusão de produtos
- ✅ Busca e filtros em tempo real
- ✅ Controle de baixo estoque (alerta para produtos com 5 ou menos unidades)
- ✅ Interface responsiva e intuitiva

### 2. 💰 Processamento de Vendas
- ✅ Registro de vendas com múltiplos produtos
- ✅ Cálculo automático do valor total
- ✅ Diferentes tipos de pagamento (Espécie, Pix, Cartão, Parcelamento, Complemento)
- ✅ Baixa automática do estoque
- ✅ Histórico completo de vendas em tempo real
- ✅ Interface simplificada e funcional

### 3. 📊 Relatórios
- ✅ Relatório diário de vendas em Excel
- ✅ Estatísticas gerais (total de produtos, vendas, faturamento)
- ✅ Visualização das últimas vendas
- ✅ Exportação profissional

## ⚡ Instalação e Configuração

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar o Sistema
```bash
python app.py
```

### 3. Acessar o Sistema
Abra seu navegador e acesse: `http://localhost:5000`

## 📖 Como Usar

### 🛍️ Cadastrando Produtos
1. Acesse a página "Estoque"
2. Preencha o formulário com:
   - **Nome do produto** (ex: "Tela iPhone 11 Pro")
   - **Quantidade em estoque**
   - **Valor de custo**
   - **Compatibilidade** (ex: "iPhone X, iPhone XS")
3. Clique em "Salvar Produto"

### 💳 Registrando Vendas
1. Acesse a página "Vendas"
2. Preencha:
   - **Nome do cliente** (opcional)
   - **Selecione os produtos** e quantidades
   - **Escolha o tipo de pagamento**
   - **Se for parcelamento**, informe o número de parcelas
3. Clique em "Finalizar Venda"
4. **Histórico atualizado automaticamente**

### 📈 Gerando Relatórios
1. Acesse a página "Relatórios"
2. Selecione a data desejada
3. Clique em "Gerar Relatório Excel"
4. O arquivo será baixado automaticamente

## 🏗️ Estrutura do Projeto

```
Estoque/
├── app.py                    # Aplicação principal Flask
├── requirements.txt          # Dependências Python
├── README.md                # Documentação principal
├── templates/               # Templates HTML
│   ├── base.html            # Template base
│   ├── index.html           # Dashboard principal
│   ├── estoque.html         # Gerenciamento de estoque
│   ├── vendas_simples.html  # Registro de vendas (otimizada)
│   └── relatorios.html      # Geração de relatórios
└── instance/                # Banco de dados SQLite (criado automaticamente)
```

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.x, Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, jQuery
- **Banco de Dados**: SQLite
- **Relatórios**: openpyxl (Excel)
- **APIs**: RESTful para produtos e vendas

## 🎯 Recursos do Sistema

### 📊 Dashboard
- Estatísticas em tempo real
- Produtos com baixo estoque
- Últimas vendas
- Faturamento do dia
- Interface moderna e responsiva

### 📦 Estoque
- Interface intuitiva para cadastro
- Busca e filtros em tempo real
- Edição inline
- Alertas de baixo estoque
- Controle completo de produtos

### 💰 Vendas
- Seleção múltipla de produtos
- Cálculo automático de totais
- Diferentes formas de pagamento
- Histórico completo em tempo real
- Interface simplificada e funcional

### 📈 Relatórios
- Exportação para Excel
- Filtros por data
- Estatísticas detalhadas
- Formatação profissional
- Download automático

## 🔧 APIs Disponíveis

### Produtos
- `GET /api/produtos` - Listar todos os produtos
- `POST /api/produtos` - Cadastrar novo produto
- `PUT /api/produtos/<id>` - Atualizar produto
- `DELETE /api/produtos/<id>` - Excluir produto

### Vendas
- `GET /api/vendas` - Listar todas as vendas
- `POST /api/vendas` - Registrar nova venda

## 📱 Funcionalidades Específicas

### Para Assistência de Celular
- **Compatibilidade de produtos** - Especificar modelos compatíveis
- **Controle de estoque** - Gerenciar peças e acessórios
- **Vendas múltiplas** - Registrar serviços + produtos
- **Relatórios detalhados** - Acompanhar faturamento

## 🚀 Melhorias Recentes

### ✅ Sistema Otimizado
- **Limpeza de arquivos** - Removidos arquivos de teste e diagnóstico
- **Página de vendas otimizada** - Interface simplificada e funcional
- **Histórico em tempo real** - Atualização automática após vendas
- **Performance melhorada** - Sistema mais rápido e responsivo

### ✅ Interface Aprimorada
- **Design responsivo** - Funciona em desktop e mobile
- **Feedback visual** - Alertas e indicadores de status
- **Navegação intuitiva** - Interface clara e organizada
- **Validação de dados** - Prevenção de erros

## 📞 Suporte

Para dúvidas ou suporte técnico, entre em contato através dos canais disponíveis.

---

**Sistema otimizado e pronto para uso em produção!** 🎉

**Desenvolvido para Assistência de Celular** 📱 