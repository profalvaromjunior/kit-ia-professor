---
name: prof-uso-ia
description: Define com o professor como a turma pode usar IA (níveis de permissão), gera o combinado e o modelo de declaração de uso, e lembra os cuidados do professor com dados de alunos (LGPD). Use quando pedirem "política de IA", "regras de uso de IA na turma", "declaração de uso de IA" ou "posso colocar dados do aluno na IA?".
---

# prof-uso-ia — combinados claros sobre IA

Proibir sem conversar não funciona, e liberar sem regra também não. Esta skill ajuda o professor a escolher um **nível de uso por atividade**, comunicar isso à turma e pedir uma declaração simples do que foi feito.

## Quando usar

- "Que regra de IA eu coloco neste trabalho?"
- "Escreva o combinado para a turma"
- "Como o aluno declara que usou IA?"
- "Posso colar a redação do aluno aqui?"

## Antes de começar

1. Leia `~/.claude/professor/perfil.md`, se existir. **Se a escola tem política própria de IA ou de dados, ela vale mais do que qualquer sugestão aqui.** Pergunte se existe.
2. Pergunte: qual é a atividade, o que o aluno precisa aprender nela e se a avaliação é em sala ou em casa.

## Como fazer

### 1. Escolher o nível (por atividade)

| Nível | Regra | Quando faz sentido |
| --- | --- | --- |
| 0 | Sem IA | O objetivo é a habilidade de fazer sozinho (primeiras leituras, cálculo básico, escrita inicial) |
| 1 | IA só para ideias e dúvidas; o texto é do aluno | Brainstorm, tirar dúvidas, revisar entendimento |
| 2 | IA para rascunho; o aluno revisa, corrige e declara | Produção em que revisar é parte da aprendizagem |
| 3 | IA livre, com declaração e registro do processo | Projetos em que usar bem a ferramenta é o objetivo |

Ajude o professor a ligar o nível ao **objetivo** da atividade, não ao medo.

### 2. Escrever o combinado

Uma página para a turma, em linguagem do ano: qual é o nível, o que pode, o que não pode, o que fazer em caso de dúvida e como será visto o processo. Tom de combinado, não de ameaça.

### 3. Modelo de declaração (cole na atividade)

```
Declaração de uso de IA
Usei IA nesta atividade?  ( ) Não   ( ) Sim
Se sim:
- Para que usei: ______________________
- O que ela sugeriu e eu NÃO aproveitei: ______________________
- O que eu mudei ou corrigi: ______________________
- Uma coisa que a IA errou ou que precisei conferir: ______________________
```

### 4. Verificar sem acusar

Detectores automáticos de texto de IA têm taxas de erro conhecidas e não devem ser prova única. Prefira o **processo visível** (rascunhos, histórico, decisões) e uma conversa curta com o aluno sobre o que escreveu. Se houver dúvida, converse antes de concluir.

### 5. Cuidados do professor com dados (LGPD)

- Não cole nomes, matrículas, notas, laudos, fotos ou trabalhos identificáveis de alunos em ferramentas de IA, a menos que a escola tenha autorização e contrato para isso.
- Use **códigos** (A01, A02) ao pedir ajuda com devolutivas e depois substitua você mesmo.
- Dados de crianças e adolescentes pedem cuidado redobrado.
- Em caso de dúvida, consulte a direção ou o encarregado de dados da escola.

Esta skill não é aconselhamento jurídico.

## Ferramenta

Sem script. Checklist:

- [ ] O nível foi escolhido por atividade e combina com o objetivo.
- [ ] A turma recebeu o combinado por escrito.
- [ ] Há modelo de declaração.
- [ ] A verificação passa pelo processo, não só por detector.
- [ ] Nenhum dado identificável de aluno foi colado.

## Entrega

O nível sugerido com a justificativa em duas linhas, o combinado para a turma e a declaração. **O que revisar:** a política da escola e se o nível vale para esta turma.

## Limites

- Você sugere; a decisão e a responsabilidade são do professor e da escola.
- Se o professor colar dados de alunos, não os repita nem os use; avise com gentileza e peça para trocar por códigos.
- Não existe regra única que funcione para todas as turmas; ajuste com a experiência do professor.
