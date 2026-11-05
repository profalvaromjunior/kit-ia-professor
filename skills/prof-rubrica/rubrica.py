#!/usr/bin/env python3
"""rubrica.py - valida uma rubrica analitica e calcula notas a partir dela.

Uso:
    python3 rubrica.py validar rubrica.json [--json]
    python3 rubrica.py nota rubrica.json --niveis 3,3,2,4
    python3 rubrica.py nota rubrica.json --niveis "Proficiente,Proficiente,Basico,Avancado"

Formato do JSON:
    {
      "titulo": "...",
      "niveis": ["Insuficiente", "Basico", "Proficiente", "Avancado"],
      "criterios": [
        {"nome": "...", "peso": 30, "descritores": ["...", "...", "...", "..."]}
      ],
      "nota_maxima": 10,                      (opcional, padrao 10)
      "pontos_niveis": [0.25, 0.5, 0.75, 1]   (opcional: fracao do peso por nivel)
    }

Sem 'pontos_niveis', o nivel i de n vale i/n do peso (o nivel mais baixo ainda vale 1/n).
Descritores sao listados do nivel mais baixo para o mais alto, na ordem de 'niveis'.
"""
import argparse
import json
import re
import sys
import unicodedata

SUBJETIVAS = {
    "bom", "boa", "otimo", "otima", "ruim", "adequado", "adequada", "razoavel",
    "satisfatorio", "satisfatoria", "regular", "fraco", "fraca", "excelente",
}
LIMITE_PESO = 50
SIMILARIDADE = 0.75


def dobrar(texto):
    t = unicodedata.normalize("NFD", str(texto))
    return "".join(c for c in t if unicodedata.category(c) != "Mn").lower()


def palavras(texto):
    return re.findall(r"\w+", dobrar(texto))


