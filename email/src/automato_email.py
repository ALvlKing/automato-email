from __future__ import annotations

import sys
from typing import Dict, Set, Tuple

# 1. Definicao explicita da 5-tupla do AFD: M = (Q, Sigma, delta, q0, F)
ESTADOS: Set[str] = {
    "q0",      # Inicial: nada lido ainda
    "q1",      # Usuario valido (ultimo char nao foi '.')
    "q2",      # Usuario apos '.' (exige char valido != '.' e != '@')
    "q3",      # Logo apos '@': inicio do 1o rotulo do dominio
    "q4",      # Dentro do 1o rotulo do dominio (alfanumerico)
    "q5",      # Logo apos '.' no dominio: inicio de proximo rotulo
    "q6",      # Rotulo apos '.': 1 letra minuscula lida
    "q7",      # Rotulo apos '.': 2 letras minusculas lidas (FINAL)
    "q8",      # Rotulo apos '.': 3 letras minusculas lidas (FINAL)
    "q9",      # Rotulo apos '.' com >=4 chars ou digitos (nao final no momento)
    "q_erro",  # Estado poco (absorvente)
}

LETRAS: Set[str] = set("abcdefghijklmnopqrstuvwxyz")
DIGITOS: Set[str] = set("0123456789")
ALFABETO: Set[str] = LETRAS | DIGITOS | {".", "_", "@"}

ESTADO_INICIAL: str = "q0"
ESTADOS_FINAIS: Set[str] = {"q7", "q8"}
ESTADO_POCO: str = "q_erro"


def classificar_simbolo(ch: str) -> str:
    """Classifica um unico caractere em uma categoria do alfabeto."""
    if ch in LETRAS:
        return "LETRA"
    if ch in DIGITOS:
        return "DIGITO"
    if ch == "_":
        return "UNDER"
    if ch == ".":
        return "PONTO"
    if ch == "@":
        return "ARROBA"
    return "INVALIDO"


# Tabela de transicao delta: estado -> categoria_do_simbolo -> proximo_estado
TRANSICOES: Dict[str, Dict[str, str]] = {
    "q0": {
        "LETRA": "q1",
        "DIGITO": "q1",
        "UNDER": "q1",
        "PONTO": "q_erro",
        "ARROBA": "q_erro",
        "INVALIDO": "q_erro",
    },
    "q1": {
        "LETRA": "q1",
        "DIGITO": "q1",
        "UNDER": "q1",
        "PONTO": "q2",
        "ARROBA": "q3",
        "INVALIDO": "q_erro",
    },
    "q2": {
        "LETRA": "q1",
        "DIGITO": "q1",
        "UNDER": "q1",
        "PONTO": "q_erro",
        "ARROBA": "q_erro",
        "INVALIDO": "q_erro",
    },
    "q3": {
        "LETRA": "q4",
        "DIGITO": "q4",
        "UNDER": "q_erro",
        "PONTO": "q_erro",
        "ARROBA": "q_erro",
        "INVALIDO": "q_erro",
    },
    "q4": {
        "LETRA": "q4",
        "DIGITO": "q4",
        "UNDER": "q_erro",
        "PONTO": "q5",
        "ARROBA": "q_erro",
        "INVALIDO": "q_erro",
    },
    "q5": {
        "LETRA": "q6",
        "DIGITO": "q9",
        "UNDER": "q_erro",
        "PONTO": "q_erro",
        "ARROBA": "q_erro",
        "INVALIDO": "q_erro",
    },
    "q6": {
        "LETRA": "q7",
        "DIGITO": "q9",
        "UNDER": "q_erro",
        "PONTO": "q5",
        "ARROBA": "q_erro",
        "INVALIDO": "q_erro",
    },
    "q7": {
        "LETRA": "q8",
        "DIGITO": "q9",
        "UNDER": "q_erro",
        "PONTO": "q5",
        "ARROBA": "q_erro",
        "INVALIDO": "q_erro",
    },
    "q8": {
        "LETRA": "q9",
        "DIGITO": "q9",
        "UNDER": "q_erro",
        "PONTO": "q5",
        "ARROBA": "q_erro",
        "INVALIDO": "q_erro",
    },
    "q9": {
        "LETRA": "q9",
        "DIGITO": "q9",
        "UNDER": "q_erro",
        "PONTO": "q5",
        "ARROBA": "q_erro",
        "INVALIDO": "q_erro",
    },
    "q_erro": {
        "LETRA": "q_erro",
        "DIGITO": "q_erro",
        "UNDER": "q_erro",
        "PONTO": "q_erro",
        "ARROBA": "q_erro",
        "INVALIDO": "q_erro",
    },
}


def executar_automato(palavra: str) -> Tuple[bool, list[str]]:
    """
    Executa o AFD simbolo por simbolo sobre 'palavra'.
    Retorna (aceita, caminho_de_estados).
    """
    estado_atual = ESTADO_INICIAL
    caminho = [estado_atual]

    for ch in palavra:
        categoria = classificar_simbolo(ch)
        proximo_estado = TRANSICOES[estado_atual].get(categoria, ESTADO_POCO)
        estado_atual = proximo_estado
        caminho.append(estado_atual)

    aceita = estado_atual in ESTADOS_FINAIS
    return aceita, caminho


def formatar_resultado(palavra: str) -> str:
    aceita, caminho = executar_automato(palavra)
    status = "aceita" if aceita else "rejeita"
    trilha = " -> ".join(caminho)
    return f"'{palavra}' => {status} | caminho: {trilha}"


def main() -> None:
    # Se receber argumentos na linha de comando, avalia cada um;
    # caso contrario, le e-mails linha a linha da entrada padrao (stdin).
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            print(formatar_resultado(arg))
        return

    for linha in sys.stdin:
        palavra = linha.rstrip("\r\n")
        print(formatar_resultado(palavra))


if __name__ == "__main__":
    main()
