---
name: prof-atividade
description: Cria uma atividade para os alunos em três versões (básica, padrão, desafio), com processo visível e declaração de uso de IA. Use quando o professor pedir "atividade", "exercício", "trabalho", "tarefa" ou "projeto" para uma turma.
---

# prof-atividade — atividade em três versões

Uma boa atividade diz com clareza o que fazer, como saber que terminou e o que entregar. Aqui ela também mostra **como o aluno chegou lá**, porque hoje o resultado final sozinho diz pouco.

## Quando usar

- "Crie uma atividade sobre … para o 8º ano"
- "Adapte esta atividade para a turma que está atrasada"
- "Quero um trabalho que não dê para copiar da IA"

## Antes de começar

1. Leia `~/.claude/professor/perfil.md`, se existir.
2. Pergunte (uma vez): objetivo da atividade, turma e ano, tempo disponível, individual ou em grupo, recursos, e a regra de uso de IA nesta atividade (veja `prof-uso-ia`; se não houver, proponha o nível 1 ou 2 e peça confirmação).
3. Sobre alunos com necessidades específicas: **pergunte ao professor o que a turma precisa** ("há alguma adaptação que eu deva prever?"). Não suponha, não rotule alunos, não peça diagnóstico.

## Como fazer

1. **Enunciado curto.** Duas ou três frases no máximo, com o verbo do objetivo.
2. **Passo a passo.** Numerado, cada passo com um resultado que o aluno consegue conferir sozinho.
3. **Critério de êxito.** "Terminei quando …", em linguagem do aluno. Se houver rubrica, aponte para ela (`prof-rubrica`).
4. **Tempo estimado** por parte, mais uma margem.
5. **Três versões** do mesmo objetivo:
   - **Básica**: mais apoio (modelo pronto para completar, exemplo resolvido, vocabulário dado).
   - **Padrão**: a atividade como foi pensada.
   - **Desafio**: o mesmo objetivo em situação nova ou com restrição extra. Não é "mais do mesmo".
6. **Processo visível.** Peça uma evidência do caminho: rascunho, captura de tela, lista de decisões, ou uma conversa de dois minutos com o professor. Escolha uma que caiba na turma.
7. **Declaração de uso de IA.** Inclua o modelo de `prof-uso-ia` adequado ao nível definido.
8. **Texto de apoio.** Se a atividade traz um texto, ofereça medir a leitura com `prof-texto`.

## Ferramenta

Sem script. Checklist antes de entregar:

- [ ] O objetivo da atividade é o mesmo nas três versões.
- [ ] Um aluno consegue começar sozinho lendo só o enunciado.
- [ ] Há como saber que terminou.
- [ ] Há evidência do processo.
- [ ] A regra de IA está escrita.
- [ ] Nenhum dado de aluno aparece no material.

## Entrega

A atividade pronta para imprimir ou projetar: enunciado, passos, critério de êxito, versões, o que entregar e a declaração de IA. Depois, um bloco **Para o professor** (gabarito ou exemplo de resposta, tempo real esperado, erros comuns que você prevê) e **O que revisar**.

## Limites

- Você não sabe quais alunos precisam de qual versão. Quem distribui as versões é o professor.
- Evite atividades que só medem se o aluno consegue pedir à IA a resposta. Peça o raciocínio, a escolha e a justificativa.
- Exemplos e contextos devem ser reais e próximos da turma; se não souber, pergunte.
