import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sistema de Chamados", layout="wide")

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

st.title("🎫 Sistema de Chamados")

params = st.query_params
admin = params.get("admin") == "1"

menu = ["Novo Chamado"]
if admin:
    menu.append("Lista de Chamados")

opcao = st.sidebar.selectbox("Menu", menu)

# NOVO
if opcao == "Novo Chamado":
    nome = st.text_input("Seu nome")
    desc = st.text_area("Descrição")
    prio = st.selectbox("Prioridade",["Baixa","Média","Alta"])

    if st.button("Abrir Chamado"):
        if nome and desc:
            c.execute("""
            INSERT INTO chamados
            (solicitante,descricao,prioridade,status,data)
            VALUES (?,?,?,?,?)
            """,(nome,desc,prio,"Aberto",datetime.now()))
            conn.commit()
            st.success("Chamado enviado!")
        else:
            st.warning("Preencha tudo!")

# LISTA (só admin)
if opcao == "Lista de Chamados":
    df = pd.read_sql("SELECT * FROM chamados ORDER BY id DESC", conn)

    for i, row in df.iterrows():
        st.write(f"### Chamado #{row['id']}")
        st.write(row["descricao"])
        st.write(f"{row['solicitante']} | {row['prioridade']} | {row['status']}")

        if row["status"] == "Aberto":
            if st.button(f"Finalizar {row['id']}"):
                c.execute("UPDATE chamados SET status='Finalizado' WHERE id=?", (row["id"],))
                conn.commit()
                st.rerun()

        st.divider()
