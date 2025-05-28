import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Consulta 1", layout="wide")

# Simulando as tabelas como DataFrames
evento = pd.DataFrame({
    "nomeEvento": [f"Evento {i}" for i in range(1, 11)],
    "duracao": ["01:30:00", "02:30:00", "01:30:00", "02:30:00", "01:30:00",
                 "02:30:00", "01:00:00", "01:30:00", "02:00:00", "02:30:00"],
    "idEvento": list(range(1, 11)),
    "siglaDepartamento": ["DINF", "DINF", "DINF", "DMAT", "DFIS", "DMAT", "DINF", "DINF", "DINF", "DINF"],
    "idTipo": [2, 3, 3, 2, 2, 1, 2, 2, 3, 3]
})

data_hora = pd.DataFrame({
    "idDataHora": list(range(1, 11)),
    "data": pd.to_datetime([
        "2025-05-16", "2025-05-17", "2025-05-18", "2025-05-19", "2025-05-20",
        "2025-05-21", "2025-05-22", "2025-05-23", "2025-05-24", "2025-05-25"
    ]),
    "hora": ["10:00:00", "11:00:00", "12:00:00", "13:00:00", "14:00:00",
             "10:00:00", "15:00:00", "16:00:00", "17:00:00", "18:00:00"]
})

_data_hora_sala_evento = pd.DataFrame({
    "idEvento": [3, 6, 7, 10, 1, 4, 7, 8, 2, 5, 9],
    "idSala": [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3],
    "idDataHora": [3, 6, 7, 10, 1, 4, 1, 8, 2, 5, 9]
})

st.title("Consulta 1")
st.subheader("Listar os nomes dos eventos futuros em ordem crescente de data.")
st.divider()

# Mostrar tabelas originais
with st.expander("Tabela: evento"):
    st.dataframe(evento)

with st.expander("Tabela: _data_hora_sala_evento"):
    st.dataframe(_data_hora_sala_evento)

with st.expander("Tabela: data_hora"):
    st.dataframe(data_hora)

# Inicialização -
join1 = pd.merge(evento, _data_hora_sala_evento, on="idEvento")
join2 = pd.merge(join1, data_hora, on="idDataHora")
df_futuro = join2[join2["data"] > pd.to_datetime(date.today())].sort_values(by="data")

# Estado da etapa
if "step" not in st.session_state:
    st.session_state.step = 0

# Descrição inicial
st.divider()
st.subheader("Objetivo Principal: Relacionar a tabela EVENTO com a tabela DATA_HORA")
st.write("Como fazer: Utilizar a tabela intermediaria data_hora_sala_evento para vincular as informações de Nome do evento com sua Data")

# Botão 1 centralizado
if st.session_state.step == 0:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("Juntar a tabela evento com a tabela intermediaria dhse"):
            st.session_state.step = 1

# Etapa 1: exibir join1
if st.session_state.step >= 1:
    st.subheader("1- Evento e ⨝ data_hora_sala_evento dhse ON e.idEvento = dhse.idEvento")
    st.dataframe(join1)

# Botão 2 centralizado
if st.session_state.step == 1:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("Relacionar o resultado anterior com os dados de Data Hora"):
            st.session_state.step = 2

# Etapa 2: exibir join2
if st.session_state.step >= 2:
    st.subheader("2- ⨝ data_hora dh ON dh.idDataHora = shde.idDataHora")
    st.dataframe(join2)

# Botão 3 centralizado
if st.session_state.step == 2:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("Filtrar por data futura ( > hoje )"):
            st.session_state.step = 3

# Etapa 3: exibir df_futuro
if st.session_state.step >= 3:
    st.subheader("3- WHERE data_hora.data > CURDATE() ORDER BY dh.data ASC")
    st.dataframe(df_futuro)

# Botão 4 centralizado
if st.session_state.step == 3:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("Aplicar SELECT Nome Evento e Data"):
            st.session_state.step = 4

# Etapa 4: exibir resultado final e SQL
if st.session_state.step >= 4:
    st.subheader("4- SELECT evento.nomeEvento, data_hora.data")
    st.dataframe(df_futuro[["nomeEvento", "data"]].reset_index(drop=True))
    st.divider()
    st.subheader("Consulta final")
    c1, c2, c3 = st.columns([2, 5, 2])
    with c2:
        query = '''
        SELECT e.nomeEvento, dh.data 
        FROM evento e 
        JOIN _data_hora_sala_evento dhse ON e.idEvento = dhse.idEvento 
        JOIN data_hora dh ON dh.idDataHora = dhse.idDataHora 
        WHERE dh.data > CURDATE() ORDER BY dh.data ASC; 
        '''
        st.code(query, language="sql")
    # Botão reiniciar
    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("Clique para recomeçar", key="btnRestart"):
            st.session_state.step = 0
