"""Identidade visual do Mel Prazer: símbolo, cores, letras e padrão de favo.

O símbolo é um favo (hexágono) com uma gota de mel que escorre e vira coração.
Tudo aqui é original do Mel Prazer; a marca-mãe é a Jardim do Éden Boutique Sensual.
"""

# ---------------------------------------------------------------- cores
CORES = {
    "noite": "#0D0708",     # fundo
    "vinho": "#22090E",     # superfícies
    "vinho_2": "#35101A",   # cartões em destaque
    "linha": "#5A2A2F",     # bordas
    "mel": "#E0A93B",       # cor principal: mel dourado
    "mel_claro": "#F2D59A", # textos dourados
    "batom": "#D81B35",     # acento: palavras em cursiva vermelha
    "creme": "#F5ECE3",     # texto
    "suave": "#BBA79C",     # texto secundário
    "folha": "#7FC8A0",     # economia / valor
}

# ---------------------------------------------------------------- símbolo
def simbolo(tamanho: int = 64, contorno: str = CORES["mel"], gota: str = CORES["mel"]) -> str:
    """Favo com gota de mel que escorre e vira coração."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="{tamanho}" height="{tamanho}" role="img" aria-label="Mel Prazer">
<defs><linearGradient id="mp-mel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6CF77"/><stop offset="1" stop-color="{gota}"/></linearGradient></defs>
<path d="M32 4 L56.2 18 V46 L32 60 L7.8 46 V18 Z" fill="none" stroke="{contorno}" stroke-width="2.6" stroke-linejoin="round"/>
<path d="M26.4 8.6 L32 5.4 L37.6 8.6 C37.6 12.6 34.4 14 34.4 18 C34.4 20.2 33.3 21.6 32 21.6 C30.7 21.6 29.6 20.2 29.6 18 C29.6 14 26.4 12.6 26.4 8.6 Z" fill="url(#mp-mel)"/>
<path d="M32 49 C21.5 42 18.2 36 21.6 31.4 C24.6 27.6 29.6 28.4 32 32.2 C34.4 28.4 39.4 27.6 42.4 31.4 C45.8 36 42.5 42 32 49 Z" fill="url(#mp-mel)"/>
<circle cx="32" cy="25.4" r="1.5" fill="{gota}"/>
</svg>"""


def favo_fundo(cor: str = CORES["mel"], opacidade: float = 0.06) -> str:
    """Padrão de favos para o fundo, como data URI para usar no CSS."""
    from urllib.parse import quote

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="56" height="97" viewBox="0 0 56 97">'
        f'<g fill="none" stroke="{cor}" stroke-opacity="{opacidade}" stroke-width="1.2">'
        f'<path d="M28 0 L56 16 V48 L28 64 L0 48 V16 Z"/><path d="M28 64 V97 M0 48 L0 81 L-28 97 M56 48 V81 L84 97"/>'
        f'<path d="M0 81 L28 97 L56 81"/></g></svg>'
    )
    return "data:image/svg+xml;utf8," + quote(svg)


# ---------------------------------------------------------------- níveis do clube
# Contados pelo número de caixas recebidas (aba histórico).
NIVEIS = [
    {"nome": "Gota", "de": 0, "ate": 2, "premio": "Boas-vindas: a primeira caixa é a mais caprichada do ano."},
    {"nome": "Favo", "de": 3, "ate": 5, "premio": "Na 3ª caixa: um mimo surpresa, porque você já é da casa."},
    {"nome": "Colmeia", "de": 6, "ate": 11, "premio": "Na 6ª caixa: um acessório a mais e 10% na loja. Você merece."},
    {"nome": "Rainha", "de": 12, "ate": 10_000, "premio": "Na 12ª caixa: a Caixa Rainha, feita só para você."},
]


def nivel(caixas: int) -> tuple[dict, dict | None]:
    atual = next(n for n in NIVEIS if n["de"] <= caixas <= n["ate"])
    i = NIVEIS.index(atual)
    proximo = NIVEIS[i + 1] if i + 1 < len(NIVEIS) else None
    return atual, proximo