def numero(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def validar(r):
    achados = []

    def add(nivel, codigo, msg):
        achados.append({"nivel": nivel, "codigo": codigo, "mensagem": msg})

    if not isinstance(r, dict):
        add("ERRO", "formato", "O arquivo deve conter um objeto JSON.")
        return achados

    niveis = r.get("niveis")
    if (not isinstance(niveis, list) or len(niveis) < 2
            or not all(isinstance(n, str) and n.strip() for n in niveis)):
        add("ERRO", "niveis", "'niveis' deve ser uma lista com pelo menos 2 nomes.")
        niveis = []
    elif len({dobrar(n).strip() for n in niveis}) != len(niveis):
        add("ERRO", "niveis", "Há nomes de nível repetidos.")

    criterios = r.get("criterios")
    if not isinstance(criterios, list) or not criterios:
        add("ERRO", "criterios", "'criterios' deve ser uma lista com pelo menos 1 critério.")
        return achados

    total = 0.0
    total_valido = True
    for i, c in enumerate(criterios, 1):
        if not isinstance(c, dict):
            add("ERRO", "criterio", f"Critério {i} deve ser um objeto.")
            total_valido = False
            continue
        nome = str(c.get("nome") or f"critério {i}")
        peso = c.get("peso")
        if not numero(peso) or peso <= 0:
            add("ERRO", "peso", f"'{nome}': 'peso' deve ser um número maior que zero.")
            total_valido = False
        else:
            total += peso
            if peso > LIMITE_PESO:
                add("ALERTA", "peso_alto",
                    f"'{nome}' vale {peso:g}% da nota. Um critério só decide a nota quando passa de {LIMITE_PESO}%.")
        desc = c.get("descritores")
        if not isinstance(desc, list):
            add("ERRO", "descritores", f"'{nome}': 'descritores' deve ser uma lista.")
            continue
        if niveis and len(desc) != len(niveis):
            add("ERRO", "descritores",
                f"'{nome}' tem {len(desc)} descritores para {len(niveis)} níveis.")
        vistos = []
        for j, d in enumerate(desc, 1):
            rotulo = niveis[j - 1] if j - 1 < len(niveis) else f"nível {j}"
            if not isinstance(d, str) or not d.strip():
                add("ERRO", "descritor_vazio", f"'{nome}', {rotulo}: descritor vazio.")
                vistos.append(None)
                continue
            ws = palavras(d)
            subj = sorted(set(ws) & SUBJETIVAS)
            if subj:
                add("ALERTA", "subjetivo",
                    f"'{nome}', {rotulo}: usa '{subj[0]}'. Descreva o que se vê no trabalho, não um juízo.")
            vistos.append((dobrar(d).strip(), set(ws), rotulo))
        reais = [v for v in vistos if v]
        for a in range(len(reais)):
            for b in range(a + 1, len(reais)):
                if reais[a][0] == reais[b][0]:
                    add("ERRO", "duplicado",
                        f"'{nome}': {reais[a][2]} e {reais[b][2]} têm o mesmo descritor.")
                else:
                    uniao = reais[a][1] | reais[b][1]
                    if uniao and len(reais[a][1] & reais[b][1]) / len(uniao) >= SIMILARIDADE:
                        add("ALERTA", "quase_igual",
                            f"'{nome}': {reais[a][2]} e {reais[b][2]} são quase iguais; "
                            "o aluno não saberia a diferença.")
    if total_valido and abs(total - 100) > 1e-9:
        add("ERRO", "pesos", f"Os pesos somam {total:g}, e devem somar 100.")

    pn = r.get("pontos_niveis")
    if pn is not None:
        if (not isinstance(pn, list) or len(pn) != len(niveis) or not all(numero(x) and 0 <= x <= 1 for x in pn)
                or any(pn[k] > pn[k + 1] for k in range(len(pn) - 1))):
            add("ERRO", "pontos_niveis",
                "'pontos_niveis' deve ter um valor de 0 a 1 por nível, sem diminuir.")
    nm = r.get("nota_maxima", 10)
    if not numero(nm) or nm <= 0:
        add("ERRO", "nota_maxima", "'nota_maxima' deve ser um número maior que zero.")
    return achados


def resolver_nivel(token, niveis):
    token = token.strip()
    if token.isdigit():
        i = int(token)
        if 1 <= i <= len(niveis):
            return i - 1
        raise ValueError(f"nível {i} não existe (use de 1 a {len(niveis)})")
    alvo = dobrar(token)
    for i, n in enumerate(niveis):
        if dobrar(n) == alvo:
            return i
    raise ValueError(f"nível '{token}' não existe (opções: {', '.join(niveis)})")


def calcular(r, tokens):
    niveis = r["niveis"]
    crit = r["criterios"]
    if len(tokens) != len(crit):
        raise ValueError(f"A rubrica tem {len(crit)} critérios, mas você deu {len(tokens)} níveis.")
    n = len(niveis)
    pontos = r.get("pontos_niveis") or [(i + 1) / n for i in range(n)]
    maxima = r.get("nota_maxima", 10)
    linhas = []
    total = 0.0
    for c, t in zip(crit, tokens):
        i = resolver_nivel(t, niveis)
        parcial = c["peso"] / 100 * pontos[i] * maxima
        total += parcial
        linhas.append({"criterio": c["nome"], "nivel": niveis[i], "peso": c["peso"],
                       "pontos": round(parcial, 2), "maximo": round(c["peso"] / 100 * maxima, 2)})
    return {"linhas": linhas, "nota": round(total, 2), "nota_maxima": maxima}


def imprimir_achados(achados, como_json):
    erros = sum(1 for a in achados if a["nivel"] == "ERRO")
    alertas = len(achados) - erros
    if como_json:
        print(json.dumps({"erros": erros, "alertas": alertas, "achados": achados},
                         ensure_ascii=False, indent=2))
        return erros
    if not achados:
        print("  Nenhum problema de forma encontrado.")
    for a in achados:
        print(f"  {a['nivel']:<7} [{a['codigo']}] {a['mensagem']}")
    print(f"Resultado: {erros} erro(s), {alertas} alerta(s).")
    return erros


def main(argv=None):
    ap = argparse.ArgumentParser(description="Valida rubricas e calcula notas.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validar")
    v.add_argument("arquivo")
    v.add_argument("--json", action="store_true")
    n = sub.add_parser("nota")
    n.add_argument("arquivo")
    n.add_argument("--niveis", required=True,
                   help="um nível por critério, na ordem: números (1 a n) ou nomes, separados por virgula")
    n.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    try:
        with open(args.arquivo, encoding="utf-8") as f:
            rubrica = json.load(f)
    except (OSError, ValueError) as e:
        print(f"Não consegui ler {args.arquivo}: {e}", file=sys.stderr)
        return 2

    achados = validar(rubrica)
    if args.cmd == "validar":
        if not args.json and isinstance(rubrica, dict):
            print(f"Rubrica: {rubrica.get('titulo', '?')}")
        return 1 if imprimir_achados(achados, args.json) else 0

    # nota: so calcula se a forma estiver correta
    if any(a["nivel"] == "ERRO" for a in achados):
        print("A rubrica tem erros de forma; corrija antes de calcular notas:", file=sys.stderr)
        imprimir_achados([a for a in achados if a["nivel"] == "ERRO"], False)
        return 1
    try:
        res = calcular(rubrica, args.niveis.split(","))
    except ValueError as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"Rubrica: {rubrica.get('titulo', '?')}")
        for l in res["linhas"]:
            print(f"  {l['criterio']:<32} {l['nivel']:<14} {l['pontos']:>5.2f} / {l['maximo']:.2f}")
        print(f"Nota: {res['nota']:.2f} de {res['nota_maxima']:g}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
