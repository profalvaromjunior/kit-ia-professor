---
name: prof-questoes
description: Cria questões de múltipla escolha com gabarito e justificativa, confere vícios comuns (resposta mais longa, gabarito repetido, "todas as anteriores") e embaralha as alternativas com questoes.py. Use quando o professor pedir "questões", "prova", "banco de questões", "quiz" ou "gabarito".
---

# prof-questoes — múltipla escolha sem vício

Questão de múltipla escolha boa tem uma resposta correta clara e erros que **fazem sentido**. Você escreve as questões; o `questoes.py` procura os vícios que fazem o aluno acertar pelo jeito da prova e não pela matéria.

## Quando usar

- "Faça 8 questões sobre …"
- "Revise estas questões" (o professor cola o banco)
- "Preciso de duas versões da prova"

## Antes de começar

1. Leia `~/.claude/professor/perfil.md`, se existir.
2. Pergunte: conteúdo coberto, ano, quantidade, nível de dificuldade e o objetivo de cada bloco. Se o professor tem o texto da aula, use-o; **não complete com fatos de memória que ele não possa conferir**.

## Como fazer

1. Um **objetivo por questão** (campo opcional `objetivo` no JSON). Se uma questão não mede nenhum objetivo, corte.
2. **Enunciado completo**: dá para responder antes de olhar as alternativas.
3. **4 alternativas** (ou 5), uma só correta.
4. **Distratores** inspirados em erros reais de aluno (confundir dois conceitos, errar uma etapa), não em absurdos.
5. Alternativas com **tamanho parecido** e mesma forma gramatical.
6. Negação (**NÃO**, **EXCETO**) só em MAIÚSCULAS ou negrito.
7. Evite "todas as anteriores" e "nenhuma das anteriores".
8. **Gabarito com justificativa**: por que a correta está certa e qual erro cada distrator representa.
9. Varie a letra da correta.
10. Grave em JSON e rode `checar`.

Formato:

```json
{
  "titulo": "Redes e segurança, 6º ano",
  "questoes": [
    {"enunciado": "...", "alternativas": ["...", "...", "...", "..."],
     "correta": "C", "objetivo": "Reconhecer equipamentos de rede",
     "comentario": "A: confunde com ... B: ..."}
  ]
}
```

## Ferramenta

O script fica nesta pasta (por exemplo `~/.claude/skills/prof-questoes/questoes.py`).

```bash
python3 questoes.py checar banco.json
python3 questoes.py embaralhar banco.json --semente 7 -o prova_B.json
```

`checar`: **erros** para alternativas repetidas, letra correta inexistente, enunciado vazio; **alertas** para "todas/nenhuma das anteriores", negação sem destaque, número de alternativas diferente de 4 a 5, uma letra correta em mais da metade das questões (com 6 ou mais) e resposta correta como a mais longa em mais da metade (com 5 ou mais).

`embaralhar`: mistura as alternativas de cada questão, atualiza a letra correta e escreve o `gabarito` no arquivo. A mesma `--semente` dá sempre a mesma prova, então a versão B pode ser refeita depois. Questões com "anteriores" ficam como estão, porque dependem da ordem.

## Entrega

As questões prontas para a prova, o gabarito com justificativas em uma seção separada para o professor, e o resultado do `checar` em uma linha. Termine com **O que revisar**: dificuldade, se a matéria cobrada foi realmente dada, e se os distratores refletem erros que a turma costuma cometer.

## Limites

- O `checar` encontra vícios de forma. Não diz se a questão está correta no conteúdo: o professor confere.
- Não reutilize questões de provas oficiais ou de livros por memória; escreva questões novas a partir do conteúdo informado.
- Não ponha nomes de alunos nas questões.
