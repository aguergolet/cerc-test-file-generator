# AP004 - OPT-IN

Gerador de arquivos AP004 da CERC para arranjo de pagamentos.

## Descrição

**CERC-AP004** – OPT-IN

## Arquivos

- `generate_ap004.py` - Script Python para gerar arquivos AP004
- `generate_ap004.json` - Arquivo de configuração (veja seção abaixo)
- `cnpjs_estabelecimentos.csv` - Lista de CNPJs de estabelecimentos comerciais

## Arquivo de Configuração (generate_ap004.json)

O arquivo `generate_ap004.json` contém todas as configurações necessárias para gerar os arquivos AP004.

### Estrutura do Arquivo

```json
{
  "cnpj_credenciadora": "00000000000001",
  "cnpj_solicitante": "00000000000002",
  "cnpj_financiador": "00000000000003",
  "arquivo_cnpjs_ec": "cnpjs_estabelecimentos.csv",
  "quantidade_registros": 10,
  "dias_futuros_inicio": 0,
  "dias_futuros_fim": 365,
  "arranjos_pagamento": ["VCC", "MCC", "BCC", "ACC"],
  "carteira_padrao": "Carteira1"
}
```

### Descrição dos Campos

- **`cnpj_credenciadora`** (string, obrigatório)
  - CNPJ completo da Instituição Credenciadora (14 dígitos)
  - **Importante**: Usa CNPJs fictícios (não válidos) para testes
  - Exemplo: `"00000000000001"`

- **`cnpj_solicitante`** (string, obrigatório)
  - CNPJ do solicitante (14 dígitos)
  - Exemplo: `"00000000000002"`

- **`cnpj_financiador`** (string, obrigatório)
  - CNPJ do financiador ou não financeira autorizado (14 dígitos)
  - Exemplo: `"00000000000003"`

- **`arquivo_cnpjs_ec`** (string, obrigatório)
  - Nome do arquivo CSV contendo a lista de CNPJs de Estabelecimentos Comerciais
  - Exemplo: `"cnpjs_estabelecimentos.csv"`

- **`quantidade_registros`** (integer, opcional, padrão: 10)
  - Quantidade padrão de registros a gerar no arquivo AP004
  - Pode ser sobrescrita via linha de comando: `python3 generate_ap004.py 50`

- **`dias_futuros_inicio`** (integer, obrigatório)
  - Quantidade de dias futuros para calcular a data de início
  - Exemplo: `0` (início hoje)

- **`dias_futuros_fim`** (integer, obrigatório)
  - Quantidade máxima de dias futuros para calcular a data de fim
  - Exemplo: `365` (fim em até 1 ano)

- **`arranjos_pagamento`** (array de strings, obrigatório)
  - Lista de códigos de arranjos de pagamento disponíveis
  - Exemplo: `["VCC", "MCC", "BCC", "ACC"]`

- **`carteira_padrao`** (string, opcional, padrão: "Carteira1")
  - Identificador da carteira padrão

## Como Usar

```bash
cd ap004
python3 generate_ap004.py [quantidade_registros]
```

## Formato

- **Separador**: Ponto e vírgula (`;`) - Conforme especificação CERC
- **Encoding**: UTF-8
- **Sem cabeçalho**: O arquivo não deve conter linha de cabeçalho

## Status

✅ Implementado e funcionando
