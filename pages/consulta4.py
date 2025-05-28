import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Consulta 4", layout="wide")
st.title("Consulta 4")
st.subheader("Listar os nomes das salas e a quantidade de eventos já realizadas nelas, ordenando pela quantidade em ordem decrescente.")
st.divider()
# Simulação das tabelas como DataFrames
sala = pd.DataFrame({
    "idSala":   [1, 2, 3],
    "nomeSala": ["Sala A", "Sala B", "Sala C"]
})
_data_hora_sala_evento = pd.DataFrame({
    "idEvento":    [1,4,7,8,2,5,9,3,6,10,7],
    "idSala":      [2,2,2,2,3,3,3,1,1,1,2],
    "idDataHora":  [1,4,1,8,2,5,9,3,6,10,1]
})

# Estado da etapa
if 'step' not in st.session_state:
    st.session_state.step = 0

# 1. Tabelas relevantes
st.subheader("Tabelas Relevantes")
with st.expander("sala"):
    st.dataframe(sala)
with st.expander("_data_hora_sala_evento"):
    st.dataframe(_data_hora_sala_evento)

st.divider()
# 2. Objetivo
st.subheader("Objetivo: Listar o nome das salas e a quantidade de eventos realizados nelas")
st.write("Como fazer: unir sala e _data_hora_sala_evento, agrupar por sala e contar eventos, ordenar desc")

# 3. Botão 1: Join sala + dhse
if st.session_state.step == 0:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.button("1. Juntar sala com _data_hora_sala_evento"):
            st.session_state.step = 1

# 4. Etapa 1: exibir join1 + Botão 2
if st.session_state.step >= 1:
    st.subheader("1- sala s ⨝ _data_hora_sala_evento dhse ON s.idSala = dhse.idSala")
    join1 = sala.merge(_data_hora_sala_evento, on="idSala")
    st.dataframe(join1)
    if st.session_state.step == 1:
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.button("2. Agrupar por sala e contar eventos"):
                st.session_state.step = 2

# 5. Etapa 2: exibir agrupamento + Botão 3
if st.session_state.step >= 2:
    st.subheader("2- GROUP BY s.idSala ORDER BY total_eventos DESC")
    result = join1.groupby('nomeSala').size().reset_index(name='total_eventos')
    result = result.sort_values(by='total_eventos', ascending=False)
    st.dataframe(result)
    if st.session_state.step == 2:
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.button("3. Exibir SQL completo"):
                st.session_state.step = 3

# 6. Etapa 3: exibir SQL completo + botão reiniciar
if st.session_state.step >= 3:
    st.subheader("Consulta completa")
    sql = '''
    SELECT s.nomeSala, COUNT(dhse.idEvento) AS total_eventos
      FROM sala s
      JOIN _data_hora_sala_evento dhse ON s.idSala = dhse.idSala
      GROUP BY s.idSala
      ORDER BY total_eventos DESC;
    '''
    st.code(sql, language="sql")
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.button("Clique para recomeçar", key="btnRestart5"):
            st.session_state.step = 0
