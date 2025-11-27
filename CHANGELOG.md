# Changelog - Gerador AP008

## Versão 2.0 - Configuração via JSON

### Novas Funcionalidades

1. **Configuração via JSON**
   - Arquivo `generate_ap008.json` para configuração centralizada
   - CNPJ da credenciadora configurável (apenas 1, pois é instrução de pagamento)

2. **Geração Aleatória de Dados**
   - Seleção aleatória de CNPJs de EC do arquivo CSV
   - Seleção aleatória de contas bancárias do arquivo CSV
   - Geração de valores aleatórios dentro dos limites configurados
   - Geração de prioridades aleatórias (1 até prioridade_maxima)

3. **Cálculo Automático de Data de Liquidação**
   - Data de liquidação = Data atual + dias_futuros_liquidacao
   - Configurável no arquivo JSON

4. **Arquivos de Entrada**
   - `cnpjs_estabelecimentos.csv`: Lista de CNPJs de estabelecimentos comerciais
   - `contas_bancarias.csv`: Lista de contas bancárias com dados completos

### Arquivos Criados

- `generate_ap008.json` - Arquivo de configuração
- `cnpjs_estabelecimentos.csv` - Lista de CNPJs de EC
- `contas_bancarias.csv` - Lista de contas bancárias

### Melhorias

- Script mais flexível e configurável
- Geração automática de dados realistas
- Validação de arquivos de entrada
- Mensagens de erro mais claras

### Como Usar

```bash
# Gera 10 registros (padrão)
python3 generate_ap008.py

# Gera N registros
python3 generate_ap008.py N
```

