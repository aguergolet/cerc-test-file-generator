# AP002 - Informações das Transações das Unidades de Recebíveis

Gerador de arquivos AP002 da CERC para arranjo de pagamentos.

## Descrição

**CERC-AP002** – INFORMAÇÕES DAS TRANSAÇÕES DAS UNIDADES DE RECEBÍVEIS

## Arquivos

- `generate_ap002.py` - Script Python para gerar arquivos AP002
- `generate_ap002.json` - Arquivo de configuração (veja seção abaixo)
- `cnpjs_estabelecimentos.csv` - Lista de CNPJs de estabelecimentos comerciais
- `contas_bancarias.csv` - Lista de contas bancárias

## Arquivo de Configuração (generate_ap002.json)

O arquivo `generate_ap002.json` contém todas as configurações necessárias para gerar os arquivos AP002.

### Estrutura do Arquivo

```json
{
  "cnpj_credenciadora": "36129585000191",
  "cnpj_participante": "24451242000160",
  "arquivo_cnpjs_ec": "cnpjs_estabelecimentos.csv",
  "arquivo_contas": "contas_bancarias.csv",
  "quantidade_registros": 10,
  "dias_futuros_liquidacao": 7,
  "valor_maximo_transacao": 100000.00,
  "arranjos_pagamento": ["VCC", "MCC", "BCC", "ACC"],
  "carteira_padrao": "Carteira1"
}
```

### Descrição dos Campos

#### Informações da Credenciadora e Participante

- **`cnpj_credenciadora`** (string, obrigatório)
  - CNPJ completo da Instituição Credenciadora (14 dígitos)
  - Exemplo: `"36129585000191"`

- **`cnpj_participante`** (string, obrigatório)
  - CNPJ completo do Participante (14 dígitos)
  - Exemplo: `"24451242000160"`

#### Arquivos de Dados

- **`arquivo_cnpjs_ec`** (string, obrigatório)
  - Nome do arquivo CSV contendo a lista de CNPJs de Estabelecimentos Comerciais
  - O script selecionará aleatoriamente CNPJs deste arquivo
  - Exemplo: `"cnpjs_estabelecimentos.csv"`

- **`arquivo_contas`** (string, obrigatório)
  - Nome do arquivo CSV contendo a lista de contas bancárias
  - O script selecionará aleatoriamente contas deste arquivo para gerar informações de pagamento
  - Uma mesma UR pode ter múltiplas informações de pagamento (geradas aleatoriamente)
  - Exemplo: `"contas_bancarias.csv"`

#### Configurações de Geração

- **`quantidade_registros`** (integer, opcional, padrão: 10)
  - Quantidade padrão de registros a gerar no arquivo AP002
  - Pode ser sobrescrita via linha de comando: `python3 generate_ap002.py 50`
  - Exemplo: `10`

- **`dias_futuros_liquidacao`** (integer, obrigatório)
  - Quantidade de dias futuros para calcular a data de liquidação
  - Data de liquidação = Data atual + dias_futuros_liquidacao
  - Exemplo: `7` (liquidação em 7 dias)

- **`valor_maximo_transacao`** (float, obrigatório)
  - Valor máximo da transação (em reais)
  - O script gerará valores aleatórios entre R$ 100,00 e este valor máximo
  - Exemplo: `100000.00` (valores até R$ 100.000,00)

#### Arranjos de Pagamento

- **`arranjos_pagamento`** (array de strings, obrigatório)
  - Lista de códigos de arranjos de pagamento disponíveis
  - O script selecionará aleatoriamente um arranjo desta lista para cada registro
  - Códigos válidos: VCC, MCC, BCC, ACC, ECC, ECD, GCC, HCC, JCC, MCC, MCD, OCD, SCC, SCD, VCC, VCD, VDC, HCD, SIC, BRS, MAC, CUP, CZC, FRC, MXC, SFC, TKC, BNC, CCD, BRC, SPC, CSC, DAC, DCC, AGC, AUC, RCC, AVC, DBC
  - Exemplo: `["VCC", "MCC", "BCC", "ACC"]`

#### Carteira

- **`carteira_padrao`** (string, opcional, padrão: "Carteira1")
  - Identificador da carteira padrão
  - Exemplo: `"Carteira1"`

### Exemplo de Configuração Completa

```json
{
  "cnpj_credenciadora": "36129585000191",
  "cnpj_participante": "24451242000160",
  "arquivo_cnpjs_ec": "cnpjs_estabelecimentos.csv",
  "arquivo_contas": "contas_bancarias.csv",
  "quantidade_registros": 50,
  "dias_futuros_liquidacao": 15,
  "valor_maximo_transacao": 50000.00,
  "arranjos_pagamento": ["VCC", "MCC"],
  "carteira_padrao": "Carteira1"
}
```

### Como Modificar a Configuração

1. Abra o arquivo `generate_ap002.json` em um editor de texto
2. Modifique os valores conforme necessário
3. Salve o arquivo
4. Execute o script: `python3 generate_ap002.py`

**Nota**: O arquivo JSON deve estar válido. Use um validador JSON online se tiver dúvidas sobre a sintaxe.

## Como Usar

```bash
cd ap002
python3 generate_ap002.py [quantidade_registros]
```

**Exemplos:**

```bash
# Gera 10 registros (valor padrão do JSON)
python3 generate_ap002.py

# Gera 50 registros (sobrescreve o valor do JSON)
python3 generate_ap002.py 50

# Gera 100 registros
python3 generate_ap002.py 100
```

## Formato

- **Separador**: Ponto e vírgula (`;`) - Conforme especificação CERC
- **Campo 15**: Lista de informações de pagamento (múltiplas informações por UR)
- **Encoding**: UTF-8
- **Sem cabeçalho**: O arquivo não deve conter linha de cabeçalho

### Campo 15 - Lista de Informações de Pagamento

O **Campo 15** é uma lista que permite múltiplas informações de pagamento para a mesma UR:
- Cada informação de pagamento contém 11 subcampos
- Múltiplas informações são separadas por `|` (pipe)
- Campos dentro de cada informação são separados por `;` (ponto e vírgula)
- Encapsulado em aspas duplas quando há múltiplas informações

**Subcampos do Campo 15 (Informações de Pagamento):**
1. Número documento titular da conta
2. Tipo de conta (CC, CD, PG, PP)
3. COMPE
4. ISPB
5. Agência
6. Número da conta
7. Valor a pagar
8. Beneficiário
9. Data liquidação efetiva
10. Valor liquidação efetiva
11. Motivo de não pagamento

## Status

✅ Implementado e funcionando
