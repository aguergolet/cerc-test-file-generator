# Geradores de Arquivos CERC

Este projeto contém ferramentas para gerar arquivos da CERC (Centralizadora de Registro de Créditos) para arranjo de pagamentos.

## Estrutura do Projeto

Cada tipo de arquivo AP tem sua própria pasta:

- **ap001/** - Manutenção Cadastral de Estabelecimento Comercial 🚧
- **ap002/** - Informações das Transações das Unidades de Recebíveis 🚧
- **ap004/** - OPT-IN 🚧
- **ap005/** - Envio de Informações de Agendas 🚧
- **ap008/** - Envio de Efeitos de Contratos ✅

## Status

- ✅ **AP002** - Implementado e funcionando
- ✅ **AP008** - Implementado e funcionando
- 🚧 **AP001, AP004, AP005** - Em desenvolvimento

## 🤝 Contribuindo

Este projeto aceita contribuições! Por favor, leia o [Guia de Contribuição](CONTRIBUTING.md) antes de começar.

**Importante**: Este projeto utiliza um modelo de colaboração direta. Contributors trabalham em branches do repositório principal, não é necessário fazer fork.

## Como Usar

Cada pasta contém seu próprio gerador. Consulte o README específico de cada pasta para mais detalhes.

### Exemplos

**AP002:**
```bash
cd ap002
python3 generate_ap002.py [quantidade_registros]
```

**AP008:**
```bash
cd ap008
python3 generate_ap008.py [quantidade_registros]
```

## Estrutura de Arquivos

- `AP008_STRUCTURE.md` - Documentação completa da estrutura do arquivo AP008
- `generate_ap008.py` - Script Python para gerar arquivos AP008
- `generate_ap008.json` - Arquivo de configuração JSON
- `cnpjs_estabelecimentos.csv` - Lista de CNPJs de estabelecimentos comerciais
- `contas_bancarias.csv` - Lista de contas bancárias para pagamento
- `CERC-AP008_example.csv` - Arquivo de exemplo com cabeçalho
- `CERC-AP008_53462828_20240115_0000001.csv` - Arquivo de exemplo com dados

## Campos Principais do AP008

### Informações do Contrato
- **Referência Externa**: Código único de controle do participante
- **Identificador do Contrato**: Código do contrato na entidade registradora
- **Entidade Registradora**: CNPJ da entidade registradora
- **Instituição Credenciadora/Subcredenciadora**: CNPJ da credenciadora
- **Usuário Final Recebedor**: CNPJ/CPF do usuário final recebedor
- **Arranjo de Pagamento**: Código do arranjo (ex: VCC, MCC, etc.)

### Informações do Efeito de Contrato
- **Identificador Efeito Contrato**: Protocolo do efeito de contrato (Campo 7.1)
- **Data de Liquidação**: Data prevista de liquidação (formato: AAAA-MM-DD)
- **Titular da UR**: CNPJ/CPF do titular da unidade de recebível
- **Constituição da UR**: 1 = Constituída, 2 = A constituir
- **Valor Constituído Total**: Valor total constituído
- **Valor Bloqueado**: Valor bloqueado para pagamento
- **Indicador de Oneração**: Prioridade do ônus (0 = Insucesso, 1 a N = Prioridade)
- **Regra de Divisão**: 1 = Valor definido, 2 = Percentual
- **Valor Onerado**: Valor ou percentual onerado

### Informações de Processamento
- **Protocolo**: Protocolo do processamento
- **Data Hora do Evento**: Data/hora no formato RFC3339
- **Status da Operação**: 0 = Sucesso, 1 = Falha
- **Código do Erro**: Código do erro (se status = 1)
- **Descrição do Erro**: Descrição do erro (se status = 1)

### Informações Bancárias
- **Número Documento Titular da Conta**: CPF/CNPJ do titular
- **Tipo de Conta**: CC, CD, CG, CI, PG, PP
- **COMPE**: Código COMPE (3 dígitos)
- **ISPB**: Número ISPB (8 dígitos)
- **Agência**: Número da agência (sem dígito verificador)
- **Número da Conta**: 
  - CC/CD/CG/CI/PP: Com hífen (ex: 123456-7)
  - PG: Sem hífen (ex: 1234567)
- **Nome Titular da Conta**: Nome do titular

## Configuração

O script utiliza um arquivo JSON de configuração (`generate_ap008.json`) com os seguintes parâmetros:

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

### Parâmetros de Configuração

- **cnpj_credenciadora**: CNPJ da credenciadora (14 dígitos) - apenas 1, pois é instrução de pagamento
- **arquivo_cnpjs_ec**: Nome do arquivo CSV com lista de CNPJs de estabelecimentos comerciais
- **arquivo_contas**: Nome do arquivo CSV com lista de contas bancárias
- **quantidade_registros**: Quantidade padrão de registros a gerar (pode ser sobrescrita via linha de comando)
- **prioridade_maxima**: Valor máximo de prioridade no pagamento (1 a N)
- **dias_futuros_liquidacao**: Quantidade de dias futuros para calcular a data de liquidação
- **valor_maximo_pagamento**: Valor máximo a ser pago na conta corrente
- **arranjos_pagamento**: Lista de códigos de arranjos de pagamento disponíveis
- **entidade_registradora**: CNPJ da entidade registradora
- **tipo_conta_padrao**: Tipo de conta padrão (CC, CD, CG, CI, PG, PP)
- **compe_padrao**: Código COMPE padrão
- **ispb_padrao**: Código ISPB padrão

### Arquivo de CNPJs de Estabelecimentos

O arquivo `cnpjs_estabelecimentos.csv` deve conter uma coluna `cnpj`:

```csv
cnpj
12345678901234
98765432109876
11122233344455
```

### Arquivo de Contas Bancárias

O arquivo `contas_bancarias.csv` deve conter as seguintes colunas:

```csv
numero_documento_titular,tipo_conta,compe,ispb,agencia,numero_conta,nome_titular
12345678901,CC,001,12345678,1234,123456-7,João da Silva
98765432109,CC,001,12345678,1234,987654-3,Maria Santos
```

## Como Usar o Script Python

### Requisitos
- Python 3.6 ou superior

### Executar o Script

O script gera registros aleatórios baseados na configuração:

```bash
# Gera a quantidade configurada no JSON (padrão: 10)
python3 generate_ap008.py

# Sobrescreve a quantidade do JSON e gera 50 registros
python3 generate_ap008.py 50

# Sobrescreve a quantidade do JSON e gera 100 registros
python3 generate_ap008.py 100
```

**Nota**: A quantidade de registros segue esta ordem de prioridade:
1. Valor passado na linha de comando (se fornecido)
2. Valor do campo `quantidade_registros` no JSON
3. Padrão de 10 registros (se não configurado)

### Funcionalidades

O script automaticamente:
- Seleciona CNPJs de EC aleatoriamente do arquivo CSV
- Seleciona contas bancárias aleatoriamente do arquivo CSV
- Calcula a data de liquidação como: data atual + dias_futuros_liquidacao
- Gera valores aleatórios até o valor_maximo_pagamento
- Gera prioridades aleatórias de 1 até prioridade_maxima
- Seleciona arranjos de pagamento aleatoriamente da lista configurada

### Exemplo de Uso Programático

```python
from generate_ap008 import AP008Generator

# Inicializa o gerador com configuração
generator = AP008Generator("generate_ap008.json")

# Gera arquivo com 20 registros
output_file = generator.generate_file(20)
print(f"Arquivo gerado: {output_file}")
```

## Nomenclatura do Arquivo

O arquivo segue o padrão:
```
CERC-AP008_CNPJ_RAIZ_YYYYMMDD_NNNNNNN.csv
```

Exemplo:
```
CERC-AP008_53462828_20240115_0000001.csv
```

Onde:
- `CERC-AP008`: Tipo de leiaute (fixo)
- `53462828`: Raiz do CNPJ (8 dígitos)
- `20240115`: Data no formato YYYYMMDD
- `0000001`: Sequencial (7 dígitos)

## Formato do Arquivo

- **Extensão**: `.csv`
- **Separador**: Ponto e vírgula (`;`) - **IMPORTANTE**: Conforme especificação CERC
- **Encoding**: UTF-8
- **Sem cabeçalho**: O arquivo não deve conter linha de cabeçalho
- **Formato de Data**: `AAAA-MM-DD`
- **Formato de Data/Hora**: RFC3339 (ex: `2024-01-15T10:30:00Z`)

### Campo 7 - Lista de Contas

O **Campo 7** é uma lista que permite múltiplas contas de pagamento para a mesma UR:
- Campos 7.1 a 7.15: Informações do efeito (não se repetem)
- Campos 7.16 a 7.22: Informações bancárias (podem se repetir)

**Formato quando há múltiplas contas:**
```
"campo7.1;campo7.2;...;campo7.15;conta1|conta2|conta3"
```
- Contas separadas por `|` (pipe)
- Campos separados por `;` (ponto e vírgula)
- Encapsulado em aspas duplas quando há múltiplas contas

## Valores Permitidos

### Tipo de Efeito (Campo 7.4)
- `1` = Troca de titularidade
- `2` = Ônus - Cessão fiduciária
- `3` = Ônus - Outros
- `4` = Bloqueio judicial
- `8` = Promessa de Cessão

### Constituição da UR
- `1` = Constituída
- `2` = A constituir

### Regra de Divisão
- `1` = Comprometimento de valor definido
- `2` = Comprometimento de percentual do valor que vier a ser constituído

### Tipo de Conta
- `CC` = Conta Corrente
- `CD` = Conta de Depósito
- `CG` = Conta Garantia
- `CI` = Conta Investimento
- `PG` = Conta de Pagamento
- `PP` = Conta Poupança

### Status da Operação
- `0` = Sucesso
- `1` = Falha

## Diretório de Saída

Conforme a estrutura da CERC, o arquivo deve ser disponibilizado em:
```
\efeitos_contrato\saida
```

## Observações Importantes

1. Todos os CNPJs devem ter 14 dígitos (completar com zeros à esquerda)
2. Todos os CPFs devem ter 11 dígitos (completar com zeros à esquerda)
3. COMPE deve ter 3 dígitos (completar com zeros à esquerda)
4. ISPB deve ter 8 dígitos (completar com zeros à esquerda)
5. Valores decimais devem ter 2 casas decimais
6. Número de conta para CC/CD/CG/CI/PP deve ter hífen
7. Número de conta para PG não deve ter hífen

## Referências

- [Documentação CERC - Financiador](https://cerc-2.gitbook.io/ola-financiador-ap/)
- [Documentação CERC - Credenciador](https://cerc-2.gitbook.io/ola-credenciador-ap/)
- Manual de Interfaces da CERC

## Suporte

Para dúvidas ou suporte, consulte:
- Email: suporte-operacoes@cerc.com
- Documentação oficial da CERC

