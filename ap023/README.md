# AP023 - Retorno de Informação Conciliada de OPT-IN

Gerador de arquivos AP023 da CERC para arranjo de pagamentos.

## Descrição

**CERC-AP023** – RETORNO DE INFORMAÇÃO CONCILIADA DE OPT-IN

## Arquivos

- `generate_ap023.py` - Script Python para gerar arquivos AP023
- `generate_ap023.json` - Arquivo de configuração

## Arquivo de Configuração (generate_ap023.json)

```json
{
  "cnpj_solicitante": "00000000000002",
  "cnpj_financiador": "00000000000003",
  "quantidade_registros": 10,
  "carteira_padrao": "Carteira1"
}
```

## Como Usar

```bash
cd ap023
python3 generate_ap023.py [quantidade_registros]
```

## Formato

- **Separador**: Ponto e vírgula (`;`) - Conforme especificação CERC
- **Encoding**: UTF-8
- **Sem cabeçalho**: O arquivo não deve conter linha de cabeçalho

## Status

✅ Implementado e funcionando

