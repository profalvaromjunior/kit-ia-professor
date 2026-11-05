---
name: prof-texto
description: Escreve ou adapta um texto de apoio para o nível de leitura da turma e mede a legibilidade com legibilidade.py (índice de Flesch adaptado ao português). Use quando o professor pedir "texto de apoio", "simplificar texto", "adaptar leitura" ou "esse texto está difícil para a turma?".
---

# prof-texto — texto na medida da turma

Um texto de apoio só ajuda se a turma consegue lê-lo sozinha. Você escreve ou adapta, **mede** e ajusta até chegar perto do alvo, sem infantilizar.

## Quando usar

- "Escreva um texto de uma página sobre … para o 7º ano"
- "Simplifique este texto sem perder o conteúdo"
- "Este texto está adequado para o 5º ano?"

## Antes de começar

1. Leia `~/.claude/professor/perfil.md`, se existir.
2. Pergunte: tema, ano, tamanho aproximado, se há termos técnicos que **precisam** aparecer (eles ficam, com explicação) e a fonte, se for adaptar um texto existente.
3. Se o texto original é de outra pessoa (livro, artigo), adapte apenas o que o professor tem direito de usar e não reproduza trechos longos. Em dúvida, escreva um texto novo a partir das ideias.

## Como fazer

1. Escreva ou adapte. Frases curtas, uma ideia por frase, voz ativa, exemplos do dia a dia.
2. Termos técnicos: use, explique na primeira vez e junte um pequeno glossário.
3. Salve em `texto.txt` e meça com o alvo da turma.
4. Veja as **frases longas** que o script lista. Divida-as ou corte o que não é essencial.
5. Meça de novo. Pare quando chegar perto do alvo; não force o índice à custa de clareza.
6. Leia o resultado como um aluno leria: o texto ficou confuso ou seco? O índice mede palavras e sílabas, não sentido.

## Ferramenta

O script fica nesta pasta (por exemplo `~/.claude/skills/prof-texto/legibilidade.py`).

```bash
python3 legibilidade.py texto.txt --alvo fund2
python3 legibilidade.py texto.txt --alvo fund1 --json
```

Alvos (índice mínimo orientativo): `fund1` 65, `fund2` 50, `medio` 35. Faixas gerais: 75–100 muito fácil, 50–75 fácil, 25–50 difícil, 0–25 muito difícil. O índice pode até ficar negativo em textos muito densos.

**Aproximado, por construção.** As sílabas são contadas por uma regra simples de grupos de vogais e as frases pela pontuação; erros de alguns pontos para mais ou para menos são esperados. Trate o número como termômetro, não como sentença. Abreviações com ponto ("Sr.", "etc.") podem criar frases falsas.

## Entrega

O texto final, o índice com a faixa e o alvo (dizendo que é aproximado), as frases longas que sobraram, se houver, e o glossário. Termine com **O que revisar**: se o vocabulário combina com a turma, se algum exemplo precisa ser trocado por um mais próximo e se a informação está correta.

## Limites

- Legibilidade não é qualidade nem correção do conteúdo. Confira os fatos e as fontes.
- Textos para alunos com dificuldades de leitura específicas pedem um olhar do professor e da equipe pedagógica; o índice não substitui isso.
- Não ponha nomes de alunos nos textos.
