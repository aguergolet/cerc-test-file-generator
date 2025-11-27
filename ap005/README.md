# AP005 - Envio de Informações de Agendas

Gerador de arquivos AP005 da CERC para arranjo de pagamentos.

## Descrição

**CERC-AP005** – ENVIO DE INFORMAÇÕES DE AGENDAS POR FORÇA DE UM CONTRATO OU OPT-IN

## Arquivos

- `generate_ap005.py` - Script Python para gerar arquivos AP005
- `generate_ap005.json` - Arquivo de configuração (veja seção abaixo)
- `cnpjs_estabelecimentos.csv` - Lista de CNPJs de estabelecimentos comerciais
- `contas_bancarias.csv` - Lista de contas bancárias

## Arquivo de Configuração (generate_ap005.json)

O arquivo `generate_ap005.json` contém todas as configurações necessárias para gerar os arquivos AP005.

### Estrutura do Arquivo

```json
{
  "cnpj_credenciadora": "00000000000001",
  "cnpj_entidade_registradora": "00000000000004",
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

- **`cnpj_credenciadora`** (string, obrigatório)
  - CNPJ completo da Instituição Credenciadora (14 dígitos)
  - **Importante**: Usa CNPJs fictícios (não válidos) para testes
  - Exemplo: `"00000000000001"`

- **`cnpj_entidade_registradora`** (string, obrigatório)
  - CNPJ da entidade registradora (14 dígitos)
  - Exemplo: `"00000000000004"`

- **`arquivo_cnpjs_ec`** (string, obrigatório)
  - Nome do arquivo CSV contendo a lista de CNPJs de Estabelecimentos Comerciais
  - Exemplo: `"cnpjs_estabelecimentos.csv"`

- **`arquivo_contas`** (string, obrigatório)
  - Nome do arquivo CSV contendo a lista de contas bancárias
  - Exemplo: `"contas_bancarias.csv"`

- **`quantidade_registros`** (integer, opcional, padrão: 10)
  - Quantidade padrão de registros a gerar no arquivo AP005
  - Pode ser sobrescrita via linha de comando: `python3 generate_ap005.py 50`

- **`dias_futuros_liquidacao`** (integer, obrigatório)
  - Quantidade de dias futuros para calcular a data de liquidação
  - Exemplo: `7` (liquidação em 7 dias)

- **`valor_maximo_transacao`** (float, obrigatório)
  - Valor máximo da transação (em reais)
  - Exemplo: `100000.00` (valores até R$ 100.000,00)

- **`arranjos_pagamento`** (array de strings, obrigatório)
  - Lista de códigos de arranjos de pagamento disponíveis
  - Exemplo: `["VCC", "MCC", "BCC", "ACC"]`

- **`carteira_padrao`** (string, opcional, padrão: "Carteira1")
  - Identificador da carteira padrão

## Como Usar

```bash
cd ap005
python3 generate_ap005.py [quantidade_registros]
```

## Formato

- **Separador**: Ponto e vírgula (`;`) - Conforme especificação CERC
- **Campo 12**: Lista de informações de pagamento (múltiplas informações por UR)
- **Encoding**: UTF-8
- **Sem cabeçalho**: O arquivo não deve conter linha de cabeçalho

## Status

✅ Implementado e funcionando
