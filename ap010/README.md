# AP010 - Retorno de Informações Conciliada de Agenda

Gerador de arquivos AP010 da CERC para arranjo de pagamentos.

## Descrição

**CERC-AP010** – RETORNO DE INFORMAÇÕES CONCILIADA DE AGENDA

## Arquivos

- `generate_ap010.py` - Script Python para gerar arquivos AP010
- `generate_ap010.json` - Arquivo de configuração
- `cnpjs_estabelecimentos.csv` - Lista de CNPJs de estabelecimentos comerciais

## Arquivo de Configuração (generate_ap010.json)

```json
{
  "cnpj_credenciadora": "00000000000001",
  "arquivo_cnpjs_ec": "cnpjs_estabelecimentos.csv",
  "quantidade_registros": 10,
  "arranjos_pagamento": ["VCC", "MCC", "BCC", "ACC"]
}
```

## Como Usar

```bash
cd ap010
python3 generate_ap010.py [quantidade_registros]
```

## Formato

- **Separador**: Ponto e vírgula (`;`) - Conforme especificação CERC
- **Encoding**: UTF-8
- **Sem cabeçalho**: O arquivo não deve conter linha de cabeçalho

## Status

✅ Implementado e funcionando

