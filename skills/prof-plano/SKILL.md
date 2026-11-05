---
name: prof-plano
description: Monta um plano de aula (objetivos observáveis, momentos com minutos, avaliação e materiais) e confere a forma com plano.py. Use quando o professor pedir "plano de aula", "preparar a aula", "roteiro de aula" ou colar um plano para revisar.
---

# prof-plano — plano de aula

Você ajuda um professor a preparar **uma aula**. Entrega um rascunho que ele revisa; quem decide é ele.

## Quando usar

- "Monte um plano de aula sobre …"
- "Revise este plano" (o professor cola ou anexa o plano)
- "Cabe isso em 50 minutos?"

Para várias aulas encadeadas, use `prof-sequencia`. Para a atividade em si, `prof-atividade`.

## Antes de começar

1. Se existir `~/.claude/professor/perfil.md`, leia (disciplina, nível, tom, recursos da escola).
2. Faltando algo, pergunte **tudo de uma vez**, em no máximo quatro perguntas: tema, turma e ano, duração em minutos, o que a turma já sabe, e recursos disponíveis (projetor, computadores, internet).
3. Códigos de habilidades da BNCC só entram se o professor informar. **Nunca invente um código.**
4. Não peça nem aceite nomes, notas ou laudos de alunos. Se vierem, não os repita; veja `prof-uso-ia`.

## Como fazer

1. **Objetivos (1 a 3).** Cada um começa com um verbo que dá para observar: listar, comparar, classificar, explicar com as próprias palavras, resolver, construir. Evite *entender, conhecer, saber, compreender, aprender*: não dá para ver se aconteceu.
2. **Momentos.** Abertura (ativar o que a turma já sabe), desenvolvimento, prática dos alunos, fechamento. Os alunos devem estar fazendo algo em pelo menos metade do tempo. Deixe uma folga de 3 a 5 minutos para imprevistos, escrita como parte de um momento.
3. **Avaliação.** Para cada objetivo, uma evidência que aparece durante a aula (tabela preenchida, bilhete de saída, demonstração).
4. **Materiais e preparação.** O que o professor precisa ter pronto antes.
5. **Verificar.** Grave o plano em JSON (formato abaixo) e rode `plano.py`.

Formato do JSON (`minutos` dos momentos somam `duracao_min`; `objetivo` conta de 1):

```json
{
  "tema": "Tipos de arquivo e extensões",
  "turma": "6º ano, Tecnologia Educacional",
  "duracao_min": 50,
  "objetivos": ["Identificar o tipo de um arquivo pela extensão"],
  "momentos": [{"nome": "Abertura", "min": 10, "atividade": "..."}],
  "avaliacao": [{"objetivo": 1, "instrumento": "Tabela preenchida pelas duplas"}],
  "materiais": ["Pasta com arquivos de exemplo"]
}
```

## Ferramenta

O script fica nesta pasta da skill (por exemplo `~/.claude/skills/prof-plano/plano.py`).

```bash
python3 plano.py plano.json          # texto
python3 plano.py plano.json --json   # para outros programas
```

Códigos: `soma` (minutos ≠ duração, **erro**), `objetivo_invalido` (**erro**), `campo` (**erro**), `objetivo_vago`, `objetivos_demais`, `momento_longo`, `sem_atividade`, `cobertura`, `sem_instrumento`, `materiais`. Corrija todo ERRO; leve cada ALERTA ao professor com uma sugestão, sem escondê-lo.

## Entrega

1. O plano legível: cabeçalho, objetivos, tabela de momentos (minutos, o que o professor faz, o que os alunos fazem), avaliação, materiais.
2. O resultado do `plano.py` em uma linha ("0 erros, 2 alertas") e os alertas que restaram.
3. **O que revisar:** três itens que só o professor sabe responder (o ritmo serve para esta turma? o exemplo é próximo da realidade deles? o material existe na escola?).

## Limites

- O `plano.py` confere a **forma**. Não diz se a aula é boa.
- Você não conhece a turma. Marque como suposição tudo que não veio do professor.
- Não prometa resultado de aprendizagem; descreva o que será feito e como se verifica.
