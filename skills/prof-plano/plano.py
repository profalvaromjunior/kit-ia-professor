#!/usr/bin/env python3
"""plano.py - confere a FORMA de um plano de aula escrito em JSON.

Uso:
    python3 plano.py plano.json [--json]

Formato do JSON:
    {
      "tema": "...", "turma": "...", "duracao_min": 50,
      "objetivos": ["Identificar ...", "Comparar ..."],
      "momentos": [{"nome": "Abertura", "min": 8, "atividade": "..."}],
      "avaliacao": [{"objetivo": 1, "instrumento": "..."}],
      "materiais": ["..."]
    }

Niveis de achado: ERRO (a forma esta quebrada; saida 1) e ALERTA (vale olhar).
Este verificador NAO avalia a qualidade pedagogica: so confere a forma.
"""
import argparse
import json
import re
import sys
import unicodedata

VERBOS_VAGOS = {
    "entender", "conhecer", "saber", "compreender", "aprender",
    "apreciar", "dominar", "perceber", "valorizar", "refletir",
}
LIMITE_MOMENTO = 0.40      # fracao da duracao que um momento unico pode ocupar
LIMITE_OBJETIVOS = 3       # para aulas de ate 60 min
DURACAO_CURTA = 60


def dobrar(texto):
    """Minusculas e sem acentos, para comparar palavras."""
    t = unicodedata.normalize("NFD", str(texto))
    return "".join(c for c in t if unicodedata.category(c) != "Mn").lower()


def numero(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def verificar(p):
    achados = []

    def add(nivel, codigo, msg):
        achados.append({"nivel": nivel, "codigo": codigo, "mensagem": msg})

    if not isinstance(p, dict):
        add("ERRO", "formato", "O arquivo deve conter um objeto JSON (chaves { }).")
        return achados

    for campo in ("tema", "turma", "duracao_min", "objetivos", "momentos", "avaliacao"):
        if p.get(campo) in (None, "", []):
            add("ERRO", "campo", f"Campo obrigatório ausente ou vazio: {campo}.")

    dur = p.get("duracao_min")
    if "duracao_min" in p and p["duracao_min"] not in (None, "", []):
        if not numero(dur) or dur <= 0:
            add("ERRO", "duracao", "duracao_min deve ser um número maior que zero.")
            dur = None
    else:
        dur = None

    # objetivos
    objetivos = p.get("objetivos")
    if not isinstance(objetivos, list):
        objetivos = []
    objetivos = [o for o in objetivos if isinstance(o, str) and o.strip()]
    for i, o in enumerate(objetivos, 1):
        primeiras = re.findall(r"\w+", dobrar(o))[:4]
        vagos = [w for w in primeiras if w in VERBOS_VAGOS]
        if vagos:
            add("ALERTA", "objetivo_vago",
                f"Objetivo {i} usa '{vagos[0]}', verbo difícil de observar. "
                "Troque por algo que se veja (listar, comparar, explicar com as próprias palavras, resolver).")
    if dur is not None and dur <= DURACAO_CURTA and len(objetivos) > LIMITE_OBJETIVOS:
        add("ALERTA", "objetivos_demais",
            f"{len(objetivos)} objetivos para uma aula de {dur:g} min. Considere no máximo {LIMITE_OBJETIVOS}.")

    # momentos
    momentos = p.get("momentos")
    if not isinstance(momentos, list):
        momentos = []
    soma = 0.0
    soma_valida = True
    for i, m in enumerate(momentos, 1):
        if not isinstance(m, dict):
            add("ERRO", "momento", f"Momento {i} deve ser um objeto com nome, min e atividade.")
            soma_valida = False
            continue
        nome = m.get("nome") or f"momento {i}"
        if not numero(m.get("min")) or m.get("min") <= 0:
            add("ERRO", "momento", f"'{nome}' precisa de 'min' numérico maior que zero.")
            soma_valida = False
            continue
        soma += m["min"]
        if not str(m.get("atividade") or "").strip():
            add("ALERTA", "sem_atividade", f"'{nome}' não descreve a atividade.")
        if dur and m["min"] > LIMITE_MOMENTO * dur:
            add("ALERTA", "momento_longo",
                f"'{nome}' ocupa {m['min']:g} de {dur:g} min "
                f"({m['min'] / dur:.0%}). Considere dividir ou variar a atividade.")
    if dur is not None and soma_valida and momentos and abs(soma - dur) > 1e-9:
        add("ERRO", "soma",
            f"Os momentos somam {soma:g} min, mas a duração é {dur:g} min.")

    # avaliacao
    avaliacao = p.get("avaliacao")
    if not isinstance(avaliacao, list):
        avaliacao = []
    cobertos = set()
    for i, a in enumerate(avaliacao, 1):
        if not isinstance(a, dict):
            add("ERRO", "avaliacao", f"Item {i} da avaliação deve ser um objeto.")
            continue
        idx = a.get("objetivo")
        if isinstance(idx, bool) or not isinstance(idx, int) or not 1 <= idx <= len(objetivos):
            add("ERRO", "objetivo_invalido",
                f"Avaliação {i} aponta para o objetivo {idx!r}, que não existe "
                f"(use de 1 a {len(objetivos)}).")
        else:
            cobertos.add(idx)
        if not str(a.get("instrumento") or "").strip():
            add("ALERTA", "sem_instrumento", f"Avaliação {i} não diz o instrumento (como se verifica).")
    for i in range(1, len(objetivos) + 1):
        if i not in cobertos:
            add("ALERTA", "cobertura", f"O objetivo {i} não tem nenhuma forma de avaliação ligada a ele.")

    # materiais
    mats = p.get("materiais")
    if not isinstance(mats, list) or not [x for x in mats if str(x).strip()]:
        add("ALERTA", "materiais", "Nenhum material listado. Se não precisa de nada, escreva isso.")

    return achados


def main(argv=None):
    ap = argparse.ArgumentParser(description="Confere a forma de um plano de aula (JSON).")
    ap.add_argument("arquivo")
    ap.add_argument("--json", action="store_true", help="saida em JSON")
    args = ap.parse_args(argv)
    try:
        with open(args.arquivo, encoding="utf-8") as f:
            plano = json.load(f)
    except (OSError, ValueError) as e:
        print(f"Não consegui ler {args.arquivo}: {e}", file=sys.stderr)
        return 2

    achados = verificar(plano)
    erros = sum(1 for a in achados if a["nivel"] == "ERRO")
    alertas = len(achados) - erros

    if args.json:
        print(json.dumps({"erros": erros, "alertas": alertas, "achados": achados},
                         ensure_ascii=False, indent=2))
    else:
        if isinstance(plano, dict):
            print(f"Plano: {plano.get('tema', '?')} ({plano.get('turma', '?')}, "
                  f"{plano.get('duracao_min', '?')} min)")
        if not achados:
            print("  Nenhum problema de forma encontrado.")
        for a in achados:
            print(f"  {a['nivel']:<7} [{a['codigo']}] {a['mensagem']}")
        print(f"Resultado: {erros} erro(s), {alertas} alerta(s).")
        print("Nota: este verificador confere a forma; a qualidade pedagógica é decisão sua.")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
