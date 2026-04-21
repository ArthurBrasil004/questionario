"""
app.py  -  Questionario SG  (v4)
Respostas salvas direto no Google Sheets via service account.
Credenciais: credentials.json (local) ou st.secrets (Streamlit Cloud).
"""

import streamlit as st
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

from questions import UNISSEX_QUESTIONS, FEMI_QUESTIONS, MASC_QUESTIONS

# ── Constantes ───────────────────────────────────────────────────────────────
SHEET_NAME   = "Questionario-iolita"
OUTRO_LABEL  = "Outro"
SKIP_TO_END  = 9999

BOLSAS_NEGATIVO = [
    "Nao, prefiro joias",
    "Nao costumo presentear com bolsas de marca",
]

ALL_COLS = ['timestamp', 'idade', 'valor_ultima_compra', 'renda', 'sexo', 'freq_compra', 'para_quem_compra', 'onde_compra', 'preocupacao_compra', 'o_que_valoriza', 'estilo_preferido', 'lojas_conhece', 'lojas_ja_comprou', 'lojas_pretende_comprar', 'freq_bolsas', 'tipo_bolsa', 'marcas_bolsas', 'marcas_presentear', 'ocasioes_compra', 'como_decide', 'compraria_online', 'interesse_bolsas', 'marcas_conhece', 'marcas_ja_comprou', 'marcas_pretende_comprar']

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

st.set_page_config(page_title="Questionario SG", page_icon="diamond_with_a_dot", layout="centered")

