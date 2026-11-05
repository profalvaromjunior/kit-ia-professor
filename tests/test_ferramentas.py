#!/usr/bin/env python3
"""Testes dos quatro verificadores do kit. Uso: python3 tests/test_ferramentas.py"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(RAIZ, "exemplos")


def caminho(skill, script):
    return os.path.join(RAIZ, "skills", skill, script)


def rodar(skill, script, *args):
    p = subprocess.run([sys.executable, "-I", caminho(skill, script), *args],
                       capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout, p.stderr


def carregar(skill, script):
    spec = importlib.util.spec_from_file_location(script[:-3], caminho(skill, script))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ler(caminho_json):
    with open(caminho_json, encoding="utf-8") as f:
        return json.load(f)


def ex(nome):
    return os.path.join(EX, nome)


def codigos(saida_json):
    return {a["codigo"] for a in json.loads(saida_json)["achados"]}


class TestPlano(unittest.TestCase):
    def test_exemplo_limpo(self):
        rc, out, _ = rodar("prof-plano", "plano.py", ex("plano_exemplo.json"))
        self.assertEqual(rc, 0, out)
        self.assertIn("0 erro(s), 0 alerta(s)", out)

    def test_problemas(self):
        rc, out, _ = rodar("prof-plano", "plano.py", ex("plano_com_problemas.json"), "--json")
        self.assertEqual(rc, 1)
        d = json.loads(out)
        self.assertEqual(d["erros"], 1)
        c = codigos(out)
        for esperado in ("soma", "objetivo_vago", "objetivos_demais", "momento_longo",
                         "sem_atividade", "cobertura", "materiais"):
            self.assertIn(esperado, c)

    def test_soma_usa_numeros_certos(self):
        _, out, _ = rodar("prof-plano", "plano.py", ex("plano_com_problemas.json"))
        self.assertIn("somam 60 min, mas a duração é 50 min", out)

    def test_objetivo_invalido(self):
        mod = carregar("prof-plano", "plano.py")
        plano = ler(ex("plano_exemplo.json"))
        plano["avaliacao"][0]["objetivo"] = 9
        self.assertIn("objetivo_invalido", {a["codigo"] for a in mod.verificar(plano)})

    def test_campo_ausente_e_tipos_errados(self):
        mod = carregar("prof-plano", "plano.py")
        self.assertEqual(mod.verificar([])[0]["codigo"], "formato")
        achados = mod.verificar({"tema": "x", "duracao_min": "50", "momentos": [1]})
        c = {a["codigo"] for a in achados}
        self.assertIn("campo", c)
        self.assertIn("duracao", c)
        self.assertIn("momento", c)

    def test_arquivo_inexistente(self):
        rc, _, err = rodar("prof-plano", "plano.py", "nao_existe.json")
        self.assertEqual(rc, 2)
        self.assertIn("Não consegui ler", err)


class TestRubrica(unittest.TestCase):
    def test_exemplo_limpo(self):
        rc, out, _ = rodar("prof-rubrica", "rubrica.py", "validar", ex("rubrica_exemplo.json"))
        self.assertEqual(rc, 0, out)

    def test_rubrica_ruim(self):
        rc, out, _ = rodar("prof-rubrica", "rubrica.py", "validar", ex("rubrica_ruim.json"), "--json")
        self.assertEqual(rc, 1)
        d = json.loads(out)
        self.assertEqual(d["erros"], 3)
        c = codigos(out)
        for esperado in ("pesos", "descritores", "duplicado", "subjetivo", "peso_alto"):
            self.assertIn(esperado, c)
        self.assertIn("somam 110", out)

    def test_nota_por_numeros(self):
        rc, out, _ = rodar("prof-rubrica", "rubrica.py", "nota", ex("rubrica_exemplo.json"),
                           "--niveis", "3,3,2,4", "--json")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["nota"], 7.5)

    def test_nota_por_nomes_sem_acento(self):
        rc, out, _ = rodar("prof-rubrica", "rubrica.py", "nota", ex("rubrica_exemplo.json"),
                           "--niveis", "Proficiente,Avancado,basico,Proficiente", "--json")
        self.assertEqual(rc, 0, out)
        self.assertEqual(json.loads(out)["nota"], 7.75)

    def test_nota_pontos_niveis(self):
        mod = carregar("prof-rubrica", "rubrica.py")
        r = ler(ex("rubrica_exemplo.json"))
        r["pontos_niveis"] = [0, 0.4, 0.75, 1]
        self.assertEqual(mod.calcular(r, ["1", "1", "1", "1"])["nota"], 0.0)
        self.assertEqual(mod.calcular(r, ["4", "4", "4", "4"])["nota"], 10.0)

    def test_nota_numero_errado_de_niveis(self):
        rc, _, err = rodar("prof-rubrica", "rubrica.py", "nota", ex("rubrica_exemplo.json"), "--niveis", "3,3")
        self.assertEqual(rc, 2)
        self.assertIn("4 critérios", err)

    def test_nota_recusa_rubrica_com_erro(self):
        rc, _, err = rodar("prof-rubrica", "rubrica.py", "nota", ex("rubrica_ruim.json"), "--niveis", "1,1,1")
        self.assertEqual(rc, 1)
        self.assertIn("erros de forma", err)

    def test_quase_igual(self):
        mod = carregar("prof-rubrica", "rubrica.py")
        r = {"niveis": ["A", "B"], "criterios": [{"nome": "X", "peso": 100, "descritores": [
            "O trabalho está organizado e completo", "O trabalho está organizado e completo e claro"]}]}
        self.assertIn("quase_igual", {a["codigo"] for a in mod.validar(r)})

    def test_palavra_subjetiva_com_acento(self):
        mod = carregar("prof-rubrica", "rubrica.py")
        r = {"niveis": ["A", "B"], "criterios": [{"nome": "X", "peso": 100, "descritores": [
            "Resultado ÓTIMO", "Resultado com dois exemplos"]}]}
        self.assertIn("subjetivo", {a["codigo"] for a in mod.validar(r)})


class TestQuestoes(unittest.TestCase):
    def test_exemplo_limpo(self):
        rc, out, _ = rodar("prof-questoes", "questoes.py", "checar", ex("questoes_exemplo.json"))
        self.assertEqual(rc, 0, out)
        self.assertIn("0 erro(s), 0 alerta(s)", out)

    def test_problemas(self):
        rc, out, _ = rodar("prof-questoes", "questoes.py", "checar", ex("questoes_com_problemas.json"), "--json")
        self.assertEqual(rc, 1)
        c = codigos(out)
        for esperado in ("duplicada", "anteriores", "num_alternativas", "posicao", "tamanho", "negacao"):
            self.assertIn(esperado, c)

    def test_negacao_destacada_nao_alerta(self):
        mod = carregar("prof-questoes", "questoes.py")
        self.assertIsNone(mod.negacao_sem_destaque("Qual alternativa NÃO é verdadeira?"))
        self.assertIsNone(mod.negacao_sem_destaque("Qual **não** é verdadeira?"))
        self.assertEqual(mod.negacao_sem_destaque("Qual não é verdadeira?"), "não")

    def test_correta_invalida(self):
        mod = carregar("prof-questoes", "questoes.py")
        d = {"questoes": [{"enunciado": "x", "alternativas": ["a", "b", "c", "d"], "correta": "E"}]}
        self.assertIn("correta", {a["codigo"] for a in mod.checar(d)})

    def test_embaralhar_preserva_a_correta(self):
        mod = carregar("prof-questoes", "questoes.py")
        d = ler(ex("questoes_exemplo.json"))
        novo = mod.embaralhar(d, 7)
        for antes, depois in zip(d["questoes"], novo["questoes"]):
            ia = mod.indice_correta(antes)
            ib = mod.indice_correta(depois)
            self.assertEqual(antes["alternativas"][ia], depois["alternativas"][ib])
            self.assertEqual(sorted(antes["alternativas"]), sorted(depois["alternativas"]))
            self.assertEqual(antes["objetivo"] if "objetivo" in antes else None,
                             depois["objetivo"] if "objetivo" in depois else None)
        self.assertEqual(novo["gabarito"], [q["correta"] for q in novo["questoes"]])

    def test_embaralhar_deterministico_e_muda_com_a_semente(self):
        a = rodar("prof-questoes", "questoes.py", "embaralhar", ex("questoes_exemplo.json"), "--semente", "7")[1]
        b = rodar("prof-questoes", "questoes.py", "embaralhar", ex("questoes_exemplo.json"), "--semente", "7")[1]
        c = rodar("prof-questoes", "questoes.py", "embaralhar", ex("questoes_exemplo.json"), "--semente", "8")[1]
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_embaralhar_mantem_ordem_com_anteriores(self):
        mod = carregar("prof-questoes", "questoes.py")
        d = {"questoes": [{"enunciado": "x", "alternativas": ["a", "b", "c", "Todas as anteriores"], "correta": "D"}]}
        self.assertEqual(mod.embaralhar(d, 3)["questoes"][0]["alternativas"], d["questoes"][0]["alternativas"])

    def test_embaralhar_grava_arquivo(self):
        with tempfile.TemporaryDirectory() as t:
            saida = os.path.join(t, "b.json")
            rc, _, _ = rodar("prof-questoes", "questoes.py", "embaralhar", ex("questoes_exemplo.json"),
                             "--semente", "2", "-o", saida)
            self.assertEqual(rc, 0)
            self.assertEqual(ler(saida)["semente"], 2)

    def test_embaralhar_recusa_banco_com_erro(self):
        rc, _, err = rodar("prof-questoes", "questoes.py", "embaralhar", ex("questoes_com_problemas.json"))
        self.assertEqual(rc, 1)


class TestLegibilidade(unittest.TestCase):
    def test_simples_mais_facil_que_dificil(self):
        _, a, _ = rodar("prof-texto", "legibilidade.py", ex("texto_simples.txt"), "--json")
        _, b, _ = rodar("prof-texto", "legibilidade.py", ex("texto_dificil.txt"), "--json")
        a, b = json.loads(a), json.loads(b)
        self.assertGreater(a["indice"], b["indice"] + 50)
        self.assertEqual(a["faixa"], "muito fácil")
        self.assertEqual(b["faixa"], "muito difícil")

    def test_alvo_e_frases_longas(self):
        _, out, _ = rodar("prof-texto", "legibilidade.py", ex("texto_dificil.txt"), "--alvo", "fund2", "--json")
        d = json.loads(out)
        self.assertFalse(d["dentro_do_alvo"])
        self.assertEqual(len(d["frases_longas"]), 1)
        _, out, _ = rodar("prof-texto", "legibilidade.py", ex("texto_simples.txt"), "--alvo", "fund1", "--json")
        self.assertTrue(json.loads(out)["dentro_do_alvo"])

    def test_contagens_do_texto_simples(self):
        d = json.loads(rodar("prof-texto", "legibilidade.py", ex("texto_simples.txt"), "--json")[1])
        self.assertEqual(d["frases"], 9)
        self.assertEqual(d["palavras"], 63)

    def test_silabas(self):
        mod = carregar("prof-texto", "legibilidade.py")
        casos = {"casa": 2, "família": 3, "água": 2, "pão": 1, "país": 2, "leão": 2, "que": 1,
                 "queijo": 2, "saída": 3, "estudante": 4, "computador": 4, "arquivo": 3,
                 "extensão": 3, "dia": 2, "história": 3, "guarda-chuva": 4, "mãe": 1, "rio": 2}
        for palavra, esperado in casos.items():
            self.assertEqual(mod.silabas(palavra), esperado, palavra)

    def test_texto_vazio(self):
        with tempfile.TemporaryDirectory() as t:
            vazio = os.path.join(t, "v.txt")
            open(vazio, "w").close()
            rc, _, err = rodar("prof-texto", "legibilidade.py", vazio)
            self.assertEqual(rc, 2)
            self.assertIn("vazio", err)

    def test_blocos_separados_por_linha_em_branco(self):
        mod = carregar("prof-texto", "legibilidade.py")
        self.assertEqual(len(mod.dividir_frases("Título sem ponto\n\nUma frase. Outra frase.")), 3)


class TestEstrutura(unittest.TestCase):
    def test_cada_skill_tem_skill_md_com_nome_e_descricao(self):
        pasta = os.path.join(RAIZ, "skills")
        nomes = sorted(os.listdir(pasta))
        self.assertEqual(len(nomes), 7)
        for n in nomes:
            with open(os.path.join(pasta, n, "SKILL.md"), encoding="utf-8") as f:
                txt = f.read()
            self.assertTrue(txt.startswith("---\n"), n)
            self.assertIn(f"name: {n}\n", txt)
            self.assertIn("\ndescription: ", txt)

    def test_plugin_json_valido(self):
        for f in ("plugin.json", "marketplace.json"):
            ler(os.path.join(RAIZ, ".claude-plugin", f))


if __name__ == "__main__":
    unittest.main(verbosity=1)
