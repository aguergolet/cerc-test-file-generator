# AP001 - Manutenção Cadastral de Estabelecimento Comercial

Gerador de arquivos AP001 da CERC para arranjo de pagamentos.

## Descrição

**CERC-AP001** – MANUTENÇÃO CADASTRAL DE ESTABELECIMENTO COMERCIAL

## Arquivos

- `generate_ap001.py` - Script Python para gerar arquivos AP001
- `generate_ap001.json` - Arquivo de configuração

## Arquivo de Configuração (generate_ap001.json)

```json
{
  "cnpj_credenciadora": "00000000000001",
  "quantidade_registros": 10
}
```

### Descrição dos Campos

- **`cnpj_credenciadora`** (string, obrigatório)
  - CNPJ completo da Instituição Credenciadora (14 dígitos)
  - **Importante**: Usa CNPJs fictícios (não válidos) para testes
  - Exemplo: `"00000000000001"`

- **`quantidade_registros`** (integer, opcional, padrão: 10)
  - Quantidade padrão de registros a gerar no arquivo AP001
  - Pode ser sobrescrita via linha de comando: `python3 generate_ap001.py 50`

## Como Usar

```bash
cd ap001
python3 generate_ap001.py [quantidade_registros]
```

**Exemplos:**

```bash
# Gera 10 registros (valor padrão do JSON)
python3 generate_ap001.py

# Gera 50 registros (sobrescreve o valor do JSON)
python3 generate_ap001.py 50
```

## Formato

- **Separador**: Ponto e vírgula (`;`) - Conforme especificação CERC
- **Encoding**: UTF-8
- **Sem cabeçalho**: O arquivo não deve conter linha de cabeçalho

## Status

✅ Implementado e funcionando
