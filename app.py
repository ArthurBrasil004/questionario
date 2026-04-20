"""
app.py  -  Questionario
Formulario multi-etapa condicional com salvamento em Excel.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

from questions import FEMI_QUESTIONS, MASC_QUESTIONS

EXCEL_PATH     = "respostas.xlsx"
OUTRO_LABEL    = "Outro"
try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
except Exception:
    ADMIN_PASSWORD = "admin123"

st.set_page_config(page_title="Questionario", page_icon="💎", layout="centered")

def load_css(path):
    with open(path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

def get_questions():
    return FEMI_QUESTIONS if st.session_state.get("genero") == "Feminino" else MASC_QUESTIONS

def init_state():
    defaults = {"step": 0, "nome": "", "email": "", "idade": None, "genero": None, "respostas": {}}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def is_valid_email(email):
    return "@" in email and "." in email.split("@")[-1]

def progress_bar():
    questions = get_questions() if st.session_state.get("genero") else []
    total = 3 + len(questions)
    step  = st.session_state.step
    st.progress(min(step / total, 1.0))
    if step > 0:
        st.caption(f"Etapa {step} de {total}")

def clean_value(v):
    # Converte R\$ (escape LaTeX) de volta para R$ antes de gravar no Excel
    if isinstance(v, list):
        return " | ".join(s.replace("\\$", "$") for s in v)
    return str(v).replace("\\$", "$") if v else ""

def save_to_excel(row):
    df_new = pd.DataFrame([row])
    if Path(EXCEL_PATH).exists():
        df_existing = pd.read_excel(EXCEL_PATH, engine="openpyxl")
        df_final    = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_final = df_new
    df_final.to_excel(EXCEL_PATH, index=False, engine="openpyxl")

def build_row():
    row = {
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "nome":      st.session_state.nome,
        "email":     st.session_state.email,
        "idade":     st.session_state.idade,
        "genero":    st.session_state.genero,
    }
    for q in get_questions():
        row[q["id"]] = clean_value(st.session_state.respostas.get(q["id"], ""))
    return row

# ── Telas ───────────────────────────────────────────────────────────────────
def tela_identificacao():
    st.markdown('<p class="titulo-step">💎 Bem-vindo(a)!</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-step">Este questionario leva cerca de 3 minutos. Suas respostas sao anonimas.</p>', unsafe_allow_html=True)
    nome  = st.text_input("Nome completo", value=st.session_state.nome,  placeholder="Seu nome")
    email = st.text_input("E-mail",         value=st.session_state.email, placeholder="seuemail@exemplo.com")
    idade = st.radio("Faixa de idade", ["18-24 anos", "25-34 anos", "35-44 anos", "45 anos ou mais"],
                     index=["18-24 anos","25-34 anos","35-44 anos","45 anos ou mais"].index(st.session_state.idade)
                     if st.session_state.idade else None, horizontal=True)
    if st.button("Continuar ->", disabled=not (nome.strip() and is_valid_email(email) and idade),
                 use_container_width=True, type="primary"):
        st.session_state.nome = nome; st.session_state.email = email
        st.session_state.idade = idade; st.session_state.step = 1; st.rerun()

def tela_genero():
    st.markdown('<p class="titulo-step">Como voce se identifica?</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-step">O questionario tem perguntas diferentes por perfil de compra.</p>', unsafe_allow_html=True)
    genero = st.radio("Genero", ["Feminino", "Masculino"],
                      index=["Feminino","Masculino"].index(st.session_state.genero)
                      if st.session_state.genero else None,
                      horizontal=True, label_visibility="collapsed")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("<- Voltar", use_container_width=True):
            st.session_state.step = 0; st.rerun()
    with col2:
        if st.button("Continuar ->", disabled=not genero, use_container_width=True, type="primary"):
            st.session_state.genero = genero; st.session_state.step = 2; st.rerun()

def tela_intro():
    nome_curto = st.session_state.nome.split()[0]
    genero     = st.session_state.genero
    questions  = get_questions()
    st.markdown(f'<p class="titulo-step">Ola, {nome_curto}! 👋</p>', unsafe_allow_html=True)
    st.markdown(f'<span class="badge-genero">Perfil {genero}</span>', unsafe_allow_html=True)
    desc = ("Agora vamos entender seus habitos de compra de joias e acessorios."
            if genero == "Feminino" else "Agora vamos entender como voce compra joias para presentear.")
    st.markdown(f'<p class="sub-step">{desc}<br>Sao <strong>{len(questions)}</strong> perguntas rapidas.</p>',
                unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("<- Voltar", use_container_width=True):
            st.session_state.step = 1; st.rerun()
    with col2:
        if st.button("Comecar ->", use_container_width=True, type="primary"):
            st.session_state.step = 3; st.rerun()

def tela_pergunta(idx):
    questions = get_questions()
    q         = questions[idx]
    total     = len(questions)
    num       = idx + 1
    tem_outro = q.get("tem_outro", False)

    st.markdown(f"**Pergunta {num} de {total}**")
    st.markdown(f"### {q['texto']}")
    resposta_atual = st.session_state.respostas.get(q["id"])

    if q["tipo"] == "single":
        opcoes_exibidas = q["opcoes"] + ([OUTRO_LABEL] if tem_outro else [])
        idx_atual = None
        if resposta_atual in opcoes_exibidas:
            idx_atual = opcoes_exibidas.index(resposta_atual)
        elif resposta_atual and str(resposta_atual).startswith("Outro:"):
            idx_atual = opcoes_exibidas.index(OUTRO_LABEL)
        valor = st.radio("Opcoes", opcoes_exibidas, index=idx_atual, label_visibility="collapsed")
        outro_texto = None
        if tem_outro and valor == OUTRO_LABEL:
            key = f"{q['id']}_outro_texto"
            txt = st.text_input("Especifique:", value=st.session_state.get(key, ""),
                                placeholder="Digite aqui...", key=key)
            outro_texto = txt.strip() if txt.strip() else None
        valido      = valor is not None and (valor != OUTRO_LABEL or outro_texto)
        valor_final = f"Outro: {outro_texto}" if valor == OUTRO_LABEL and outro_texto else valor

    else:
        st.caption(f"Selecione ate {q['max']} opcoes")
        opcoes_exibidas  = q["opcoes"] + ([OUTRO_LABEL] if tem_outro else [])
        selecionados     = list(resposta_atual) if isinstance(resposta_atual, list) else []
        selecionados_limpos = []
        outro_salvo = ""
        for s in selecionados:
            if str(s).startswith("Outro:"):
                selecionados_limpos.append(OUTRO_LABEL)
                outro_salvo = s.replace("Outro:", "").strip()
            else:
                selecionados_limpos.append(s)
        novos = []
        for opcao in opcoes_exibidas:
            marcado      = opcao in selecionados_limpos
            desabilitado = not marcado and len(selecionados_limpos) >= q["max"]
            if st.checkbox(opcao, value=marcado, disabled=desabilitado, key=f"{q['id']}_{opcao}"):
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

    prev_step = 2 if idx == 0 else 3 + idx - 1
    col1, col2 = st.columns(2)
    with col1:
        if st.button("<- Voltar", use_container_width=True):
            st.session_state.step = prev_step; st.rerun()
    with col2:
        label = "Finalizar" if num == total else "Continuar ->"
        if st.button(label, disabled=not valido, use_container_width=True, type="primary"):
            st.session_state.respostas[q["id"]] = valor_final
            st.session_state.step = 3 + idx + 1; st.rerun()

def tela_final():
    st.balloons()
    nome_curto = st.session_state.nome.split()[0]
    st.markdown(f'<div class="success-card"><p>Respostas enviadas com sucesso, {nome_curto}! Obrigado pela participacao.</p></div>',
                unsafe_allow_html=True)
    row = build_row()
    save_to_excel(row)

    with st.expander("Ver resumo das suas respostas"):
        labels = {"timestamp":"Data/hora","nome":"Nome","email":"E-mail","idade":"Faixa etaria","genero":"Perfil"}
        for k, v in row.items():
            st.write(f"**{labels.get(k, k.replace(chr(95), chr(32)).capitalize())}:** {v}")

    st.divider()
    with st.expander("Área administrativa"):
        senha = st.text_input("Senha", type="password", key="admin_senha")
        if senha:
            if senha == ADMIN_PASSWORD:
                st.success("Acesso autorizado.")
                if Path(EXCEL_PATH).exists():
                    with open(EXCEL_PATH, "rb") as f:
                        st.download_button(
                            label="Baixar todas as respostas (Excel)",
                            data=f,
                            file_name="respostas.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True,
                        )
                    df = pd.read_excel(EXCEL_PATH, engine="openpyxl")
                    st.caption(f"{len(df)} resposta(s) registrada(s) ate agora.")
                else:
                    st.info("Nenhuma resposta registrada ainda.")
            else:
                st.error("Senha incorreta.")

    if st.button("Responder novamente", use_container_width=True):
        for key in ["step","nome","email","idade","genero","respostas"]:
            del st.session_state[key]
        st.rerun()

def main():
    init_state()
    progress_bar()
    step      = st.session_state.step
    questions = get_questions() if st.session_state.get("genero") else []
    if step == 0:
        tela_identificacao()
    elif step == 1:
        tela_genero()
    elif step == 2:
        tela_intro()
    elif 3 <= step < 3 + len(questions):
        tela_pergunta(step - 3)
    else:
        tela_final()

if __name__ == "__main__":
    main()