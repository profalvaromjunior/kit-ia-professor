# Kit IA para Professores

Sete skills do Claude para o trabalho do professor, em português, com quatro verificadores em Python
que conferem o que a IA escreveu. Criado por **Álvaro Machado Júnior**.

Grátis, sem cadastro, sem chave de API. **A IA escreve o rascunho, o script confere a forma, e quem
decide é você.**

## O que tem aqui

| Comando | Para que serve | Verificador |
| --- | --- | --- |
| `/prof-plano` | Plano de uma aula: objetivos observáveis, momentos com minutos, avaliação, materiais | `plano.py` |
| `/prof-sequencia` | Sequência de 3 a 8 aulas encadeadas, com produto final | (checklist) |
| `/prof-atividade` | Atividade em três versões (básica, padrão, desafio), com processo visível | (checklist) |
| `/prof-rubrica` | Rubrica analítica com descritores observáveis, e a nota a partir dos níveis | `rubrica.py` |
| `/prof-questoes` | Múltipla escolha com gabarito comentado; embaralha as alternativas | `questoes.py` |
| `/prof-texto` | Texto de apoio no nível de leitura da turma | `legibilidade.py` |
| `/prof-uso-ia` | Níveis de uso de IA, combinado com a turma, declaração e cuidados com dados | (checklist) |

## Princípios

1. **Você decide.** Toda entrega traz uma lista "O que revisar".
2. **Sem dados de alunos.** Nada de nomes, notas ou laudos na IA. Use códigos (A01, A02). Veja `/prof-uso-ia`.
3. **Sem inventar.** Códigos da BNCC só entram se você informar.
4. **Conferir o que dá para conferir.** Somar minutos, somar pesos, achar alternativa repetida e medir
   frases longas é trabalho para um programa, não para a IA.

## Instalação

**1. Como plugin** no Claude Code:

```
/plugin marketplace add profalvaromjunior/kit-ia-professor
/plugin install kit-ia-professor@kit-ia-professor
```

No PowerShell ou no terminal, fora do Claude Code, troque a `/` por `claude`:
`claude plugin marketplace add profalvaromjunior/kit-ia-professor` e
`claude plugin install kit-ia-professor@kit-ia-professor`. É preciso ter o **Git** instalado.

Instalado como plugin, os comandos ganham o prefixo do kit: `/kit-ia-professor:prof-plano`,
`/kit-ia-professor:prof-rubrica` e assim por diante. Digite `/prof` e escolha na lista. Na instalação
manual (opção 3), o comando fica só `/prof-plano`.

**2. Pedindo ao próprio Claude**, colando no chat:

```
Instale as skills do repositório https://github.com/profalvaromjunior/kit-ia-professor
na minha pasta de skills e depois me mostre como usar /prof-plano.
```

**3. Manual, pelo terminal:**

```bash
git clone https://github.com/profalvaromjunior/kit-ia-professor.git
cp -r kit-ia-professor/skills/prof-* ~/.claude/skills/
```

Para usar só em um projeto, copie as pastas
para `.claude/skills/` dentro dele. Cada skill é independente: pode copiar só as que quiser.

Os verificadores precisam de **Python 3** (nenhuma biblioteca extra). Sem Claude Code, cole o
`SKILL.md` de uma skill no começo de uma conversa; você perde só os scripts.

## Primeiro passo: seu perfil

Copie [`templates/perfil-professor.md`](templates/perfil-professor.md) para
`~/.claude/professor/perfil.md` e preencha em dez minutos (disciplina, anos, recursos da escola, tom,
regras da escola sobre IA). As skills leem esse arquivo antes de fazer perguntas.

## Os verificadores

Python 3 puro. Todos aceitam arquivos em UTF-8 e retornam código de saída `1` quando há erro.

```bash
python3 skills/prof-plano/plano.py exemplos/plano_exemplo.json
python3 skills/prof-rubrica/rubrica.py validar exemplos/rubrica_ruim.json
python3 skills/prof-rubrica/rubrica.py nota exemplos/rubrica_exemplo.json --niveis 3,3,2,4
python3 skills/prof-questoes/questoes.py checar exemplos/questoes_com_problemas.json
python3 skills/prof-questoes/questoes.py embaralhar exemplos/questoes_exemplo.json --semente 7
python3 skills/prof-texto/legibilidade.py exemplos/texto_dificil.txt --alvo fund2
```

Cada exemplo existe em duas versões, uma limpa e outra com problemas, para você ver o que o
verificador aponta.

## Testes

```bash
python3 tests/test_ferramentas.py
```

32 testes cobrem os quatro verificadores, os exemplos e a estrutura do kit.

## Limites, ditos com franqueza

- **Os verificadores conferem a forma, não a qualidade pedagógica.** Um plano sem erros pode ser um
  mau plano.
- **A legibilidade é aproximada.** As sílabas são contadas por uma regra simples, e as faixas e os
  alvos por ano são orientações, não medidas oficiais.
- **A rubrica depende da escala de pontos por nível.** O padrão (nível *i* de *n* vale *i/n*) é uma
  escolha; ajuste com `pontos_niveis`.
- **Nada aqui é aconselhamento jurídico.** Siga a política da escola e a LGPD.
- **Confira os fatos** de qualquer texto, questão ou exemplo que a IA produzir.

## Para estudar como funciona

[`docs/COMO-FUNCIONA.md`](docs/COMO-FUNCIONA.md) explica a arquitetura (uma skill por pasta, scripts
ao lado, o `SKILL.md` como contrato) e propõe cinco laboratórios para estender o kit.

## Licença

MIT. Veja [`LICENSE`](LICENSE).
