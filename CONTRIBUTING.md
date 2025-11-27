# Guia de Contribuição

Obrigado por seu interesse em contribuir para este projeto! Este guia explica como você pode colaborar diretamente como contributor.

## 🎯 Por que Contributor e não Fork?

Este projeto utiliza um modelo de colaboração direta onde contributors trabalham em branches do repositório principal, ao invés de fazer fork. Isso facilita:

- ✅ Revisão de código mais rápida
- ✅ Melhor comunicação entre contributors
- ✅ Histórico de commits mais organizado
- ✅ Integração contínua mais eficiente

## 🚀 Como Começar

### 1. Obter Acesso de Contributor

Se você ainda não tem acesso de contributor, entre em contato com o mantenedor do projeto para solicitar permissões de escrita no repositório.

### 2. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd ap008
```

### 3. Configurar seu Ambiente

Certifique-se de ter Python 3.6+ instalado:

```bash
python3 --version
```

### 4. Criar uma Branch para sua Contribuição

**IMPORTANTE**: Sempre crie uma nova branch a partir da `main` ou `master`:

```bash
# Atualizar a branch principal
git checkout main
git pull origin main

# Criar sua branch de trabalho
git checkout -b feature/nome-da-sua-feature
# ou
git checkout -b fix/nome-do-bug
# ou
git checkout -b docs/melhorias-na-documentacao
```

### Convenções de Nomenclatura de Branches

- `feature/` - Para novas funcionalidades
- `fix/` - Para correções de bugs
- `docs/` - Para melhorias na documentação
- `refactor/` - Para refatoração de código
- `test/` - Para adicionar ou melhorar testes

## 📝 Processo de Contribuição

### 1. Desenvolver sua Contribuição

- Faça suas alterações no código
- Adicione testes se necessário
- Atualize a documentação se sua mudança requer
- Certifique-se de que o código segue os padrões do projeto

### 2. Testar suas Alterações

Antes de fazer commit, teste suas alterações:

```bash
# Exemplo para AP008
cd ap008/ap008
python3 generate_ap008.py 5
```

### 3. Commitar suas Alterações

Use mensagens de commit claras e descritivas:

```bash
git add .
git commit -m "feat(ap008): adiciona suporte para múltiplas contas bancárias"
```

**Formato de Commit Messages:**

```
tipo(escopo): descrição curta

Descrição detalhada (opcional)

- Item 1
- Item 2
```

**Tipos de commit:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação, ponto e vírgula faltando, etc
- `refactor`: Refatoração de código
- `test`: Adicionar testes
- `chore`: Tarefas de manutenção

### 4. Fazer Push da sua Branch

```bash
git push origin feature/nome-da-sua-feature
```

### 5. Criar um Pull Request

1. Vá para o repositório no GitHub/GitLab
2. Você verá um banner sugerindo criar um Pull Request
3. Clique em "Create Pull Request"
4. Preencha o template do PR:
   - **Título**: Descrição clara e concisa
   - **Descrição**: Explique o que foi feito e por quê
   - **Checklist**: Marque os itens relevantes

### Template de Pull Request

```markdown
## Descrição
Breve descrição das mudanças realizadas.

## Tipo de Mudança
- [ ] Nova funcionalidade
- [ ] Correção de bug
- [ ] Melhoria de documentação
- [ ] Refatoração

## Checklist
- [ ] Meu código segue os padrões do projeto
- [ ] Realizei uma auto-revisão do meu código
- [ ] Comentei código complexo quando necessário
- [ ] Minhas mudanças não geram novos warnings
- [ ] Adicionei testes que provam que minha correção é efetiva ou que minha funcionalidade funciona
- [ ] Testes novos e existentes passam localmente
- [ ] Atualizei a documentação conforme necessário
```

## 📋 Padrões de Código

### Python

- Use Python 3.6+
- Siga PEP 8 para estilo de código
- Use type hints quando possível
- Documente funções e classes com docstrings

### Estrutura de Arquivos

Cada tipo de AP deve ter sua própria pasta:
```
ap008/
├── ap001/
├── ap002/
├── ap008/
│   ├── generate_ap008.py
│   ├── generate_ap008.json
│   └── README.md
```

### Nomenclatura

- **Métodos e variáveis**: Inglês
- **Endpoints e URLs**: Inglês
- **Labels e textos para usuário**: Português
- **Entidades de banco de dados**: Inglês

## 🧪 Testes

Antes de fazer push, certifique-se de que:

- [ ] Seu código funciona corretamente
- [ ] Não quebrou funcionalidades existentes
- [ ] Os arquivos gerados estão no formato correto

## 🔍 Revisão de Código

Após criar o Pull Request:

1. Aguarde a revisão de pelo menos um mantenedor
2. Responda aos comentários e faça as alterações solicitadas
3. Faça push das correções na mesma branch
4. O PR será atualizado automaticamente

## ✅ Após Aprovação

Quando seu PR for aprovado:

1. Um mantenedor fará o merge
2. Sua branch será deletada automaticamente (se configurado)
3. Suas mudanças estarão na branch principal!

## 🐛 Reportando Problemas

Se encontrar um bug ou tiver uma sugestão:

1. Verifique se já existe uma issue aberta
2. Se não existir, crie uma nova issue
3. Use o template apropriado
4. Forneça informações detalhadas

## 💡 Sugerindo Melhorias

Para sugerir melhorias:

1. Crie uma issue com a label "enhancement"
2. Descreva claramente a melhoria proposta
3. Explique o caso de uso
4. Aguarde feedback antes de começar a implementar

## 📚 Recursos Úteis

- [Documentação CERC](https://cerc-2.gitbook.io/)
- [PEP 8 - Style Guide for Python Code](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## ❓ Dúvidas?

Se tiver dúvidas sobre como contribuir:

1. Verifique a documentação existente
2. Procure em issues anteriores
3. Abra uma issue com a label "question"
4. Entre em contato com os mantenedores

## 🙏 Obrigado!

Sua contribuição é muito valiosa para este projeto. Obrigado por dedicar seu tempo e esforço!

