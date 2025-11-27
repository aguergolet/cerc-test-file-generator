# AP008 - Envio de Efeitos de Contratos Aplicáveis às Unidades de Recebíveis

Gerador de arquivos AP008 da CERC para arranjo de pagamentos.

## Descrição

**CERC-AP008** – ENVIO DE EFEITOS DE CONTRATOS APLICÁVEIS ÀS UNIDADES DE RECEBÍVEIS PARA FINS DE LIQUIDAÇÃO

## Arquivos

- `generate_ap008.py` - Script Python para gerar arquivos AP008
- `generate_ap008.json` - Arquivo de configuração (veja seção abaixo)
- `cnpjs_estabelecimentos.csv` - Lista de CNPJs de estabelecimentos comerciais
- `contas_bancarias.csv` - Lista de contas bancárias
- `AP008_STRUCTURE.md` - Documentação da estrutura do arquivo

## Arquivo de Configuração (generate_ap008.json)

O arquivo `generate_ap008.json` contém todas as configurações necessárias para gerar os arquivos AP008. Todas as configurações são centralizadas neste arquivo JSON.

### Estrutura do Arquivo

```json
{
  "cnpj_credenciadora": "36129585000191",
  "arquivo_cnpjs_ec": "cnpjs_estabelecimentos.csv",
  "arquivo_contas": "contas_bancarias.csv",
  "quantidade_registros": 10,
  "prioridade_maxima": 5,
  "dias_futuros_liquidacao": 7,
  "valor_maximo_pagamento": 100000.00,
  "arranjos_pagamento": ["VCC", "MCC", "BCC", "ACC"],
  "entidade_registradora": "12345678000190",
  "tipo_conta_padrao": "CC",
  "compe_padrao": "001",
  "ispb_padrao": "12345678"
}
```

### Descrição dos Campos

#### Informações da Credenciadora

- **`cnpj_credenciadora`** (string, obrigatório)
  - CNPJ completo da Instituição Credenciadora (14 dígitos)
  - **Importante**: Como é instrução de pagamento, apenas 1 credenciadora é permitida
  - Exemplo: `"36129585000191"`

#### Arquivos de Dados

- **`arquivo_cnpjs_ec`** (string, obrigatório)
  - Nome do arquivo CSV contendo a lista de CNPJs de Estabelecimentos Comerciais
  - O script selecionará aleatoriamente CNPJs deste arquivo para gerar os registros
  - Exemplo: `"cnpjs_estabelecimentos.csv"`

- **`arquivo_contas`** (string, obrigatório)
  - Nome do arquivo CSV contendo a lista de contas bancárias
  - O script selecionará aleatoriamente contas deste arquivo para gerar os registros
  - Uma mesma UR pode ter múltiplas contas (geradas aleatoriamente)
  - Exemplo: `"contas_bancarias.csv"`

#### Configurações de Geração

- **`quantidade_registros`** (integer, opcional, padrão: 10)
  - Quantidade padrão de registros a gerar no arquivo AP008
  - Pode ser sobrescrita via linha de comando: `python3 generate_ap008.py 50`
  - Exemplo: `10`

- **`prioridade_maxima`** (integer, obrigatório)
  - Valor máximo de prioridade no pagamento (1 a N)
  - O script gerará prioridades aleatórias entre 1 e este valor
  - Exemplo: `5` (gera prioridades de 1 a 5)

- **`dias_futuros_liquidacao`** (integer, obrigatório)
  - Quantidade de dias futuros para calcular a data de liquidação
  - Data de liquidação = Data atual + dias_futuros_liquidacao
  - Exemplo: `7` (liquidação em 7 dias)

- **`valor_maximo_pagamento`** (float, obrigatório)
  - Valor máximo a ser pago na conta corrente (em reais)
  - O script gerará valores aleatórios entre R$ 100,00 e este valor máximo
  - Exemplo: `100000.00` (valores até R$ 100.000,00)

#### Arranjos de Pagamento

- **`arranjos_pagamento`** (array de strings, obrigatório)
  - Lista de códigos de arranjos de pagamento disponíveis
  - O script selecionará aleatoriamente um arranjo desta lista para cada registro
  - Códigos válidos: VCC, MCC, BCC, ACC, ECC, ECD, GCC, HCC, JCC, MCC, MCD, OCD, SCC, SCD, VCC, VCD, VDC, HCD, SIC, BRS, MAC, CUP, CZC, FRC, MXC, SFC, TKC, BNC, CCD, BRC, SPC, CSC, DAC, DCC, AGC, AUC, RCC, AVC, DBC
  - Exemplo: `["VCC", "MCC", "BCC", "ACC"]`

#### Informações da Entidade Registradora

- **`entidade_registradora`** (string, obrigatório)
  - CNPJ da entidade registradora (14 dígitos)
  - Exemplo: `"12345678000190"`

#### Valores Padrão para Contas Bancárias

Estes valores são usados quando não especificados no arquivo `contas_bancarias.csv`:

- **`tipo_conta_padrao`** (string, opcional, padrão: "CC")
  - Tipo de conta padrão
  - Valores permitidos: `CC` (Conta Corrente), `CD` (Conta de Depósito), `CG` (Conta Garantia), `CI` (Conta Investimento), `PG` (Conta de Pagamento), `PP` (Conta Poupança)
  - Exemplo: `"CC"`

- **`compe_padrao`** (string, opcional, padrão: "001")
  - Código COMPE padrão da Instituição de Domicílio (3 dígitos)
  - Exemplo: `"001"`

- **`ispb_padrao`** (string, opcional, padrão: "12345678")
  - Número ISPB padrão da Instituição de Domicílio (8 dígitos)
  - Exemplo: `"12345678"`

### Exemplo de Configuração Completa

```json
{
  "cnpj_credenciadora": "36129585000191",
  "arquivo_cnpjs_ec": "cnpjs_estabelecimentos.csv",
  "arquivo_contas": "contas_bancarias.csv",
  "quantidade_registros": 50,
  "prioridade_maxima": 3,
  "dias_futuros_liquidacao": 15,
  "valor_maximo_pagamento": 50000.00,
  "arranjos_pagamento": ["VCC", "MCC"],
  "entidade_registradora": "12345678000190",
  "tipo_conta_padrao": "CC",
  "compe_padrao": "001",
  "ispb_padrao": "12345678"
}
```

### Como Modificar a Configuração

1. Abra o arquivo `generate_ap008.json` em um editor de texto
2. Modifique os valores conforme necessário
3. Salve o arquivo
4. Execute o script: `python3 generate_ap008.py`

**Nota**: O arquivo JSON deve estar válido. Use um validador JSON online se tiver dúvidas sobre a sintaxe.

## Como Usar

```bash
cd ap008
python3 generate_ap008.py [quantidade_registros]
```

**Exemplos:**

```bash
# Gera 10 registros (valor padrão do JSON)
python3 generate_ap008.py

# Gera 50 registros (sobrescreve o valor do JSON)
python3 generate_ap008.py 50

# Gera 100 registros
python3 generate_ap008.py 100
```

## Formato

- **Separador**: Ponto e vírgula (`;`)
- **Campo 7**: Lista de contas (múltiplas contas por UR)
- **Encoding**: UTF-8

## Status

✅ Implementado e funcionando

