# Como o kit funciona

Guia de estudo para quem quer entender, copiar a ideia ou estender. Serve também como roteiro de aula.

## 1. Mapa

```
kit-ia-professor/
├── .claude-plugin/        plugin.json e marketplace.json (para instalar como plugin)
├── skills/
│   ├── prof-plano/        SKILL.md + plano.py
│   ├── prof-sequencia/    SKILL.md
│   ├── prof-atividade/    SKILL.md
│   ├── prof-rubrica/      SKILL.md + rubrica.py
│   ├── prof-questoes/     SKILL.md + questoes.py
│   ├── prof-texto/        SKILL.md + legibilidade.py
│   └── prof-uso-ia/       SKILL.md
├── exemplos/              entradas limpas e entradas com problemas
├── templates/             perfil-professor.md
├── tests/                 test_ferramentas.py (32 testes)
└── docs/
```

## 2. Uma skill por dentro

Uma skill é uma **pasta** com um `SKILL.md`. O arquivo tem duas partes:

1. **Cabeçalho (frontmatter)**, entre `---`: `name` e `description`. A descrição lista as frases que
   devem ativar a skill ("plano de aula", "preparar a aula"). É ela que faz o Claude escolher a skill.
2. **Corpo em Markdown**: as instruções. Neste kit, todas seguem o mesmo roteiro: *Quando usar*, *Antes
   de começar*, *Como fazer*, *Ferramenta*, *Entrega* e *Limites*.

Os scripts ficam **na mesma pasta** da skill e não importam nada de outras. Por isso dá para copiar
uma skill sozinha para outro computador e ela continua funcionando.

## 3. Quem faz o quê

| Tarefa | Quem faz | Por quê |
| --- | --- | --- |
| Escrever objetivos, atividades, questões, textos | O modelo (IA) | Linguagem e variedade |
| Somar minutos e pesos, achar alternativa repetida, contar frases | O script | Conta exata, sempre igual |
| Decidir se a aula serve para a turma | O professor | Só ele conhece a turma |

A regra de projeto: **tudo que for verificável por regra vai para um script**; o modelo não "confere de
cabeça". Os scripts devolvem um código de saída (`0` bem, `1` erro de forma, `2` entrada ilegível),
o que permite usá-los em outros programas.

## 4. Anatomia de um verificador

Os quatro seguem o mesmo molde:

1. **Ler** o arquivo (JSON ou texto) e tratar erro de leitura (saída `2`).
2. **Normalizar** o texto para comparar palavras: minúsculas e sem acentos (`unicodedata`, forma NFD,
   removendo marcas). Assim "ÓTIMO" e "otimo" são a mesma palavra.
3. **Aplicar regras** pequenas e independentes, cada uma com um `codigo`, um `nivel` (ERRO ou ALERTA)
   e uma mensagem em português.
4. **Mostrar** em texto ou em `--json`, e sair com `1` se houver ERRO.

Repare na diferença entre **ERRO** (a forma está quebrada: pesos que somam 110) e **ALERTA** (vale
olhar, mas pode estar certo: um momento de 30 minutos). Essa distinção é uma decisão de projeto.

## 5. Onde o kit é honesto sobre seus limites

- `legibilidade.py` conta sílabas com uma regra de grupos de vogais. Funciona bem para o português
  comum, mas erra em casos como hiatos pouco usuais e palavras estrangeiras.
- `questoes.py` pode apontar `negacao` num enunciado onde "não" não é pegadinha.
- `rubrica.py nota` depende de uma escala de pontos por nível que é escolha do professor.

Um bom exercício é encontrar mais casos assim e escrever um teste para cada um.

## 6. Cinco laboratórios

1. **Quebre de propósito.** Edite `exemplos/plano_exemplo.json` para provocar cada código do
   `plano.py`. Anote a mensagem de cada um e proponha uma mensagem melhor.
2. **Conte as sílabas.** Ache cinco palavras em que `silabas()` erra em `legibilidade.py`. Descreva a
   regra do português que a heurística ignora e tente corrigi-la sem quebrar `test_silabas`.
3. **Nova regra para rubricas.** Faça o `validar` avisar quando os descritores de um critério ficam
   cada vez mais curtos (sinal de preguiça ao escrever os níveis altos). Escreva primeiro o teste.
4. **Nova skill.** Crie `prof-devolutiva` (comentário individual para o aluno a partir de uma rubrica
   preenchida), com a regra de usar só códigos de aluno. Escreva o `SKILL.md` e a lista "O que revisar".
5. **Teste a skill, não só o script.** Peça o mesmo plano a três pessoas ou três modelos diferentes,
   rode `plano.py` em cada um e compare os alertas. O que se repete mostra o que a skill ainda não
   ensina bem; ajuste o `SKILL.md` e repita.

## 7. Ideias para evoluir

- Exportar o plano e a rubrica para documento de texto ou planilha.
- Ler a rubrica de um arquivo de planilha em vez de JSON.
- Verificar que uma atividade cobre todos os critérios da rubrica.
- Medir a distribuição de dificuldade de um banco de questões, quando houver dados de uso.