# ---------------------------------------------------------------- CSS
def css() -> str:
    c = CORES
    return f"""
<style>
@font-face {{ font-family:'Great Vibes'; src:url('app/static/fonts/great-vibes-latin-400-normal.woff2') format('woff2'); font-display:swap; }}
@font-face {{ font-family:'Cinzel'; font-weight:500; src:url('app/static/fonts/cinzel-latin-500-normal.woff2') format('woff2'); font-display:swap; }}
@font-face {{ font-family:'Cinzel'; font-weight:600; src:url('app/static/fonts/cinzel-latin-600-normal.woff2') format('woff2'); font-display:swap; }}
@font-face {{ font-family:'Montserrat'; font-weight:400; src:url('app/static/fonts/montserrat-latin-400-normal.woff2') format('woff2'); font-display:swap; }}
@font-face {{ font-family:'Montserrat'; font-weight:500; src:url('app/static/fonts/montserrat-latin-500-normal.woff2') format('woff2'); font-display:swap; }}
@font-face {{ font-family:'Montserrat'; font-weight:600; src:url('app/static/fonts/montserrat-latin-600-normal.woff2') format('woff2'); font-display:swap; }}
@font-face {{ font-family:'Montserrat'; font-weight:700; src:url('app/static/fonts/montserrat-latin-700-normal.woff2') format('woff2'); font-display:swap; }}

[data-testid="stApp"] {{
  background-color:{c['noite']};
  background-image: radial-gradient(90% 50% at 85% 0%, rgba(216,27,53,.14), transparent 60%),
                    radial-gradient(80% 40% at 0% 100%, rgba(224,169,59,.08), transparent 60%),
                    url("{favo_fundo()}");
  background-attachment: fixed, fixed, scroll;
}}
[data-testid="stHeader"] {{ background: transparent; }}
html, body, .stMarkdown, .stMarkdown p, .stMarkdown li, [data-testid="stMarkdownContainer"], label, input, textarea,
.stButton p, .stLinkButton p, .stTabs p, .stAlert p, [data-testid="stCaptionContainer"] {{
  font-family:'Montserrat','Segoe UI',Arial,sans-serif;
}}
h1, h2, h3 {{ font-family:'Cinzel',Georgia,serif !important; letter-spacing:.04em; color:{c['creme']}; }}

.mp-topo {{ display:flex; flex-direction:column; align-items:center; text-align:center; gap:2px; margin:0 0 6px; }}
.mp-topo svg {{ filter: drop-shadow(0 6px 16px rgba(224,169,59,.35)); }}
.mp-mae {{ font-family:'Cinzel',Georgia,serif; font-size:.68rem; letter-spacing:.32em; color:{c['suave']}; text-transform:uppercase; margin-top:6px; }}
.mp-titulo {{ font-family:'Great Vibes','Brush Script MT',cursive !important; color:{c['mel']}; font-size:3.4rem !important; line-height:1.1 !important; margin:10px 0 0; }}
.mp-sub {{ font-family:'Cinzel',Georgia,serif; font-size:1rem !important; letter-spacing:.1em; text-transform:uppercase; color:{c['creme']}; margin:2px 0 14px; }}
.mp-sub em {{ font-family:'Great Vibes',cursive; font-style:normal; text-transform:none; color:{c['batom']}; font-size:1.8em; letter-spacing:0; }}
.mp-lema {{ font-family:'Great Vibes',cursive !important; color:{c['mel_claro']}; font-size:1.9rem !important; text-align:center; margin:26px 0 4px; }}
.mp-rodape {{ text-align:center; color:{c['suave']}; font-size:.75rem; letter-spacing:.06em; }}

.mp-plano {{ border:1px solid {c['linha']}; border-radius:16px; padding:16px 18px; margin-bottom:8px; background:rgba(34,9,14,.72); }}
.mp-plano.on {{ border-color:{c['mel']}; background:linear-gradient(180deg, rgba(224,169,59,.16), rgba(34,9,14,.8)); box-shadow:0 14px 36px -22px rgba(224,169,59,.8); }}
.mp-plano .pn {{ font-family:'Great Vibes',cursive; color:{c['mel']}; font-size:2.1rem; line-height:1; }}
.mp-plano .pp {{ font-family:'Cinzel',Georgia,serif; font-size:1.5rem; font-weight:600; color:{c['creme']}; }}
.mp-plano .pp small {{ font-family:'Montserrat'; font-size:.8rem; color:{c['suave']}; }}
.mp-plano .vl {{ color:{c['folha']}; font-size:.85rem; font-weight:600; }}
.mp-plano .tx {{ color:{c['suave']}; font-size:.9rem; margin-top:4px; }}
.mp-selo {{ display:inline-block; background:{c['mel']}; color:{c['noite']}; font-size:.62rem; font-weight:700; letter-spacing:.18em; padding:3px 9px; border-radius:99px; text-transform:uppercase; margin-bottom:6px; }}

.mp-passos {{ display:grid; gap:10px; margin:6px 0 16px; }}
.mp-passo {{ display:grid; grid-template-columns:34px 1fr; gap:12px; align-items:start; }}
.mp-passo b {{ display:block; color:{c['creme']}; }}
.mp-passo div span {{ display:block; color:{c['suave']}; font-size:.9rem; line-height:1.45; }}
.mp-hex {{ width:30px; height:30px; display:grid; place-items:center; color:{c['noite']} !important; font-family:'Cinzel',Georgia,serif; font-weight:600; font-size:.95rem;
  background:{c['mel']}; clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%); }}

.mp-cartao {{ border:1px solid {c['linha']}; border-radius:16px; padding:16px 18px; background:rgba(34,9,14,.78); margin:6px 0 12px; }}
.mp-cartao.mel {{ border-color:{c['mel']}; }}
.mp-codigo {{ font-family:'Cinzel',Georgia,serif; font-size:1.7rem; letter-spacing:.14em; color:{c['mel']}; text-align:center; margin:6px 0; }}
.mp-nivel {{ display:flex; gap:6px; justify-content:space-between; margin:12px 0 6px; }}
.mp-nivel div {{ flex:1; text-align:center; font-size:.72rem; color:{c['suave']}; }}
.mp-nivel i {{ display:block; height:26px; margin:0 auto 4px; width:24px; background:{c['linha']};
  clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%); }}
.mp-nivel .ok i {{ background:{c['mel']}; }}
.mp-nivel .ok {{ color:{c['mel_claro']}; font-weight:600; }}
.mp-barra {{ height:8px; border-radius:99px; background:{c['linha']}; overflow:hidden; margin:8px 0 4px; }}
.mp-barra b {{ display:block; height:100%; background:linear-gradient(90deg,#B7802A,{c['mel']}); border-radius:99px; }}
.mp-spoiler {{ border:1px solid {c['mel']}; border-radius:12px; padding:12px 16px; background:rgba(224,169,59,.10); color:{c['mel_claro']}; margin:8px 0 16px; }}
.mp-gota {{ display:inline-block; background:{c['batom']}; color:{c['creme']}; font-size:.68rem; font-weight:700; letter-spacing:.12em;
  padding:3px 9px; border-radius:99px; text-transform:uppercase; }}

/* ---- layout geral ---- */
.block-container {{ max-width:560px; padding-top:1.4rem; padding-bottom:3rem; }}
footer {{ visibility:hidden; height:0; }}
hr {{ border:none !important; height:1px !important; margin:30px 0 !important; opacity:.7;
  background:linear-gradient(90deg,transparent,{c['mel']},transparent) !important; }}

/* ---- títulos de seção com ornamento ---- */
.mp-secao {{ display:flex; align-items:center; gap:12px; margin:36px 0 16px; font-family:'Cinzel',Georgia,serif;
  font-size:.74rem; letter-spacing:.3em; text-transform:uppercase; color:{c['mel']}; }}
.mp-secao::before {{ content:""; flex:1; height:1px; background:linear-gradient(90deg,transparent,{c['linha']}); }}
.mp-secao::after {{ content:""; flex:1; height:1px; background:linear-gradient(90deg,{c['linha']},transparent); }}
.mp-secao span {{ white-space:nowrap; }}

/* ---- campos de texto ---- */
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {{
  background:#1A0A0E !important; border:1px solid {c['linha']} !important; border-radius:14px !important; }}
[data-baseweb="input"]:focus-within, [data-baseweb="textarea"]:focus-within, [data-baseweb="select"] > div:focus-within {{
  border-color:{c['mel']} !important; box-shadow:0 0 0 3px rgba(224,169,59,.18) !important; }}
input, textarea {{ color:{c['creme']} !important; }}
[data-testid="stWidgetLabel"] p {{ color:{c['creme']} !important; font-weight:500; font-size:.92rem; letter-spacing:.02em; }}
[data-testid="stCaptionContainer"] p {{ color:{c['suave']} !important; line-height:1.5; }}

/* ---- botões ---- */
[data-testid="stBaseButton-primary"], [data-testid="stFormSubmitButton"] button {{ min-height:3rem; border:none !important; border-radius:999px !important;
  background:linear-gradient(180deg,#F0C15A,#B7802A) !important; box-shadow:0 14px 28px -14px rgba(224,169,59,.8); }}
[data-testid="stBaseButton-primary"] p, [data-testid="stFormSubmitButton"] button p {{ color:{c['noite']} !important; font-family:'Cinzel',Georgia,serif !important;
  font-weight:600 !important; letter-spacing:.12em; text-transform:uppercase; font-size:.84rem; }}
[data-testid="stBaseButton-secondary"], [data-testid="stLinkButton"] a {{ min-height:2.8rem; border-radius:999px !important;
  border:1px solid {c['mel']} !important; background:transparent !important; }}
[data-testid="stBaseButton-secondary"] p, [data-testid="stLinkButton"] p {{ color:{c['mel_claro']} !important;
  font-family:'Cinzel',Georgia,serif !important; letter-spacing:.08em; font-size:.82rem; }}

/* ---- escolhas em formato de pílula ---- */
[data-testid="stRadioGroup"] {{ flex-wrap:wrap; gap:8px; }}
[data-testid="stRadioGroup"] > div {{ margin:0 !important; }}
[data-testid="stRadioOption"] {{ background:rgba(34,9,14,.85); border:1px solid {c['linha']} !important;
  border-radius:999px !important; padding:.4rem .95rem !important; transition:all .2s ease; }}
[data-testid="stRadioOption"]:hover {{ border-color:{c['mel']} !important; }}
[data-testid="stRadioOption"]:has(input:checked) {{ background:linear-gradient(180deg,#F0C15A,#B7802A) !important;
  border-color:{c['mel']} !important; box-shadow:0 8px 18px -10px rgba(224,169,59,.9); }}
[data-testid="stRadioOption"]:has(input:checked) p {{ color:{c['noite']} !important; font-weight:600; }}
[data-testid="stRadioOption"] > div > div:first-child {{ display:none !important; }}

/* ---- cartões: expander, abas, métricas, avisos ---- */
[data-testid="stExpander"] {{ border:1px solid {c['linha']} !important; border-radius:16px !important;
  background:rgba(34,9,14,.6); overflow:hidden; }}
[data-testid="stExpander"] summary p {{ font-family:'Cinzel',Georgia,serif; letter-spacing:.06em; color:{c['creme']}; font-size:.95rem; }}
[data-baseweb="tab-highlight"] {{ background:{c['mel']} !important; }}
[data-baseweb="tab-border"] {{ background:{c['linha']} !important; }}
button[role="tab"] p {{ font-family:'Cinzel',Georgia,serif; letter-spacing:.08em; text-transform:uppercase; font-size:.74rem; }}
[data-testid="stMetric"] {{ background:rgba(34,9,14,.85); border:1px solid {c['linha']}; border-radius:16px; padding:12px 14px; }}
[data-testid="stMetricValue"] {{ font-family:'Cinzel',Georgia,serif; color:{c['mel']}; }}
[data-testid="stMetricLabel"] p {{ color:{c['suave']} !important; }}
[data-testid="stAlert"] {{ border-radius:14px; }}
</style>
"""


def secao(titulo: str) -> str:
    """Título de seção com ornamento de linhas douradas."""
    return f'<div class="mp-secao"><span>{titulo}</span></div>'
