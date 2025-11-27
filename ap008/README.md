# AP008 - Envio de Efeitos de Contratos Aplicáveis às Unidades de Recebíveis

Gerador de arquivos AP008 da CERC para arranjo de pagamentos.

## Descrição

**CERC-AP008** – ENVIO DE EFEITOS DE CONTRATOS APLICÁVEIS ÀS UNIDADES DE RECEBÍVEIS PARA FINS DE LIQUIDAÇÃO

## Arquivos

- `generate_ap008.py` - Script Python para gerar arquivos AP008
- `generate_ap008.json` - Arquivo de configuração
- `cnpjs_estabelecimentos.csv` - Lista de CNPJs de estabelecimentos comerciais
- `contas_bancarias.csv` - Lista de contas bancárias
- `AP008_STRUCTURE.md` - Documentação da estrutura do arquivo

## Como Usar

```bash
cd ap008
python3 generate_ap008.py [quantidade_registros]
```

## Formato

- **Separador**: Ponto e vírgula (`;`)
- **Campo 7**: Lista de contas (múltiplas contas por UR)
- **Encoding**: UTF-8

## Status

✅ Implementado e funcionando

