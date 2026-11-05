#!/usr/bin/env python3
"""questoes.py - confere e embaralha questoes de multipla escolha.

Uso:
    python3 questoes.py checar questoes.json [--json]
    python3 questoes.py embaralhar questoes.json --semente 7 [-o saida.json]

Formato do JSON:
    {
      "titulo": "...",
      "questoes": [
        {"enunciado": "...", "alternativas": ["...", "...", "...", "..."], "correta": "C"}
      ]
    }
Campos extras (objetivo, comentario...) sao preservados no 'embaralhar'.
"""
import argparse
import json
import random
import re
import sys
import unicodedata

LETRAS = "ABCDE"
NEGACOES = {"nao", "exceto", "incorreta", "incorreto", "falsa", "falso", "errada", "errado"}
FRASES_ANTERIORES = ("anteriores", "alternativas acima", "todas as alternativas", "nenhuma das alternativas")
MIN_QUESTOES_POSICAO = 6
MIN_QUESTOES_TAMANHO = 5
LIMITE_VIES = 0.5


def dobrar(texto):
    t = unicodedata.normalize("NFD", str(texto))
    return "".join(c for c in t if unicodedata.category(c) != "Mn").lower()


def indice_correta(q):
    c = q.get("correta")
    if isinstance(c, str) and len(c.strip()) == 1 and c.strip().upper() in LETRAS:
        return LETRAS.index(c.strip().upper())
    return None


def e_anteriores(alt):
    d = dobrar(alt)
    return any(f in d for f in FRASES_ANTERIORES)


def negacao_sem_destaque(enunciado):
    """Devolve a palavra de negacao que aparece sem MAIUSCULAS nem **negrito**."""
    for m in re.finditer(r"\w+", enunciado):
        w = m.group(0)
        if dobrar(w) in NEGACOES:
            destacada = w.isupper() and len(w) > 1
            em_negrito = enunciado[max(0, m.start() - 2):m.start()] == "**"
            if not (destacada or em_negrito):
                return w
    return None


def checar(dados):
    achados = []

    def add(nivel, codigo, msg, q=None):
        achados.append({"nivel": nivel, "codigo": codigo,
                        "mensagem": (f"Questão {q}: " if q else "") + msg})

    qs = dados.get("questoes") if isinstance(dados, dict) else None
    if not isinstance(qs, list) or not qs:
        add("ERRO", "formato", "O arquivo precisa de uma lista 'questoes'.")
        return achados

    posicoes, mais_longa = [], 0
    validas_tamanho = 0
    for n, q in enumerate(qs, 1):
        if not isinstance(q, dict) or not str(q.get("enunciado") or "").strip():
            add("ERRO", "enunciado", "enunciado ausente ou vazio.", n)
            continue
        alts = q.get("alternativas")
        if not isinstance(alts, list) or not all(isinstance(a, str) and a.strip() for a in alts) or len(alts) < 2:
            add("ERRO", "alternativas", "precisa de uma lista de pelo menos 2 alternativas, todas preenchidas.", n)
            continue
        if not 4 <= len(alts) <= 5:
            add("ALERTA", "num_alternativas", f"tem {len(alts)} alternativas; o usual é 4 ou 5.", n)
        if len(alts) > len(LETRAS):
            add("ERRO", "alternativas", f"no máximo {len(LETRAS)} alternativas.", n)
            continue
        idx = indice_correta(q)
        if idx is None or idx >= len(alts):
            add("ERRO", "correta",
                f"'correta' deve ser uma letra de A a {LETRAS[len(alts) - 1]} (veio {q.get('correta')!r}).", n)
            idx = None
        vistos = {}
        for j, a in enumerate(alts):
            chave = dobrar(a).strip()
            if chave in vistos:
                add("ERRO", "duplicada", f"as alternativas {LETRAS[vistos[chave]]} e {LETRAS[j]} são iguais.", n)
            vistos.setdefault(chave, j)
            if e_anteriores(a):
                add("ALERTA", "anteriores",
                    f"a alternativa {LETRAS[j]} usa 'todas/nenhuma das anteriores'; "
                    "isso permite acertar sem saber a matéria.", n)
        neg = negacao_sem_destaque(str(q["enunciado"]))
        if neg:
            add("ALERTA", "negacao",
                f"o enunciado tem '{neg}' sem destaque. Escreva em MAIÚSCULAS ou **negrito** para ninguém errar por leitura.", n)
        if idx is not None:
            posicoes.append(idx)
            validas_tamanho += 1
            tam = [len(a.strip()) for a in alts]
            if tam[idx] == max(tam) and tam.count(max(tam)) == 1:
                mais_longa += 1

    if len(posicoes) >= MIN_QUESTOES_POSICAO:
        for p in set(posicoes):
            share = posicoes.count(p) / len(posicoes)
            if share > LIMITE_VIES:
                add("ALERTA", "posicao",
                    f"a letra {LETRAS[p]} é a correta em {posicoes.count(p)} de {len(posicoes)} questões "
                    f"({share:.0%}). Varie o gabarito.")
    if validas_tamanho >= MIN_QUESTOES_TAMANHO and mais_longa / validas_tamanho > LIMITE_VIES:
        add("ALERTA", "tamanho",
            f"a resposta correta é a alternativa mais longa em {mais_longa} de {validas_tamanho} questões. "
            "Quem chuta pelo tamanho acerta; equilibre os textos.")
    return achados


