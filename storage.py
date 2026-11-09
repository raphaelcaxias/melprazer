"""Armazenamento do Mel Prazer.

Usa uma planilha Google quando os segredos estão configurados no Streamlit.
Sem segredos, grava em arquivos CSV na pasta data/ (bom para testar no computador).
"""

from __future__ import annotations

import os
import secrets
from datetime import datetime

import pandas as pd
import streamlit as st

# Abas da planilha e suas colunas, na ordem em que aparecem.
TABELAS = {
    "cadastros": [
        "id", "data", "nome", "whatsapp", "email", "cidade", "entrega",
        "para_quem", "faixa_etaria", "ousadia", "tamanho", "restricoes",
        "plano_sugerido", "plano", "status", "observacoes",
        "codigo", "indicado_por", "pedido",
    ],
    "meses": ["mes", "tema", "codigo", "video_url", "itens", "guia", "proximo_tema"],
    "historico": ["data", "cliente_id", "nome", "mes", "plano", "itens"],
    "avaliacoes": ["data", "cliente_id", "nome", "mes", "item", "nota", "comentario"],
}

STATUS = ["aguardando pagamento", "ativa", "pulou o mês", "cancelada"]
PEDIDOS = ["", "pular o próximo mês", "voltar a receber", "resolvido"]
NOTAS = ["Amei", "Gostei", "Não é pra mim"]

PASTA_LOCAL = os.path.join(os.path.dirname(__file__), "data")


def _usa_planilha() -> bool:
    try:
        return "gcp_service_account" in st.secrets and "planilha" in st.secrets
    except Exception:  # sem arquivo de segredos
        return False


@st.cache_resource(show_spinner=False)
def _planilha():
    import gspread

    cliente = gspread.service_account_from_dict(dict(st.secrets["gcp_service_account"]))
    return cliente.open_by_key(st.secrets["planilha"]["id"])


@st.cache_resource(show_spinner=False)
def _aba(nome: str):
    import gspread

    planilha = _planilha()
    try:
        aba = planilha.worksheet(nome)
    except gspread.WorksheetNotFound:
        aba = planilha.add_worksheet(title=nome, rows=1000, cols=len(TABELAS[nome]))
        aba.append_row(TABELAS[nome])
        return aba
    # Planilha criada por uma versão anterior do app: acrescenta as colunas novas no fim.
    cabecalho = aba.row_values(1)
    if cabecalho != TABELAS[nome] and TABELAS[nome][: len(cabecalho)] == cabecalho:
        aba.update([TABELAS[nome]], "A1", value_input_option="RAW")
    return aba


def _arquivo(nome: str) -> str:
    os.makedirs(PASTA_LOCAL, exist_ok=True)
    caminho = os.path.join(PASTA_LOCAL, f"{nome}.csv")
    if not os.path.exists(caminho):
        pd.DataFrame(columns=TABELAS[nome]).to_csv(caminho, index=False)
    return caminho


@st.cache_data(ttl=60, show_spinner=False)
def ler(nome: str) -> pd.DataFrame:
    """Lê uma aba inteira. Fica em cache por 60 s para não estourar a cota do Google."""
    if _usa_planilha():
        # get_all_values devolve tudo como texto (não transforma "0123" em 123).
        valores = _aba(nome).get_all_values()
        cabecalho, linhas = (valores[0], valores[1:]) if valores else (TABELAS[nome], [])
        df = pd.DataFrame(linhas, columns=cabecalho)
    else:
        df = pd.read_csv(_arquivo(nome), dtype=str, keep_default_na=False)
    for coluna in TABELAS[nome]:
        if coluna not in df.columns:
            df[coluna] = ""
    return df[TABELAS[nome]].astype(str)


def adicionar(nome: str, linha: dict) -> None:
    valores = [str(linha.get(c, "")) for c in TABELAS[nome]]
    if _usa_planilha():
        _aba(nome).append_row(valores, value_input_option="RAW")
    else:
        df = pd.read_csv(_arquivo(nome), dtype=str, keep_default_na=False)
        df = pd.concat([df, pd.DataFrame([dict(zip(TABELAS[nome], valores))])], ignore_index=True)
        df.to_csv(_arquivo(nome), index=False)
    ler.clear()


def salvar(nome: str, df: pd.DataFrame) -> None:
    """Regrava a aba inteira (usado pelo painel ao editar status e observações)."""
    df = df[TABELAS[nome]].fillna("").astype(str)
    if _usa_planilha():
        aba = _aba(nome)
        aba.clear()
        aba.update([TABELAS[nome]] + df.values.tolist(), value_input_option="RAW")
    else:
        df.to_csv(_arquivo(nome), index=False)
    ler.clear()


def novo_id() -> str:
    return datetime.now().strftime("MP%y%m%d%H%M%S") + secrets.token_hex(2)


def novo_codigo(existentes: set[str]) -> str:
    """Código pessoal da assinante, ex.: MEL-7KQ2. Sem letras que confundem (O/0, I/1)."""
    letras = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    while True:
        codigo = "MEL-" + "".join(secrets.choice(letras) for _ in range(4))
        if codigo not in existentes:
            return codigo


def modo() -> str:
    return "Planilha Google" if _usa_planilha() else "Arquivos locais (teste)"
