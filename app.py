import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# CONFIG
st.set_page_config(page_title="Sistema de Chamados", layout="wide")

st.title("🎫 Sistema de Chamados")

st.write("Banco salvo em:", os.getcwd())

# BANCO
conn = sqlite3.connect("chamados.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS chamados(
id INTEGER PRIMARY KEY AUTOINCREMENT,
solicitante TEXT,
descricao TEXT,
prioridade TEXT,
status TEXT,
data TEXT
)
""")

menu = st.sidebar.selectbox("Menu", ["Novo Chamado","Lista de Chamados"])

# NOVO
if menu == "Novo Chamado":

    nome = st.text_input("Solicitante")
    desc = st.text_area("Descrição")
    prio = st.selectbox("Prioridade",["Baixa","Média","Alta"])

    if st.button("Abrir Chamado"):
        if nome and desc:
            c.execute("""
            INSERT INTO chamados (solicitante,descricao,prioridade,status,data)
            VALUES (?,?,?,?,?)
            """,(nome,desc,prio,"Aberto",datetime.now()))
            conn.commit()
            st.success("Chamado criado!")
        else:
            st.warning("Preencha tudo!")

# LISTA
if menu == "Lista de Chamados":
    df = pd.read_sql("SELECT * FROM chamados ORDER BY id DESC", conn)

    if df.empty:
        st.info("Nenhum chamado ainda.")
    else:
        for i, row in df.iterrows():
            st.write(f"### Chamado #{row['id']}")
            st.write(f"👤 {row['solicitante']}")
            st.write(f"📝 {row['descricao']}")
            st.write(f"⚡ Prioridade: {row['prioridade']} | Status: {row['status']}")
            st.write(f"📅 {row['data']}")

            # BOTÃO FINALIZAR
            if row["status"] == "Aberto":
                if st.button(f"Finalizar {row['id']}"):
                    c.execute("UPDATE chamados SET status='Finalizado' WHERE id=?", (row["id"],))
                    conn.commit()
                    st.rerun()

            st.divider()