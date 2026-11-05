---
name: prof-sequencia
description: Organiza uma sequência didática de 3 a 8 aulas encadeadas, com produto final e avaliação ao longo do caminho. Use quando o professor pedir "sequência didática", "unidade", "projeto de várias aulas" ou "planejamento do bimestre".
---

# prof-sequencia — sequência didática

Uma sequência é um caminho: cada aula deixa algo pronto para a seguinte. Seu trabalho é desenhar esse caminho e deixar claro o que cada aula entrega.

## Quando usar

- "Preciso de 5 aulas sobre …"
- "Transforme este tema em um projeto com entrega final"
- O professor tem aulas soltas e quer ligá-las

Para detalhar uma aula, passe para `prof-plano`.

## Antes de começar

1. Leia `~/.claude/professor/perfil.md`, se existir.
2. Pergunte de uma vez: tema, turma e ano, **quantas aulas e de quantos minutos**, o que os alunos devem ser capazes de fazer no final, recursos disponíveis, e se há data fixa (prova, feira, entrega).
3. Habilidades da BNCC só se o professor informar. Nunca invente códigos.

## Como fazer

1. **Comece pelo fim.** Escreva o produto final (o que o aluno entrega ou demonstra) em uma frase concreta.
2. **Divida em degraus.** Liste o que o aluno precisa saber fazer para chegar lá. Cada degrau vira uma aula ou parte de uma.
3. **Para cada aula**, escreva: pergunta que ela responde, o que os alunos fazem, o que fica pronto no fim ("entrega da aula") e como o professor percebe se foi atingido.
4. **Verifique o encadeamento.** A entrega da aula *n* é usada na aula *n+1*? Se não for, a ordem está errada ou a aula está solta.
5. **Reserve duas aulas de segurança**: uma de retomada no meio, outra no fim para finalizar e apresentar. Sequências sem folga atrasam.
6. **Avaliação ao longo do caminho.** Pelo menos duas verificações antes do produto final, com tempo para o professor devolver o retorno.
7. **Carga do professor.** Some o tempo de correção. Se a conta não fecha, simplifique o instrumento (rubrica curta, amostragem) em vez de prometer o que não cabe.

## Ferramenta

Esta skill não tem script. Confira à mão:

- [ ] Cada aula tem uma entrega visível.
- [ ] A entrega de cada aula alimenta a seguinte.
- [ ] Há retomada no meio e fechamento no fim.
- [ ] Há pelo menos duas verificações antes do produto final.
- [ ] O professor consegue corrigir tudo no tempo que tem.

Para cada aula que o professor queira detalhar, converta a linha da sequência em um plano e rode `prof-plano`.

## Entrega

Uma tabela com: aula, pergunta, o que os alunos fazem, entrega da aula, verificação. Abaixo, o produto final, o instrumento de avaliação sugerido (indique `prof-rubrica`) e a lista **O que revisar** (ritmo, recursos, datas).

## Limites

- Você propõe; o professor conhece o calendário e a turma.
- Não invente recursos que a escola pode não ter. Quando precisar de internet ou computadores, diga e ofereça uma versão sem eles.
- Não prometa que a sequência "garante" aprendizagem.
