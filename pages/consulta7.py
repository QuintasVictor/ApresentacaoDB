import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Consulta 7", layout="wide")
st.title("Consulta 7")
st.subheader("Detecção de Eventos Simultâneos na Mesma Sala")
st.divider()

# Simulação das tabelas como DataFrames
_data_hora_sala_evento = pd.DataFrame({
    "idEvento": [3,6,7,10,1,4,7,8,2,5,9],
    "idSala":    [1,1,1, 1,2,2, 2,2,3,3,3],
    "idDataHora":[3,6,7,10,1,4, 1,8,2,5,9]
})
evento = pd.DataFrame({
    "nomeEvento": [f"Evento {i}" for i in range(1, 11)],
    "duracao": ["01:30:00", "02:30:00", "01:30:00", "02:30:00", "01:30:00",
                 "02:30:00", "01:00:00", "01:30:00", "02:00:00", "02:30:00"],
    "idEvento": list(range(1, 11)),
    "siglaDepartamento": ["DINF", "DINF", "DINF", "DMAT", "DFIS", "DMAT", "DINF", "DINF", "DINF", "DINF"],
    "idTipo": [2, 3, 3, 2, 2, 1, 2, 2, 3, 3]
})
sala = pd.DataFrame({
    "idSala": [1,2,3],
    "nomeSala": ["Sala A","Sala B","Sala C"]
})
data_hora = pd.DataFrame({
    "idDataHora": list(range(1,11)),
    "data": ["2025-05-16","2025-05-17","2025-05-18","2025-05-19","2025-05-20",
              "2025-05-21","2025-05-22","2025-05-23","2025-05-24","2025-05-25"],
    "hora": ["10:00:00","11:00:00","12:00:00","13:00:00","14:00:00",
             "10:00:00","15:00:00","16:00:00","17:00:00","18:00:00"]
})

# Pré-calcular todos os joins necessários
# Etapa 1: auto-join dhse para pares de eventos na mesma sala e horário
dhse1 = _data_hora_sala_evento.copy()
# rename columns to merge
with st.expander("Tabela: evento"):
    st.dataframe(evento)

with st.expander("Tabela: data_hora"):
    st.dataframe(data_hora)

with st.expander("Tabela: sala"):
    st.dataframe(sala)

with st.expander("Tabela: _data_hora_sala_evento"):
    st.dataframe(_data_hora_sala_evento)

# Cópias para auto-join
dhse1 = _data_hora_sala_evento.copy()
dhse2 = _data_hora_sala_evento.copy()

# Inicializa etapa
if "step" not in st.session_state:
    st.session_state.step = 0

# Descrição inicial
st.divider()
st.subheader("Objetivo: Detecção de eventos que ocorrem simultaneamente na mesma sala")
st.write("Consulta: encontrar pares de eventos na mesma sala e horário")

# Etapa 1: botão centralizado
if st.session_state.step == 0:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.button("1. Quais são os eventos que acontecem na mesma sala na mesma hora?"):
            st.session_state.step = 1

# Etapa 1: executar e mostrar join1
if st.session_state.step >= 1:
    st.subheader(
        "1- dhse1 ⨝  dhse2 ON dhse1.idSala = dhse2.idSala AND dhse1.idDataHora = dhse2.idDataHora AND dhse1.idEvento < dhse2.idEvento")
    st.write("_data_hora_sala_evento dhse1 JOIN _data_hora_sala_evento dhse2")
    join1 = dhse1.merge(
        dhse2,
        on=["idSala","idDataHora"],
        suffixes=("1","2")
    )
    join1 = join1[join1['idEvento1'] < join1['idEvento2']]
    st.dataframe(join1)
    if st.session_state.step == 1:
        c1, c2, c3 = st.columns([2,1,2])
        with c2:
            if st.button("2. Quais os nomes desses eventos?", key="btn2"):
                st.session_state.step = 2

# Etapa 2: executar e mostrar join2
if st.session_state.step >= 2:
    st.subheader("2- ⨝ evento e1 ON dhse1.idEvento = e1.idEvento ⨝ evento e2 ON dhse2.idEvento = e2.idEvento")
    st.write("Renomear: idEvento → idEvento1; nomeEvento: Evento1")
    st.write("Renomear: idEvento → idEvento2; nomeEvento: Evento2")
    join2 = join1.merge(
        evento.rename(columns={"idEvento":"idEvento1","nomeEvento":"Evento1"}),
        on="idEvento1"
    ).merge(
        evento.rename(columns={"idEvento":"idEvento2","nomeEvento":"Evento2"}),
        on="idEvento2"
    )
    st.dataframe(join2)
    if st.session_state.step == 2:
        c1, c2, c3 = st.columns([2,1,2])
        with c2:
            if st.button("3. Qual o nome da sala que está dando conflito?", key="btn3"):
                st.session_state.step = 3

# Etapa 3: executar e mostrar join3
if st.session_state.step >= 3:
    st.subheader("3- ⨝ sala s ON dhse1.idSala = s.idSala")
    join3 = join2.merge(sala, on="idSala")
    st.dataframe(join3)
    if st.session_state.step == 3:
        c1, c2, c3 = st.columns([2,1,2])
        with c2:
            if st.button("4. Qual a data e a hora do conflito?", key="btn4"):
                st.session_state.step = 4

# Etapa 4: executar e mostrar resultado final
if st.session_state.step >= 4:

    st.subheader("4- ⨝ data_hora dh ON dhse1.idDataHora = dh.idDataHora")
    final = join3.merge(data_hora, on="idDataHora")
    st.dataframe(final)
    st.subheader("5 - SELECT e1.nomeEvento AS Evento1, e2.nomeEvento AS Evento2, s.nomeSala, dh.data, dh.hora")
    st.dataframe(final[["Evento1","Evento2","nomeSala","data","hora"]].reset_index(drop=True))
    st.divider()
    st.subheader("Consulta final")
    c1, c2, c3 = st.columns([2,5,2])
    with c2:

        query = """
        SELECT e1.nomeEvento AS Evento1, e2.nomeEvento AS Evento2, s.nomeSala, dh.data, dh.hora
        FROM _data_hora_sala_evento dhse1
        JOIN _data_hora_sala_evento dhse2 
            ON dhse1.idSala = dhse2.idSala 
            AND dhse1.idDataHora = dhse2.idDataHora 
            AND dhse1.idEvento < dhse2.idEvento
        JOIN evento e1 ON dhse1.idEvento = e1.idEvento
        JOIN evento e2 ON dhse2.idEvento = e2.idEvento
        JOIN sala s ON dhse1.idSala = s.idSala
        JOIN data_hora dh ON dhse1.idDataHora = dh.idDataHora;
        """

        st.code(query, language="sql")

    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("Clique para recomeçar", key="btnRestart"):
            st.session_state.step = 0
