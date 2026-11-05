---
name: prof-rubrica
description: Cria e valida rubricas analíticas (critérios, pesos, níveis e descritores observáveis) e calcula a nota a partir dos níveis escolhidos, com rubrica.py. Use quando o professor pedir "rubrica", "critérios de avaliação", "barema" ou "como corrigir este trabalho".
---

# prof-rubrica — rubrica que se pode usar

Uma rubrica vale pelo que o aluno consegue ler nela: o que o trabalho precisa ter para estar em cada nível. Seu trabalho é escrever descritores **observáveis** e conferir a conta.

## Quando usar

- "Faça uma rubrica para este trabalho"
- "Esta rubrica está boa?" (o professor cola a dele)
- "Dei nível 3 em conteúdo e 2 em organização, quanto dá?"

## Antes de começar

1. Leia `~/.claude/professor/perfil.md`, se existir.
2. Pergunte: qual é a tarefa, qual o objetivo, quantos níveis o professor usa (padrão: 4) e se a nota é de 0 a 10 ou outra escala.
3. Se existe uma atividade escrita (`prof-atividade`), use-a como base: os critérios devem medir o que ela pede.

## Como fazer

1. **3 a 5 critérios**, cada um medindo uma coisa só. Dê nomes curtos.
2. **Pesos** em porcentagem, somando 100. Evite um critério com mais de 50%: ele decide a nota sozinho.
3. **Níveis** com nomes neutros e ordem crescente (por exemplo Insuficiente, Básico, Proficiente, Avançado).
4. **Descritores**: um por critério e por nível, do mais baixo ao mais alto. Cada um diz o que se **vê** no trabalho (quantidade, presença, funcionamento), não um juízo. Em vez de "bom exemplo", escreva "dá pelo menos um exemplo do dia a dia".
5. Dois descritores vizinhos devem diferir em algo que o aluno possa mudar na próxima versão.
6. Inclua um critério de **processo** (registro das etapas, declaração de uso de IA) quando a atividade pedir.
7. Grave em JSON e valide.

Formato:

```json
{
  "titulo": "Mini-projeto: site de uma página",
  "niveis": ["Insuficiente", "Básico", "Proficiente", "Avançado"],
  "nota_maxima": 10,
  "criterios": [
    {"nome": "Conteúdo", "peso": 30,
     "descritores": ["...nível 1...", "...nível 2...", "...nível 3...", "...nível 4..."]}
  ]
}
```

Opcional: `"pontos_niveis": [0, 0.4, 0.75, 1]` define quanto do peso cada nível vale. Sem ele, o nível *i* de *n* vale *i/n* (com 4 níveis: 25%, 50%, 75%, 100%). **Essa escolha muda a nota; mostre ao professor e deixe ele decidir.**

## Ferramenta

O script fica nesta pasta (por exemplo `~/.claude/skills/prof-rubrica/rubrica.py`).

```bash
python3 rubrica.py validar rubrica.json
python3 rubrica.py nota rubrica.json --niveis 3,3,2,4
python3 rubrica.py nota rubrica.json --niveis "Proficiente,Avançado,Básico,Proficiente"
```

`validar` aponta: pesos que não somam 100, número de descritores diferente do de níveis, descritor vazio ou repetido (**erros**); palavras de juízo (bom, ruim, adequado, razoável, satisfatório, regular, fraco, excelente), descritores quase iguais e critério acima de 50% (**alertas**). `nota` recusa-se a calcular se houver erro, e mostra os pontos por critério.

## Entrega

A rubrica em tabela, o resultado do `validar` (uma linha) e, se o professor deu níveis, a nota com o detalhe por critério. Termine com **O que revisar**: a escala de pontos por nível e se cada critério mede o que o professor quer.

## Limites

- A rubrica confere forma e conta. Não garante que os critérios sejam justos.
- A nota calculada é uma sugestão para o professor, que pode ajustar com base no que viu.
- Não use dados de alunos reais ao testar: identifique por código (A01, A02).
