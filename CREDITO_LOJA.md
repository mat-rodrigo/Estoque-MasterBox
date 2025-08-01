# Sistema de Crédito na Loja - MasterBox

## Visão Geral

Foi implementada uma nova funcionalidade que permite aos atacadistas acumular crédito na loja quando devolvem produtos já pagos. Este sistema oferece flexibilidade para os atacadistas escolherem entre receber o valor em dinheiro ou deixá-lo como crédito para futuras compras.

## Funcionalidades Implementadas

### 1. Devolução com Opção de Crédito

Quando um atacadista devolve produtos de um crediário que já foi pago, ele pode escolher entre:

- **Receber o valor**: O valor é retirado do caixa diário (comportamento atual)
- **Deixar como crédito**: O valor fica disponível como crédito na loja para futuras compras

### 2. Controle de Crédito na Loja

#### 2.1 Modelo de Dados
```python
class CreditoLoja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)  # Pode ser positivo (crédito) ou negativo (uso)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    origem = db.Column(db.String(100), nullable=False)  # 'devolucao_crediario', 'uso_credito', etc.
    crediario_id = db.Column(db.Integer, db.ForeignKey('crediario.id'))  # Opcional
    observacoes = db.Column(db.Text)
```

#### 2.2 APIs Implementadas

**Consultar Crédito do Cliente:**
```javascript
GET /api/credito-loja/cliente/{cliente_id}
```

**Usar Crédito para Pagar Crediário:**
```javascript
POST /api/credito-loja/cliente/{cliente_id}/usar
{
    "valor": 100.00,
    "crediario_id": 123,
    "observacoes": "Pagamento com crédito"
}
```

**Adicionar Crédito Manualmente:**
```javascript
POST /api/credito-loja/cliente/{cliente_id}/adicionar
{
    "valor": 50.00,
    "origem": "pagamento_adicional",
    "observacoes": "Crédito adicional"
}
```

### 3. Interface do Usuário

#### 3.1 Modal de Devolução
- Quando o crediário está pago, aparecem opções para escolher o tipo de devolução
- Opção "Receber o valor" (retira do caixa)
- Opção "Deixar como crédito na loja"

#### 3.2 Seção de Crédito na Loja
- Mostra o saldo atual de crédito
- Exibe histórico de créditos (positivos e negativos)
- Atualiza automaticamente após operações

#### 3.3 Modal de Pagamento
- Quando há crédito disponível, oferece opção de usar crédito
- Opção "Dinheiro/Cartão" (pagamento normal)
- Opção "Usar Crédito na Loja"

### 4. Fluxo de Funcionamento

#### 4.1 Devolução de Produtos Pagos
1. Atacadista seleciona produtos para devolução
2. Sistema verifica se o crediário está pago
3. Se pago, oferece opções de devolução:
   - **Caixa**: Retira valor do caixa diário
   - **Crédito**: Adiciona valor como crédito na loja
4. Produtos são devolvidos ao estoque
5. Crédito é registrado (se escolhido)

#### 4.2 Uso do Crédito
1. Atacadista seleciona crediário para pagar
2. Sistema verifica se há crédito disponível
3. Se há crédito, oferece opção de usar
4. Crédito é descontado e crediário é pago
5. Histórico é atualizado

### 5. Impacto no Caixa Diário

- **Devoluções tipo "caixa"**: Afetam o caixa diário (comportamento atual)
- **Devoluções tipo "crédito"**: NÃO afetam o caixa diário
- **Uso de crédito**: NÃO afeta o caixa diário (já foi "pago" anteriormente)

### 6. Vantagens do Sistema

1. **Flexibilidade**: Atacadistas podem escolher como receber o valor
2. **Fidelização**: Crédito incentiva futuras compras
3. **Controle**: Sistema rastreia origem e uso de cada crédito
4. **Transparência**: Histórico completo de créditos
5. **Facilidade**: Pagamento de crediários com crédito disponível

### 7. Exemplos de Uso

#### Exemplo 1: Devolução com Crédito
- Atacadista paga crediário de R$ 500,00
- Devolve produtos no valor de R$ 100,00
- Escolhe "Deixar como crédito na loja"
- Resultado: R$ 100,00 disponível como crédito

#### Exemplo 2: Uso do Crédito
- Atacadista tem R$ 100,00 de crédito
- Tem crediário pendente de R$ 80,00
- Usa crédito para pagar crediário
- Resultado: Crediário pago, R$ 20,00 de crédito restante

### 8. Considerações Técnicas

- Sistema mantém compatibilidade com funcionalidades existentes
- Devoluções tipo "caixa" continuam funcionando normalmente
- Crédito é sempre vinculado ao cliente específico
- Histórico completo de transações é mantido
- Validações garantem integridade dos dados

## Conclusão

Esta nova funcionalidade oferece maior flexibilidade para os atacadistas, permitindo que eles escolham como receber valores de devoluções e facilitando o pagamento de crediários através do crédito acumulado na loja. 