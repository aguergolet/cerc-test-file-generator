# Estrutura do Arquivo AP008 - CERC

## Descrição
**CERC-AP008** – ENVIO DE EFEITOS DE CONTRATOS APLICÁVEIS ÀS UNIDADES DE RECEBÍVEIS PARA FINS DE LIQUIDAÇÃO

## Diretório de Saída
`\efeitos_contrato\saida`

## Estrutura de Campos

### Campos Principais

| Campo | Nome | Formato | Regra | Observação |
|-------|------|---------|-------|------------|
| 1 | Referência Externa | Alfa(256) | Obrigatório | Código de referência único (exclusivo), de controle do participante, para identificação nas próximas transações relacionadas |
| 2 | Identificador do Contrato | Alfa(256) | Obrigatório | Código identificador do contrato na entidade registradora requisitante |
| 3 | Entidade Registradora | Alfa(14) | Obrigatório | CNPJ da entidade registradora requisitante. Sem formatação. Preenchidos com 0 à esquerda |
| 4 | Instituição Credenciadora ou Subcredenciadora | Alfa(14) | Obrigatório | CNPJ da instituição credenciadora ou subcredenciadora responsável pelos reflexos das unidades de recebíveis consultadas. Formato: 14 dígitos para CNPJ e 11 dígitos para CPF |
| 5 | Usuário Final Recebedor | Alfa(14) | Obrigatório | CNPJ ou CPF do usuário final recebedor das unidades de recebíveis consultadas. Formato: 14 dígitos para CNPJ e 11 dígitos para CPF |
| 6 | Arranjo de Pagamento | Alfa(3) | Obrigatório | Código constante da tabela vigente neste manual |
| 7.1 | Identificador Efeito Contrato | Alfa | Obrigatório | Protocolo do efeito de contrato |
| 7.2 | Data de Liquidação | Data | Obrigatório | Data de liquidação do recebível prevista pelo arranjo de pagamento ou com efeitos da antecipação pré-contratada. Formato: AAAA-MM-DD |
| 7.3 | Titular da Unidade de Recebível | Alfa(14) | Obrigatório | CNPJ ou CPF do titular da UR. Sem formatação. Preenchidos com 0 à esquerda |
| 7.4 | Constituição da Unidade de Recebível | Alfa(1) | Obrigatório | Tipo da constituição da unidade de recebível, sendo: 1 = Constituída, 2 = A constituir |
| 7.5 | Valor Constituído Total | Decimal | Obrigatório (se constituição = 1) | Valor constituído total da unidade de recebível |
| 7.6 | Valor Bloqueado | Decimal | Obrigatório | Valor bloqueado para pagamento na unidade de recebível |
| 7.7 | Indicador de Oneração | Alfa | Obrigatório | Identificador sequencial que indica a prioridade do ônus, sendo: 0 = Insucesso; 1 a N = Prioridade do ônus |
| 7.8 | Regra de Divisão | Alfa(1) | Obrigatório | Critério de comprometimento da unidade de recebível, podendo ser: 1 = Comprometimento de valor definido; 2 = Comprometimento de percentual do valor que vier a ser constituído |
| 7.9 | Valor Onerado na Unidade de Recebível | Decimal | Obrigatório | Parâmetro do comprometimento (número percentual ou valor em reais), conforme a regra da divisão contratada |
| 7.10 | Protocolo | Alfa | Obrigatório | Protocolo do processamento da operação |
| 7.11 | Data Hora do Evento | Alfa | Obrigatório | Data no formato RFC3339 |
| 7.12 | Status da Operação | Alfa(1) | Obrigatório | Código que identifica o status da operação, sendo: 0 = Sucesso, 1 = Falha |
| 7.13 | Código do Erro | Número | Obrigatório (se status = 1) | Código do erro se houve falha no processamento da operação |
| 7.14 | Descrição do Erro | Alfa(max. 1000) | Obrigatório (se status = 1) | Descrição se houve falha no processamento da operação |
| 7.15 | Valor Constituído do Efeito de Contrato na Unidade de Recebível | Decimal | Opcional | Valor calculado pela CERC aplicando o efeito de contrato na Unidade de Recebível. Representa o montante do valor constituído total que foi afetado pelo efeito |
| 7.16 | Número Documento Titular da Conta para Liquidação | Alfa(14) | Obrigatório | CPF ou CNPJ do titular da conta bancária ou conta de pagamento. Formatação: Preencher até 11 caracteres para CPF ou 14 caracteres com CNPJ, sempre com os 0 à esquerda |
| 7.17 | Tipo de Conta | Alfa(2) | Obrigatório | Tipo de conta onde o pagamento será liquidado: CC = Conta Corrente; CD = Conta de Depósito; CG = Conta Garantia; CI = Conta Investimento; PG = Conta de Pagamento; PP = Conta Poupança |
| 7.18 | COMPE | Alfa(3) | Opcional | Código COMPE da Instituição de Domicílio, complementar com 0 à esquerda |
| 7.19 | ISPB | Alfa(8) | Obrigatório | Número do ISPB da Instituição de Domicílio, complementar com 0 à esquerda |
| 7.20 | Agência | Alfa | Obrigatório (se tipo de conta diferente de PG) | Número da Agência para pagamento. Formato: sem dígito verificador |
| 7.21 | Número da Conta ou Número da Conta de Pagamento | Alfa(20) | Obrigatório | Conta CC, CD, CG, CI ou PP: Informar número com dígito verificador, separado por hífen (ex. 999999-9). Conta PG: Informar número sem hífen (ex. 9999999) |
| 7.22 | Nome Titular da Conta para Liquidação | Alfa | Opcional | Nome do titular da conta bancária ou conta de pagamento |

