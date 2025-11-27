# AP012 - Retorno de Informações Conciliada de Contratos

Gerador de arquivos AP012 da CERC para arranjo de pagamentos.

## Descrição

**CERC-AP012** – RETORNO DE INFORMAÇÕES CONCILIADA DE CONTRATOS

## Arquivos

- `generate_ap012.py` - Script Python para gerar arquivos AP012
- `generate_ap012.json` - Arquivo de configuração

## Arquivo de Configuração (generate_ap012.json)

```json
{
  "cnpj_participante": "00000000000005",
  "cnpj_detentor": "00000000000006",
  "quantidade_registros": 10,
  "carteira_padrao": "Carteira1"
}
```

## Como Usar

```bash
cd ap012
python3 generate_ap012.py [quantidade_registros]
```

## Formato

- **Separador**: Ponto e vírgula (`;`) - Conforme especificação CERC
- **Encoding**: UTF-8
- **Sem cabeçalho**: O arquivo não deve conter linha de cabeçalho

## Status

✅ Implementado e funcionando

