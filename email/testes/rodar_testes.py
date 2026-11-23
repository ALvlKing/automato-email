from __future__ import annotations

import os
import sys
from typing import List, Tuple

if "__file__" in globals():
    _PASTA_TESTES = os.path.dirname(os.path.abspath(__file__))
    RAIZ_PROJETO = os.path.dirname(_PASTA_TESTES)
else:
    _cwd = os.path.abspath(os.getcwd())
    RAIZ_PROJETO = os.path.dirname(_cwd) if os.path.basename(_cwd) == "testes" else _cwd

_SRC_DIR = os.path.join(RAIZ_PROJETO, "src")
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from automato_email import executar_automato  # noqa: E402

# Palavras obrigatorias do Tema 6 (anexo do PDF)
CASOS_OBRIGATORIOS: List[Tuple[str, bool]] = [
    ("aluno@uni.edu.br", True),
    ("joao.silva_2@mail.com", True),
    ("j@a.io", True),
    (".joao@mail.com", False),
    ("joao..silva@mail.com", False),
    ("joao@mail", False),
    ("joao@@mail.com", False),
    ("joao@mail.c", False),
    ("joao@mail.coml", False),
]

# 20 palavras proprias: 10 aceitas e 10 rejeitadas (incluindo bordas e palavra vazia)
CASOS_PROPRIOS: List[Tuple[str, bool]] = [
    # 10 aceitas
    ("a@b.io", True),
    ("a@b.com", True),
    ("_@a.br", True),
    ("user_@a.org", True),
    ("___@1.net", True),
    ("123@456.io", True),
    ("a.b.c@d.e.f.br", True),
    ("x@m1.m2.co", True),
    ("nome.sobrenome@sub.dom.uk", True),
    ("u1_u2.u3@ab.cd.com", True),

    # 10 rejeitadas (bordas)
    ("", False),
    ("@a.com", False),
    ("user@", False),
    ("user@.", False),
    ("user@.com", False),
    ("user@com.", False),
    ("user.@mail.com", False),
    ("User@mail.com", False),
    ("user@mail.c1", False),
    ("user@mail.com!x", False),
]


def rodar() -> int:
    todos = [("OBRIGATORIO", p, esp) for p, esp in CASOS_OBRIGATORIOS] + [
        ("PROPRIO", p, esp) for p, esp in CASOS_PROPRIOS
    ]

    falhas = 0
    for origem, palavra, esperado in todos:
        obtido, caminho = executar_automato(palavra)
        bateu = obtido == esperado
        if not bateu:
            falhas += 1

        esp_txt = "aceita" if esperado else "rejeita"
        obt_txt = "aceita" if obtido else "rejeita"
        ok_txt = "SIM" if bateu else "NAO"
        trilha = " -> ".join(caminho)
        print(
            f"[{origem}] palavra={palavra!r} | esperado={esp_txt} | "
            f"obtido={obt_txt} | bateu={ok_txt} | caminho={trilha}"
        )

    print(f"\nTotal: {len(todos)} | Falhas: {falhas}")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(rodar())