## Formato do Arquivo

- **Extensão**: `.csv`
- **Separador**: Ponto e vírgula (`;`) - **IMPORTANTE**: Conforme especificação CERC
- **Encoding**: UTF-8
- **Formato de Data**: AAAA-MM-DD
- **Formato de Data/Hora**: RFC3339
- **Sem cabeçalho**: O arquivo não deve conter linha de cabeçalho

## Estrutura do Campo 7 (Lista)

O **Campo 7** é uma lista que pode conter múltiplas contas de pagamento para a mesma UR:

- **Campos 7.1 a 7.15**: Informações do efeito de contrato (não se repetem)
- **Campos 7.16 a 7.22**: Informações bancárias (podem se repetir - uma conta por vez)

### Formato da Lista no Campo 7

Quando há múltiplas contas, o campo 7 deve ser formatado como:
```
"campo7.1;campo7.2;...;campo7.15;conta1_info|conta2_info|conta3_info"
```

Onde:
- Campos dentro do efeito são separados por `;` (ponto e vírgula)
- Múltiplas contas são separadas por `|` (pipe)
- Campos dentro de cada conta são separados por `;` (ponto e vírgula)
- O campo completo é encapsulado em aspas duplas quando há múltiplas contas

**Exemplo com 2 contas:**
```
"EFEITO_001;2025-12-04;12345678901234;1;10000.50;0.00;1;1;10000.50;PROT_001;2025-11-27T10:00:00Z;0;;;10000.50;12345678901;CC;001;12345678;1234;123456-7;João Silva|98765432109;CC;001;12345678;1234;987654-3;Maria Santos"
```

## Nomenclatura do Arquivo

**Máscara**: `CERC-AP008_Ident_IC_DataReq_Seq.csv`

Onde:
- `Tipo_Leiaute`: Nome do tipo de leiaute gerado, fixo "CERC-AP008"
- `Ident_IC`: Identificação da Instituição Credenciadora, considerando a raiz do seu CNPJ (8 dígitos)
- `DataReq`: Data do envio do arquivo, no formato "YYYYMMDD", somente números
- `Seq`: Número sequencial inteiro maior que 0, no formato 7 dígitos, iniciando por "0000001"

**Exemplo**: `CERC-AP008_53462828_20190221_0000001.csv`

## Observações Importantes

1. O arquivo AP008 é gerado pela CERC e disponibilizado no diretório `\efeitos_contrato\saida`
2. Este arquivo contém informações sobre os efeitos de contratos aplicados às unidades de recebíveis para fins de liquidação
3. O campo 7.1 (Identificador Efeito Contrato) corresponde ao protocolo do efeito de contrato
4. O campo 7.4 (Tipo de Efeito) pode conter os seguintes valores:
   - 1 = Troca de titularidade
   - 2 = Ônus - Cessão fiduciária
   - 3 = Ônus - Outros
   - 4 = Bloqueio judicial
   - 8 = Promessa de Cessão

## Referências

- Manual de Interfaces da CERC
- Documentação oficial da CERC disponível em: https://cerc-2.gitbook.io/

