# AP003 - Informação de Pós-contratadas

Gerador de arquivos AP003 da CERC para arranjo de pagamentos.

## Descrição

**CERC-AP003** – INFORMAÇÃO DE PÓS-CONTRATADAS

## Arquivos

- `generate_ap003.py` - Script Python para gerar arquivos AP003
- `generate_ap003.json` - Arquivo de configuração
- `cnpjs_estabelecimentos.csv` - Lista de CNPJs de estabelecimentos comerciais
- `contas_bancarias.csv` - Lista de contas bancárias

## Arquivo de Configuração (generate_ap003.json)

```json
{
  "cnpj_credenciadora": "00000000000001",
  "arquivo_cnpjs_ec": "cnpjs_estabelecimentos.csv",
  "arquivo_contas": "contas_bancarias.csv",
  "quantidade_registros": 10,
  "dias_futuros_liquidacao": 7,
  "valor_maximo_antecipacao": 100000.00,
  "arranjos_pagamento": ["VCC", "MCC", "BCC", "ACC"]
}
```

## Como Usar

```bash
cd ap003
python3 generate_ap003.py [quantidade_registros]
```

## Formato

- **Separador**: Ponto e vírgula (`;`) - Conforme especificação CERC
- **Encoding**: UTF-8
- **Sem cabeçalho**: O arquivo não deve conter linha de cabeçalho

## Status

✅ Implementado e funcionando

