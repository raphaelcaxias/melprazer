"""Mel Prazer · clube de assinatura da Jardim do Éden Boutique Sensual.

Telas (escolhidas pelo endereço, ex.: .../?p=caixa):
  inicio  -> apresentação e planos
  quiz    -> perguntas de perfil e plano indicado
  caixa   -> página do QR Code da caixa: conteúdo do mês e avaliação dos itens
  favo    -> "Meu Favo": nível no clube, prêmios, indicação e pedido de pular o mês
  painel  -> área da Daiane (pede senha)
"""

from __future__ import annotations

import hashlib
import hmac
import os
from datetime import datetime
from urllib.parse import quote

import pandas as pd
import streamlit as st
from PIL import Image

import marca
import storage

PASTA = os.path.dirname(__file__)
st.set_page_config(
    page_title="Mel Prazer · Jardim do Éden",
    page_icon=Image.open(os.path.join(PASTA, "assets", "icone.png")),
    layout="centered",
)

# ---------------------------------------------------------------- dados fixos
PLANOS = {
    "leve": {"nome": "Mel Leve", "preco": 69.99, "vale": 70, "texto": "Cosméticos sensuais, gel e o desafio do mês."},
    "prazer": {"nome": "Mel Prazer", "preco": 99.99, "vale": 105, "texto": "Um acessório recarregável e cosméticos do tema."},
    "intenso": {"nome": "Mel Intenso", "preco": 159.99, "vale": 175, "texto": "Acessório premium e, a cada 2 meses, uma lingerie."},
    "ouro": {"nome": "Mel Ouro", "preco": 209.99, "vale": 230, "texto": "Lingerie da boutique todo mês, no seu tamanho."},
}
DESTAQUE = "prazer"


def segredo(secao: str, chave: str, padrao: str = "") -> str:
    try:
        return str(st.secrets.get(secao, {}).get(chave, padrao))
    except Exception:
        return padrao