def embaralhar(dados, semente):
    rng = random.Random(semente)
    saida = json.loads(json.dumps(dados))
    gabarito = []
    for q in saida["questoes"]:
        alts = q["alternativas"]
        idx = indice_correta(q)
        if any(e_anteriores(a) for a in alts):
            gabarito.append(q["correta"].strip().upper())  # ordem fixa: a alternativa depende da posicao
            continue
        ordem = list(range(len(alts)))
        rng.shuffle(ordem)
        q["alternativas"] = [alts[i] for i in ordem]
        q["correta"] = LETRAS[ordem.index(idx)]
        gabarito.append(q["correta"])
    saida["gabarito"] = gabarito
    saida["semente"] = semente
    return saida


def main(argv=None):
    ap = argparse.ArgumentParser(description="Confere e embaralha questoes de multipla escolha.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("checar")
    c.add_argument("arquivo")
    c.add_argument("--json", action="store_true")
    e = sub.add_parser("embaralhar")
    e.add_argument("arquivo")
    e.add_argument("--semente", type=int, default=1)
    e.add_argument("-o", "--saida")
    args = ap.parse_args(argv)

    try:
        with open(args.arquivo, encoding="utf-8") as f:
            dados = json.load(f)
    except (OSError, ValueError) as e_:
        print(f"Não consegui ler {args.arquivo}: {e_}", file=sys.stderr)
        return 2

    achados = checar(dados)
    erros = sum(1 for a in achados if a["nivel"] == "ERRO")

    if args.cmd == "checar":
        alertas = len(achados) - erros
        if args.json:
            print(json.dumps({"erros": erros, "alertas": alertas, "achados": achados},
                             ensure_ascii=False, indent=2))
        else:
            if isinstance(dados, dict):
                print(f"Banco: {dados.get('titulo', '?')} ({len(dados.get('questoes', []))} questões)")
            if not achados:
                print("  Nenhum problema de forma encontrado.")
            for a in achados:
                print(f"  {a['nivel']:<7} [{a['codigo']}] {a['mensagem']}")
            print(f"Resultado: {erros} erro(s), {alertas} alerta(s).")
        return 1 if erros else 0

    if erros:
        print("O banco tem erros de forma; rode 'checar' e corrija antes de embaralhar.", file=sys.stderr)
        return 1
    texto = json.dumps(embaralhar(dados, args.semente), ensure_ascii=False, indent=2)
    if args.saida:
        with open(args.saida, "w", encoding="utf-8") as f:
            f.write(texto + "\n")
        print(f"Gravado em {args.saida} (semente {args.semente}).")
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
