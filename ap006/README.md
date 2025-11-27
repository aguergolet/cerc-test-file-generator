# AP006 - OPT-OUT

Gerador de arquivos AP006 da CERC para arranjo de pagamentos.

## Descrição

**CERC-AP006** – OPT-OUT

## Arquivos

- `generate_ap006.py` - Script Python para gerar arquivos AP006
- `generate_ap006.json` - Arquivo de configuração

## Arquivo de Configuração (generate_ap006.json)

```json
{
  "cnpj_credenciadora": "00000000000001",
  "cnpj_solicitante": "00000000000002",
  "quantidade_registros": 10,
  "carteira_padrao": "Carteira1"
}
```

## Como Usar

```bash
cd ap006
python3 generate_ap006.py [quantidade_registros]
```

## Formato

- **Separador**: Ponto e vírgula (`;`) - Conforme especificação CERC
- **Encoding**: UTF-8
- **Sem cabeçalho**: O arquivo não deve conter linha de cabeçalho

## Status

✅ Implementado e funcionando