def reais(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def so_digitos(texto: str) -> str:
    return "".join(c for c in texto if c.isdigit())


st.markdown(marca.css(), unsafe_allow_html=True)


# ---------------------------------------------------------------- pedaços de tela
def topo(titulo: str = "Mel Prazer", sub: str = "Uma caixa surpresa <em>todo mês</em>", simbolo: int = 64) -> None:
    st.markdown(
        f"""<div class="mp-topo">{marca.simbolo(simbolo)}
<div class="mp-mae">Jardim do Éden apresenta</div>
<div class="mp-titulo">{titulo}</div><div class="mp-sub">{sub}</div></div>""",
        unsafe_allow_html=True,
    )


def rodape() -> None:
    st.markdown(
        '<p class="mp-lema">Você pode perguntar. Aqui é normal.</p>'
        '<p class="mp-rodape">Mel Prazer é um clube da Jardim do Éden Boutique Sensual · Somente para maiores de 18 anos</p>',
        unsafe_allow_html=True,
    )


def ir(pagina: str) -> None:
    st.query_params.clear()
    if pagina != "inicio":
        st.query_params["p"] = pagina
    st.rerun()


def cartao_plano(chave: str, marcado: bool = False) -> None:
    p = PLANOS[chave]
    selo = '<span class="mp-selo">Mais escolhido</span><br>' if chave == DESTAQUE else ""
    st.markdown(
        f"""<div class="mp-plano {'on' if marcado else ''}">{selo}<span class="pn">{p['nome'].replace('Mel ', '')}</span>
<div class="pp">{reais(p['preco'])} <small>/mês</small></div>
<div class="vl">Vale cerca de {reais(p['vale'])} na loja</div>
<div class="tx">{p['texto']}</div></div>""",
        unsafe_allow_html=True,
    )


def contato_loja(texto: str = "Falar com a loja no WhatsApp", mensagem: str = "") -> None:
    numero = segredo("loja", "whatsapp")
    if numero:
        link = f"https://wa.me/55{so_digitos(numero).removeprefix('55')}"
        if mensagem:
            link += "?text=" + quote(mensagem)
        st.link_button(texto, link)
        st.caption(f"WhatsApp da loja: {numero}")


def niveis_html(caixas: int) -> str:
    partes = []
    for n in marca.NIVEIS:
        ok = "ok" if n["de"] <= caixas else ""
        partes.append(f'<div class="{ok}"><i></i>{n["nome"]}</div>')
    return f'<div class="mp-nivel">{"".join(partes)}</div>'


def caixas_recebidas(cliente_id: str) -> int:
    hist = storage.ler("historico")
    return int(hist[hist["cliente_id"] == cliente_id]["mes"].nunique())


def buscar_assinante(codigo: str) -> pd.Series | None:
    codigo = codigo.strip().upper()
    if not codigo:
        return None
    cad = storage.ler("cadastros")
    achou = cad[cad["codigo"].str.strip().str.upper() == codigo]
    if achou.empty:
        storage.ler.clear()
        cad = storage.ler("cadastros")
        achou = cad[cad["codigo"].str.strip().str.upper() == codigo]
    return None if achou.empty else achou.iloc[-1]


def gota_de_ouro(cliente_id: str, mes: str) -> bool:
    """Sorteio fixo: cerca de 1 em cada 5 caixas do mês leva um mimo extra."""
    return int(hashlib.sha256(f"{cliente_id}|{mes}".encode()).hexdigest(), 16) % 5 == 0


# ---------------------------------------------------------------- telas
def tela_inicio() -> None:
    topo(simbolo=76)
    st.write(
        "Oi, eu sou a Daiane. Todo mês monto uma caixa pensando em você, sem contar o que vem. "
        "Dentro dela tem um QR Code que abre um vídeo meu explicando cada item, do jeito que eu explicaria no balcão. "
        "Retire na loja ou receba em casa, sempre em embalagem discreta."
    )
    st.markdown(marca.secao("Como funciona"), unsafe_allow_html=True)
    st.markdown(
        """<div class="mp-passos">
<div class="mp-passo"><span class="mp-hex">1</span><div><b>Responda o quiz</b><span>Me conta do seu jeitinho. Leva um minuto e ninguém julga.</span></div></div>
<div class="mp-passo"><span class="mp-hex">2</span><div><b>Assine pelo Mercado Pago</b><span>Cartão, Pix ou boleto, no ambiente seguro do Mercado Pago. Quer sair? É só cancelar.</span></div></div>
<div class="mp-passo"><span class="mp-hex">3</span><div><b>Receba no dia 15</b><span>Abre a caixa, escaneia o QR e descobre cada surpresa comigo, no vídeo.</span></div></div>
</div>""",
        unsafe_allow_html=True,
    )
    st.markdown(marca.secao("Os planos"), unsafe_allow_html=True)
    for par in (("leve", "prazer"), ("intenso", "ouro")):
        for coluna, chave in zip(st.columns(2), par):
            with coluna:
                cartao_plano(chave, marcado=chave == DESTAQUE)
    st.write("")
    if st.button("Descobrir o meu plano", type="primary", width="stretch"):
        ir("quiz")

    st.markdown(marca.secao("Quanto mais tempo, mais mel"), unsafe_allow_html=True)
    st.markdown(
        '<div class="mp-cartao">' + niveis_html(0)
        + '<span style="color:#BBA79C;font-size:.9rem">Quanto mais caixas, mais o seu favo enche. Na 3ª, 6ª e 12ª tem presente. '
        "E todo mês, cerca de 1 em cada 5 caixas leva a <b>Gota de Ouro</b>, um mimo extra sorteado. "
        "Fidelidade aqui tem recompensa, e eu não esqueço de quem fica.</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown(marca.secao("Dúvidas"), unsafe_allow_html=True)
    with st.expander("O que todo mundo pergunta"):
        st.markdown(
            "- **Quando chega?** As vendas de cada tema vão do dia 15 ao dia 14. A caixa sai a partir do dia 15.\n"
            "- **A embalagem é discreta?** Sim, de verdade. Caixa e remetente neutros, sem nome de loja por fora. Só você sabe o que tem dentro.\n"
            "- **Posso pular um mês?** Pode, sem drama. Peça no Meu Favo ou no WhatsApp até o dia 10.\n"
            "- **E se eu não gostar de um item?** Acontece, e tudo bem. Avalie a caixa pelo QR. Eu uso a sua sinceridade para montar a próxima.\n"
            "- **Quem pode assinar?** Só maiores de 18 anos. Sem exceção e sem jeitinho."
        )
    if st.button("Já sou assinante, quero ver meu favo", width="stretch"):
        ir("favo")
    rodape()


def recomendar(r: dict) -> str:
    if r["lingerie"] == "Sim, todo mês":
        return "ouro"
    if r["ousadia"] == "Intensa" or (r["faixa_etaria"] in ("45 a 59", "60 ou mais") and r["ousadia"] != "Suave"):
        return "intenso"
    if r["ousadia"] == "Suave" and r["para_quem"] == "Só para mim":
        return "leve"
    return "prazer"


def tela_quiz() -> None:
    topo("Me conta de você", "Sem <em>julgamento</em>", simbolo=48)
    st.caption("Pode ser sincera. Eu só uso isso para acertar a sua caixa.")
    st.markdown(marca.secao("Sobre você"), unsafe_allow_html=True)
    with st.form("quiz"):
        nome = st.text_input("Seu nome", key="q_nome")
        whatsapp = st.text_input("WhatsApp com DDD", key="q_whats")
        email = st.text_input("E-mail (opcional)", key="q_email")
        cidade = st.text_input("Cidade", key="q_cidade")
        entrega = st.radio("Como prefere receber?", ["Retirar grátis na loja", "Receber em casa (frete à parte)"], key="q_entrega")
        para_quem = st.radio("Para quem é a caixa?", ["Só para mim", "Para o casal", "De presente"], horizontal=True, key="q_para")
        faixa = st.selectbox("Sua faixa de idade", ["18 a 24", "25 a 34", "35 a 44", "45 a 59", "60 ou mais"], key="q_faixa")
        ousadia = st.select_slider("Quanta ousadia?", ["Suave", "Picante", "Intensa"], value="Picante", key="q_ousadia")
        lingerie = st.radio("Quer lingerie na caixa?", ["Não", "De vez em quando", "Sim, todo mês"], horizontal=True, key="q_lingerie")
        tamanho = st.selectbox("Tamanho de lingerie", ["Não se aplica", "PP", "P", "M", "G", "GG", "EXG"], key="q_tamanho")
        restricoes = st.text_input("Alergias ou o que prefere evitar (ex.: fragrância, sabor)", key="q_restr")
        indicacao = st.text_input("Código de quem te indicou (opcional, ex.: MEL-7KQ2)", key="q_indic")
        maior = st.checkbox("Declaro que tenho 18 anos ou mais", key="q_18")
        lgpd = st.checkbox("Aceito que a loja guarde estes dados para montar e enviar minhas caixas", key="q_lgpd")
        enviado = st.form_submit_button("Ver meu plano", type="primary", width="stretch")

    if enviado:
        faltando = [n for n, v in (("nome", nome), ("WhatsApp", whatsapp)) if not v.strip()]
        indicacao = indicacao.strip().upper()
        if faltando:
            st.error(f"Falta preencher {' e '.join(faltando)} pra eu montar o seu plano.")
        elif not maior:
            st.error("Essa assinatura é só para maiores de 18 anos. Marca a declaração aí em cima e seguimos.")
        elif not lgpd:
            st.error("Preciso do seu aceite para guardar seus dados e montar a sua caixa. Sem ele, não consigo.")
        elif indicacao and buscar_assinante(indicacao) is None:
            st.error("Esse código de indicação não bateu aqui. Confere com quem te indicou, ou deixa em branco.")
        else:
            respostas = dict(
                nome=nome.strip(), whatsapp=whatsapp.strip(), email=email.strip(), cidade=cidade.strip(),
                entrega=entrega, para_quem=para_quem, faixa_etaria=faixa, ousadia=ousadia,
                lingerie=lingerie, tamanho=tamanho, restricoes=restricoes.strip(), indicado_por=indicacao,
            )
            respostas["plano_sugerido"] = recomendar(respostas)
            st.session_state["respostas"] = respostas
            ir("plano")
    if st.button("Voltar aos planos"):
        ir("inicio")


def tela_plano() -> None:
    r = st.session_state.get("respostas")
    if not r:
        ir("quiz")
        return
    sugerido = r["plano_sugerido"]
    primeiro_nome = r["nome"].split()[0]

    if st.session_state.get("salvo"):
        chave, codigo = st.session_state["salvo"]
        topo(f"Bem-vinda, {primeiro_nome}", "Falta só <em>um cliquinho</em>", simbolo=48)
        cartao_plano(chave, marcado=True)
        link = segredo("mercadopago", chave)
        if link:
            st.link_button(f"Assinar o {PLANOS[chave]['nome']} no Mercado Pago", link, type="primary", width="stretch")
            st.caption("O pagamento acontece no Mercado Pago, em ambiente seguro. Depois de pagar, me chama no WhatsApp que eu confirmo por lá.")
        else:
            st.warning("O link de pagamento deste plano ainda não foi configurado. Fale com a loja para assinar.")
        st.markdown(
            f"""<div class="mp-cartao mel"><div style="text-align:center;color:#BBA79C;font-size:.85rem">Seu código de assinante</div>
<div class="mp-codigo">{codigo}</div>
<div style="text-align:center;color:#BBA79C;font-size:.85rem">Guarde esse código com carinho. Ele abre o seu Favo, guarda as suas avaliações
e é a sua chave de indicação: quem assinar com ele ganha um mimo, e você também.</div></div>""",
            unsafe_allow_html=True,
        )
        contato_loja(mensagem=f"Oi! Acabei de assinar o {PLANOS[chave]['nome']}. Meu código é {codigo}.")
        return

    topo(f"Olá, {primeiro_nome}", f"Achei o seu <em>{PLANOS[sugerido]['nome']}</em>", simbolo=48)
    opcoes = list(PLANOS)
    escolha = st.radio(
        "Pensei em você ao indicar esse. Mas a escolha é sua:", opcoes, index=opcoes.index(sugerido),
        format_func=lambda c: f"{PLANOS[c]['nome']} · {reais(PLANOS[c]['preco'])}/mês" + ("  (indicado)" if c == sugerido else ""),
        key="escolha_plano",
    )
    cartao_plano(escolha, marcado=True)
    if st.button("Confirmar plano", type="primary", width="stretch"):
        existentes = set(storage.ler("cadastros")["codigo"])
        codigo = storage.novo_codigo(existentes)
        storage.adicionar("cadastros", {
            "id": storage.novo_id(), "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            **{k: v for k, v in r.items() if k != "lingerie"},
            "restricoes": f"{r['restricoes']} | lingerie: {r['lingerie']}".strip(" |"),
            "plano": escolha, "status": "aguardando pagamento", "observacoes": "",
            "codigo": codigo, "pedido": "",
        })
        st.session_state["salvo"] = (escolha, codigo)
        st.rerun()


def tela_caixa() -> None:
    topo("Sua caixa", "Abre com <em>carinho</em>", simbolo=48)
    codigo = st.text_input("Código do mês impresso no cartão da caixa", key="codigo").strip().upper()
    if not codigo:
        st.caption("Achou o cartão? O código impresso nele libera o vídeo e o guia do mês.")
        return
    meses = storage.ler("meses")
    achado = meses[meses["codigo"].str.strip().str.upper() == codigo]
    if achado.empty:  # o mês pode ter acabado de ser cadastrado: busca de novo, sem cache
        storage.ler.clear()
        meses = storage.ler("meses")
        achado = meses[meses["codigo"].str.strip().str.upper() == codigo]
    if achado.empty:
        st.error("Não encontramos esse código. Confira as letras e os números do cartão.")
        contato_loja()
        return
    m = achado.iloc[-1]
    st.subheader(f"{m['mes']}: {m['tema']}")
    if m["video_url"].strip():
        st.video(m["video_url"].strip())
    itens = [i.strip() for i in m["itens"].replace(";", "\n").splitlines() if i.strip()]
    if itens:
        st.markdown("**O que veio pra você**")
        st.markdown("\n".join(f"- {i}" for i in itens))
    if m["guia"].strip():
        with st.expander("Guia do mês: modo de uso e cuidados", expanded=True):
            st.markdown(m["guia"])
    if m["proximo_tema"].strip():
        st.markdown(f'<div class="mp-spoiler">Spoiler do próximo mês: <b>{m["proximo_tema"]}</b></div>', unsafe_allow_html=True)

    if itens:
        st.markdown(marca.secao("Me conta: o que ficou?"), unsafe_allow_html=True)
        st.caption("Seja sincera: o que você amou e o que foi pro fundo da gaveta? Leva 30 segundos, e a próxima caixa já sai melhor por causa disso.")
        avaliar(m["mes"], itens)
    st.markdown("**Apaixonou por algum item?** Assinante tem preço especial na loja. É só chamar.")
    contato_loja()
    if st.button("Abrir o Meu Favo", width="stretch"):
        ir("favo")


def avaliar(mes: str, itens: list[str]) -> None:
    if st.session_state.get(f"avaliou_{mes}"):
        st.success("Recebido, obrigada! Sua opinião já entrou na montagem da próxima caixa. 💛")
        return
    with st.form(f"avaliacao_{mes}"):
        meu_codigo = st.text_input("Seu código de assinante (ex.: MEL-7KQ2)", key="av_codigo")
        notas = {}
        for i, item in enumerate(itens):
            notas[item] = st.radio(item, storage.NOTAS, index=None, horizontal=True, key=f"av_{i}")
        comentario = st.text_area("Quer contar mais alguma coisa? (opcional)", key="av_coment")
        enviar = st.form_submit_button("Enviar avaliação", type="primary", width="stretch")
    if not enviar:
        return
    cliente = buscar_assinante(meu_codigo)
    if cliente is None:
        st.error("Não encontramos esse código de assinante. Ele está no cartão da sua primeira caixa e no seu WhatsApp.")
        return
    respondidas = {k: v for k, v in notas.items() if v}
    if not respondidas:
        st.error("Marque pelo menos um item.")
        return
    av = storage.ler("avaliacoes")
    if not av[(av["cliente_id"] == cliente["id"]) & (av["mes"] == mes)].empty:
        st.info("Você já avaliou a caixa deste mês. Obrigada!")
        st.session_state[f"avaliou_{mes}"] = True
        return
    for item, nota in respondidas.items():
        storage.adicionar("avaliacoes", {
            "data": datetime.now().strftime("%d/%m/%Y"), "cliente_id": cliente["id"], "nome": cliente["nome"],
            "mes": mes, "item": item, "nota": nota, "comentario": comentario.strip(),
        })
    st.session_state[f"avaliou_{mes}"] = True
    st.rerun()


def tela_favo() -> None:
    topo("Meu Favo", "Seu cantinho <em>no clube</em>", simbolo=56)
    codigo = st.text_input("Seu código de assinante (ex.: MEL-7KQ2)", key="favo_codigo")
    if not codigo.strip():
        st.caption("Seu código está no cartão da primeira caixa e na mensagem de boas-vindas no WhatsApp. Sem ele, o seu favo fica trancado.")
        rodape()
        return
    c = buscar_assinante(codigo)
    if c is None:
        st.error("Não encontramos esse código. Confira as letras e os números.")
        contato_loja()
        return

    caixas = caixas_recebidas(c["id"])
    atual, proximo = marca.nivel(caixas)
    st.markdown(f"### Oi, {c['nome'].split()[0]}! Que bom ter você por aqui.")
    if c["status"] != "ativa":
        st.info(f"Situação da assinatura: {c['status']}.")
    progresso = ""
    if proximo:
        falta = proximo["de"] - caixas
        feito = (caixas - atual["de"]) / max(1, proximo["de"] - atual["de"])
        progresso = (f'<div class="mp-barra"><b style="width:{max(6, int(feito * 100))}%"></b></div>'
                     f'<span style="color:#BBA79C;font-size:.88rem">Falta{"m" if falta > 1 else ""} {falta} caixa{"s" if falta > 1 else ""} '
                     f'para o nível <b style="color:#F2D59A">{proximo["nome"]}</b>. {proximo["premio"]}</span>')
    st.markdown(
        f"""<div class="mp-cartao mel"><div style="display:flex;justify-content:space-between;align-items:baseline;gap:8px;flex-wrap:wrap">
<span style="font-family:'Cinzel',serif;font-size:1.3rem;color:#E0A93B">Nível {atual['nome']}</span>
<span style="color:#BBA79C;font-size:.85rem">{caixas} caixa{'s' if caixas != 1 else ''} recebida{'s' if caixas != 1 else ''}</span></div>
{niveis_html(caixas)}{progresso}</div>""",
        unsafe_allow_html=True,
    )

    cad = storage.ler("cadastros")
    indicadas = cad[(cad["indicado_por"].str.upper() == c["codigo"].upper()) & (cad["status"] == "ativa")]
    url_app = segredo("loja", "url")
    convite = f"Assinei o Mel Prazer e estou amando! Use meu código {c['codigo']} e ganha um mimo na sua primeira caixa. Bora?"
    if url_app:
        convite += f" {url_app}"
    st.markdown(
        f"""<div class="mp-cartao"><b style="color:#F5ECE3">Conhece alguém curioso? Indique</b>
<div class="mp-codigo">{c['codigo']}</div>
<span style="color:#BBA79C;font-size:.88rem">Quem assinar com o seu código ganha um mimo na primeira caixa, e você ganha outro. Curiosidade compartilhada é melhor.
Indicações ativas: <b style="color:#F2D59A">{len(indicadas)}</b></span></div>""",
        unsafe_allow_html=True,
    )
    st.link_button("Enviar convite pelo WhatsApp", "https://wa.me/?text=" + quote(convite), width="stretch")

    st.markdown(marca.secao("Precisa de uma pausa?"), unsafe_allow_html=True)
    if c["pedido"] == "pular o próximo mês":
        st.success("Seu pedido para pular o próximo mês já está com a loja. Sem drama, a gente cuida do resto.")
    elif st.button("Pular o próximo mês", width="stretch"):
        cad = storage.ler("cadastros")
        cad.loc[cad["id"] == c["id"], "pedido"] = "pular o próximo mês"
        storage.salvar("cadastros", cad)
        st.rerun()
    st.caption("Pedidos até o dia 10 valem para a caixa do dia 15. Quer cancelar? Sem drama: fala com a loja.")
    contato_loja("Falar com a loja", f"Oi! Sou assinante do Mel Prazer, meu código é {c['codigo']}.")


def tela_painel() -> None:
    topo("Painel", "Só para a <em>Daiane</em>", simbolo=48)
    senha_certa = segredo("painel", "senha")
    if not senha_certa:
        st.error("Configure a senha do painel nos segredos do app (seção [painel]).")
        return
    if not st.session_state.get("logada"):
        senha = st.text_input("Senha", type="password", key="senha")
        if st.button("Entrar", type="primary"):
            if hmac.compare_digest(senha, senha_certa):
                st.session_state["logada"] = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
        return

    st.caption(f"Dados em: {storage.modo()}")
    cad = storage.ler("cadastros")
    hist = storage.ler("historico")
    ativas = cad[cad["status"] == "ativa"]
    receita = sum(PLANOS.get(p, {}).get("preco", 0) for p in ativas["plano"])
    pedidos = cad[cad["pedido"].isin(["pular o próximo mês", "voltar a receber"])]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ativas", len(ativas))
    c2.metric("Receita/mês", reais(receita))
    c3.metric("Aguardando", int((cad["status"] == "aguardando pagamento").sum()))
    c4.metric("Pedidos", len(pedidos))
    if len(pedidos):
        st.warning("Pedidos para resolver: " + ", ".join(f"{r['nome']} ({r['pedido']})" for _, r in pedidos.iterrows()))

    aba1, aba2, aba3, aba4, aba5 = st.tabs(["Assinantes", "Lista de envio", "Meses", "Histórico", "Avaliações"])

    with aba1:
        st.caption("Mude o status quando o pagamento cair, quando ela pular o mês ou cancelar. Marque o pedido como resolvido depois de ajustar no Mercado Pago.")
        editado = st.data_editor(
            cad, key="ed_cad", hide_index=True, width="stretch",
            disabled=[c for c in cad.columns if c not in ("status", "plano", "observacoes", "pedido")],
            column_config={
                "status": st.column_config.SelectboxColumn("status", options=storage.STATUS, required=True),
                "plano": st.column_config.SelectboxColumn("plano", options=list(PLANOS), required=True),
                "pedido": st.column_config.SelectboxColumn("pedido", options=storage.PEDIDOS),
            },
        )
        if st.button("Salvar alterações", type="primary", key="salvar_cad"):
            storage.salvar("cadastros", editado)
            st.success("Alterações salvas.")
            st.rerun()

    with aba2:
        mes_envio = datetime.now().strftime("%Y-%m")
        lista = ativas[["id", "nome", "codigo", "whatsapp", "cidade", "entrega", "plano", "tamanho", "restricoes", "indicado_por"]].copy()
        lista = lista[~lista["id"].isin(cad[cad["pedido"] == "pular o próximo mês"]["id"])]
        contagem = hist.groupby("cliente_id")["mes"].nunique()
        lista["caixa_nº"] = [int(contagem.get(i, 0)) + 1 for i in lista["id"]]
        lista["extra"] = [
            ", ".join(x for x in (
                "prêmio de nível" if n in (3, 6, 12) else "",
                "gota de ouro" if gota_de_ouro(i, mes_envio) else "",
                "mimo de indicação" if n == 1 and ind else "",
            ) if x)
            for i, n, ind in zip(lista["id"], lista["caixa_nº"], lista["indicado_por"])
        ]
        lista = lista.drop(columns=["id"]).sort_values(["entrega", "plano"])
        st.write(f"{len(lista)} caixa{'s' if len(lista) != 1 else ''} para montar")
        st.caption("A coluna extra diz quais caixas levam presente: prêmio de nível (3ª, 6ª e 12ª caixa), Gota de Ouro (sorteio) e mimo de indicação.")
        resumo = lista.groupby("plano").size().rename("caixas").reset_index()
        st.dataframe(resumo, hide_index=True)
        st.dataframe(lista, hide_index=True, width="stretch")
        st.download_button("Baixar lista de envio (CSV)", lista.to_csv(index=False).encode("utf-8-sig"),
                           file_name=f"envio_{mes_envio}.csv", mime="text/csv")

    with aba3:
        st.caption("Uma linha por mês. O código vai impresso no cartão da caixa; use itens separados por ponto e vírgula.")
        meses = storage.ler("meses")
        meses_ed = st.data_editor(meses, key="ed_meses", hide_index=True, num_rows="dynamic", width="stretch")
        if st.button("Salvar meses", type="primary", key="salvar_meses"):
            storage.salvar("meses", meses_ed)
            st.success("Meses salvos.")
            st.rerun()

    with aba4:
        st.caption("Registre o que cada plano recebeu no mês. O painel avisa se algum item se repete para a mesma cliente.")
        with st.form("registrar"):
            mes = st.text_input("Mês (ex.: Dezembro 2026)", key="h_mes")
            plano = st.selectbox("Plano", list(PLANOS), format_func=lambda c: PLANOS[c]["nome"], key="h_plano")
            itens = st.text_area("Itens enviados (um por linha)", key="h_itens")
            ok = st.form_submit_button("Registrar para todas as ativas deste plano")
        if ok and mes.strip() and itens.strip():
            novos = [i.strip().lower() for i in itens.splitlines() if i.strip()]
            alvo = ativas[ativas["plano"] == plano]
            repetidos = []
            for _, c in alvo.iterrows():
                anteriores = " ".join(hist[hist["cliente_id"] == c["id"]]["itens"]).lower()
                repetidos += [f"{c['nome']}: {i}" for i in novos if i in anteriores]
                storage.adicionar("historico", {
                    "data": datetime.now().strftime("%d/%m/%Y"), "cliente_id": c["id"], "nome": c["nome"],
                    "mes": mes.strip(), "plano": plano, "itens": "; ".join(novos),
                })
            st.success(f"Registrado para {len(alvo)} assinantes.")
            if repetidos:
                st.warning("Itens repetidos para estas clientes:\n\n" + "\n".join(f"- {r}" for r in repetidos))
        st.dataframe(storage.ler("historico"), hide_index=True, width="stretch")

    with aba5:
        av = storage.ler("avaliacoes")
        if av.empty:
            st.caption("Ainda sem avaliações. Assim que a primeira caixa chegar e alguém avaliar pelo QR, elas aparecem aqui.")
        else:
            st.caption("Itens com muito 'Não é pra mim' saem da lista de compra. Os com 'Amei' podem virar venda na loja.")
            tabela = av.pivot_table(index=["mes", "item"], columns="nota", values="cliente_id", aggfunc="count", fill_value=0)
            tabela = tabela.reindex(columns=storage.NOTAS, fill_value=0).reset_index()
            st.dataframe(tabela, hide_index=True, width="stretch")
            comentarios = av[av["comentario"].str.strip() != ""].drop_duplicates(["cliente_id", "mes"])
            for _, r in comentarios.iterrows():
                st.markdown(f"> {r['comentario']}\n\n— {r['nome']}, {r['mes']}")

    if st.button("Sair"):
        st.session_state["logada"] = False
        st.rerun()


# ---------------------------------------------------------------- roteamento
TELAS = {"inicio": tela_inicio, "quiz": tela_quiz, "plano": tela_plano, "caixa": tela_caixa,
         "favo": tela_favo, "painel": tela_painel}
pagina = st.query_params.get("p", "inicio")
TELAS.get(pagina, tela_inicio)()
