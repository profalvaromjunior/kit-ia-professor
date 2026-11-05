#!/usr/bin/env python3
"""legibilidade.py - estima a facilidade de leitura de um texto em portugues.

Uso:
    python3 legibilidade.py texto.txt [--alvo fund1|fund2|medio] [--json]

Indice: Flesch adaptado ao portugues (Martins et al., 1996):
    248,835 - 1,015 * (palavras/frases) - 84,6 * (silabas/palavra)
Faixas: 75-100 muito facil | 50-75 facil | 25-50 dificil | 0-25 muito dificil.

ATENCAO: as silabas sao contadas por uma heuristica de grupos de vogais, e a
divisao de frases e feita por pontuacao. O resultado e uma ORIENTACAO (alguns
pontos para mais ou para menos), nao uma medida exata. Nao substitui a leitura
do professor, que conhece a turma.
"""
import argparse
import json
import re
import sys
import unicodedata

VOGAIS = set("aeiouáéíóúâêôãõàü")
FORTES = set("aeoáéóâêôãõà")
FRACAS = set("iuíúü")
ALVO_MINIMO = {"fund1": 65, "fund2": 50, "medio": 35}
FRASE_LONGA = 25

PALAVRA = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*", re.UNICODE)


def silabas_parte(p):
    p = p.lower()
    p = unicodedata.normalize("NFC", p)
    p = re.sub(r"(?<=[qg])u(?=[eéêií])", "", p)  # u mudo: que, qui, gue, gui
    n = len(p)
    total = 0
    i = 0
    while i < n:
        if p[i] not in VOGAIS:
            i += 1
            continue
        j = i
        while j < n and p[j] in VOGAIS:
            j += 1
        grupo = p[i:j]
        depois = p[j:]
        total += 1
        for k in range(1, len(grupo)):
            ant, v = grupo[k - 1], grupo[k]
            posicao = i + k
            if ant == "ã" and v in "oe" or ant == "õ" and v == "e":
                continue  # ditongo nasal: ão, ãe, õe
            if v in "íú":
                total += 1  # hiato acentuado: sa-í-da, pa-ís
            elif ant in FORTES and v in FORTES:
                total += 1  # hiato: le-ão, po-e-ta
            elif ant in FORTES and v in FRACAS:
                pass        # ditongo decrescente: ai, ei, oi, au, eu, ou
            elif ant in FRACAS and v in FRACAS:
                pass        # ui, iu
            else:           # fraca + forte: ditongo crescente?
                antes = p[posicao - 2] if posicao >= 2 else ""
                if ant == "u" and antes in ("q", "g"):
                    pass    # qua, gua: á-gua
                elif posicao == j - 1 and depois in ("", "s") and total > 1:
                    pass    # final átono depois de outra sílaba: fa-mí-lia
                else:
                    total += 1
        i = j
    return total


def silabas(palavra):
    return max(1, sum(silabas_parte(parte) for parte in palavra.split("-")))


def dividir_frases(texto):
    frases = []
    for bloco in re.split(r"\n\s*\n", texto):
        bloco = " ".join(bloco.split())
        for f in re.split(r"(?<=[.!?…])\s+", bloco):
            if PALAVRA.search(f):
                frases.append(f.strip())
    return frases


def analisar(texto):
    frases = dividir_frases(texto)
    por_frase = [PALAVRA.findall(f) for f in frases]
    n_pal = sum(len(p) for p in por_frase)
    if n_pal == 0:
        return None
    n_sil = sum(silabas(w) for p in por_frase for w in p)
    n_fr = len(frases)
    pf = n_pal / n_fr
    sp = n_sil / n_pal
    indice = 248.835 - 1.015 * pf - 84.6 * sp
    if indice >= 75:
        faixa = "muito fácil"
    elif indice >= 50:
        faixa = "fácil"
    elif indice >= 25:
        faixa = "difícil"
    else:
        faixa = "muito difícil"
    longas = [{"palavras": len(p), "inicio": f[:70]} for f, p in zip(frases, por_frase) if len(p) > FRASE_LONGA]
    return {"palavras": n_pal, "frases": n_fr, "palavras_por_frase": round(pf, 1),
            "silabas_por_palavra": round(sp, 2), "indice": round(indice, 1),
            "faixa": faixa, "frases_longas": longas}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Estima a legibilidade de um texto em portugues.")
    ap.add_argument("arquivo")
    ap.add_argument("--alvo", choices=sorted(ALVO_MINIMO))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        with open(args.arquivo, encoding="utf-8") as f:
            texto = f.read()
    except OSError as e:
        print(f"Não consegui ler {args.arquivo}: {e}", file=sys.stderr)
        return 2
    r = analisar(texto)
    if r is None:
        print("O texto está vazio ou não tem palavras.", file=sys.stderr)
        return 2
    if args.alvo:
        r["alvo"] = args.alvo
        r["indice_minimo_do_alvo"] = ALVO_MINIMO[args.alvo]
        r["dentro_do_alvo"] = r["indice"] >= ALVO_MINIMO[args.alvo]
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    print(f"Palavras: {r['palavras']}   Frases: {r['frases']}   "
          f"Palavras/frase: {r['palavras_por_frase']}   Sílabas/palavra: {r['silabas_por_palavra']}")
    print(f"Índice de leitura: {r['indice']} ({r['faixa']})  [estimativa aproximada]")
    if args.alvo:
        if r["dentro_do_alvo"]:
            print(f"Alvo {args.alvo} (minimo {ALVO_MINIMO[args.alvo]}): dentro do alvo.")
        else:
            print(f"Alvo {args.alvo} (minimo {ALVO_MINIMO[args.alvo]}): ABAIXO do alvo; o texto tende a ser difícil demais.")
    if r["frases_longas"]:
        print(f"Frases com mais de {FRASE_LONGA} palavras:")
        for f in r["frases_longas"]:
            print(f"  ({f['palavras']} palavras) {f['inicio']}...")
    print("Lembrete: o índice é uma orientação; quem conhece a turma decide.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