def load_css(path):
    with open(path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")


# ── Google Sheets ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_sheet():
    """Retorna a worksheet. Usa secrets.toml na nuvem ou credentials.json local."""
    try:
        # Streamlit Cloud: credenciais em st.secrets
        info = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    except Exception:
        # Local: le o arquivo credentials.json
        creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

    client = gspread.authorize(creds)
    sheet  = client.open(SHEET_NAME).sheet1
    return sheet


def save_to_sheets(row: dict):
    """Acrescenta uma linha na primeira linha vazia disponivel."""
    sheet = get_sheet()
    linha = [row.get(col, "") for col in ALL_COLS]
    sheet.append_row(linha, value_input_option="USER_ENTERED")



# ── Helpers de estado ─────────────────────────────────────────────────────────
def init_state():
    defaults = {"step": 0, "respostas": {}}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def get_sexo():
    return st.session_state.respostas.get("sexo")

def get_specific_questions():
    sexo = get_sexo()
    if sexo == "Feminino":
        return FEMI_QUESTIONS
    elif sexo == "Masculino":
        return MASC_QUESTIONS
    return []

def get_total_steps():
    sexo = get_sexo()
    if not sexo:
        return len(UNISSEX_QUESTIONS)
    return len(UNISSEX_QUESTIONS) + len(get_specific_questions())

def progress_bar():
    total = get_total_steps()
    step  = min(st.session_state.step, total)
    st.progress(step / total if total else 0)
    st.caption(f"Pergunta {step} de {total}")

def clean_value(v):
    if isinstance(v, list):
        return " | ".join(str(s).replace("\\$", "$") for s in v)
    return str(v).replace("\\$", "$") if v else ""

def build_row():
    row = {"timestamp": datetime.now().strftime("%d/%m/%Y %H:%M")}
    for q in UNISSEX_QUESTIONS:
        row[q["id"]] = clean_value(st.session_state.respostas.get(q["id"], ""))
    for q in get_specific_questions():
        row[q["id"]] = clean_value(st.session_state.respostas.get(q["id"], ""))
    return row

def get_next_step(current_step, q_id, valor_final):
    sexo = get_sexo()
    if sexo == "Masculino" and q_id == "interesse_bolsas":
        if valor_final in BOLSAS_NEGATIVO:
            return SKIP_TO_END
        return current_step + 1
    if sexo == "Feminino" and q_id == "marcas_bolsas":
        sel = valor_final if isinstance(valor_final, list) else []
        if not sel:
            return SKIP_TO_END
        return current_step + 1
    return current_step + 1

def get_prev_step(current_step):
    return max(0, current_step - 1)


# ── Renderizacao de opcoes ────────────────────────────────────────────────────
def render_single(q, resposta_atual):
    tem_outro = q.get("tem_outro", False)
    opcoes    = q["opcoes"] + ([OUTRO_LABEL] if tem_outro else [])
    idx_atual = None
    if resposta_atual in opcoes:
        idx_atual = opcoes.index(resposta_atual)
    elif resposta_atual and str(resposta_atual).startswith("Outro:"):
        idx_atual = opcoes.index(OUTRO_LABEL)
    valor = st.radio("op", opcoes, index=idx_atual, label_visibility="collapsed")
    outro_texto = None
    if tem_outro and valor == OUTRO_LABEL:
        key = f"{q['id']}_outro_texto"
        txt = st.text_input("Especifique:", value=st.session_state.get(key, ""),
                            placeholder="Digite aqui...", key=key)
        outro_texto = txt.strip() if txt.strip() else None
    valido      = valor is not None and (valor != OUTRO_LABEL or outro_texto)
    valor_final = f"Outro: {outro_texto}" if valor == OUTRO_LABEL and outro_texto else valor
    return valor_final, valido

def render_multi(q, resposta_atual):
    tem_outro = q.get("tem_outro", False)
    opcoes    = q["opcoes"] + ([OUTRO_LABEL] if tem_outro else [])
    selecionados_limpos = []
    outro_salvo = ""
    if isinstance(resposta_atual, list):
        for s in resposta_atual:
            if str(s).startswith("Outro:"):
                selecionados_limpos.append(OUTRO_LABEL)
                outro_salvo = s.replace("Outro:", "").strip()
            else:
                selecionados_limpos.append(s)
    st.caption(f"Selecione ate {q['max']} opcoes")
    novos = []
    for opcao in opcoes:
        marcado      = opcao in selecionados_limpos
        desabilitado = not marcado and len(selecionados_limpos) >= q["max"]
        if st.checkbox(opcao, value=marcado, disabled=desabilitado,
                       key=f"{q['id']}_{opcao}"):
            novos.append(opcao)
    outro_texto = None
    if tem_outro and OUTRO_LABEL in novos:
        key = f"{q['id']}_outro_texto"
        txt = st.text_input("Especifique:", value=st.session_state.get(key, outro_salvo),
                            placeholder="Digite aqui...", key=key)
        outro_texto = txt.strip() if txt.strip() else None
    valor_final = []
    for n in novos:
        if n == OUTRO_LABEL:
            if outro_texto:
                valor_final.append(f"Outro: {outro_texto}")
        else:
            valor_final.append(n)
    valido = len(novos) > 0 and (OUTRO_LABEL not in novos or outro_texto)
    return valor_final, valido

def render_dynamic_single(q, resposta_atual):
    fonte_val  = st.session_state.respostas.get(q["fonte"], [])
    opcoes_din = []
    for v in (fonte_val if isinstance(fonte_val, list) else []):
        label = v.replace("Outro: ", "") if v.startswith("Outro:") else v
        opcoes_din.append(label)
    if not opcoes_din:
        return None, True
    idx_atual = None
    if resposta_atual in opcoes_din:
        idx_atual = opcoes_din.index(resposta_atual)
    valor  = st.radio("op", opcoes_din, index=idx_atual, label_visibility="collapsed")
    valido = valor is not None
    return valor, valido


# ── Tela de pergunta ──────────────────────────────────────────────────────────
def tela_pergunta(step):
    n_unissex = len(UNISSEX_QUESTIONS)
    if step < n_unissex:
        q     = UNISSEX_QUESTIONS[step]
        num   = step + 1
        total = get_total_steps()
        secao = "Perfil geral"
    else:
        idx   = step - n_unissex
        qs    = get_specific_questions()
        q     = qs[idx]
        num   = step + 1
        total = get_total_steps()
        secao = "Joias" if get_sexo() == "Feminino" else "Presentes"

    st.markdown(f"**{secao}  |  Pergunta {num} de {total}**")
    st.markdown(f"### {q['texto']}")
    resposta_atual = st.session_state.respostas.get(q["id"])
    tipo = q.get("tipo")

    if tipo == "single":
        valor_final, valido = render_single(q, resposta_atual)
    elif tipo == "multi":
        valor_final, valido = render_multi(q, resposta_atual)
    elif tipo == "dynamic_single":
        valor_final, valido = render_dynamic_single(q, resposta_atual)
    else:
        valor_final, valido = None, False

    col1, col2 = st.columns(2)
    with col1:
        if step > 0:
            if st.button("Voltar", use_container_width=True):
                st.session_state.step = get_prev_step(step)
                st.rerun()
    with col2:
        is_last = (step == get_total_steps() - 1)
        label   = "Finalizar" if is_last else "Continuar"
        if st.button(label, disabled=not valido, use_container_width=True, type="primary"):
            st.session_state.respostas[q["id"]] = valor_final
            next_step = get_next_step(step, q["id"], valor_final)
            st.session_state.step = next_step
            st.rerun()


# ── Tela final ────────────────────────────────────────────────────────────────
def tela_final():
    st.balloons()
    st.markdown('<p class="titulo-step">Obrigado pela participacao!</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-step">Suas respostas foram registradas com sucesso.</p>',
                unsafe_allow_html=True)

    row = build_row()
    save_to_sheets(row)

    if st.button("Responder novamente", use_container_width=True):
        for k in ["step", "respostas"]:
            del st.session_state[k]
        st.rerun()


# ── Roteador principal ────────────────────────────────────────────────────────
def main():
    init_state()

    step  = st.session_state.step
    total = get_total_steps()

    if step == SKIP_TO_END or step >= total:
        tela_final()
    else:
        progress_bar()
        tela_pergunta(step)


if __name__ == "__main__":
    main()