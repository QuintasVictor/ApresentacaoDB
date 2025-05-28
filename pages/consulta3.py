import streamlit as st
import pandas as pd
from datetime import date

# Configuração da página
st.set_page_config(page_title="Consulta 3:", layout="wide")
st.title("Consulta 3: ")
st.subheader("Participantes inscritos em mais de um evento")
st.divider()

# Simulação das tabelas como DataFrames
alunos = pd.DataFrame({
    "idAluno": list(range(1001, 1010)),
    "nome": [f"Aluno {i}" for i in range(1001, 1010)],
    "email": [f"aluno.{i}@email.com" for i in range(1001, 1010)]
})
alunos_participante = pd.DataFrame({
    "idAluno": [1002,1003,1004,1005,1006,1007],
    "idParticipante": [1,2,3,4,5,6]
})
evento_participante = pd.DataFrame({
    "idEvento": [1,2,3,2,3,4,5,6] + [1,1,1] + [7]*31,
    "idParticipante": [1,1,1,2,3,4,5,6,7,8,9] + list(range(10,41))
})
professores = pd.DataFrame({
    "idProfessor": [501,502,503,504,505,506],
    "nome": [f"Professor {i}" for i in range(501,507)],
    "email": [f"professor.{i}@email.com" for i in range(501,507)]
})
professores_participante = pd.DataFrame({
    "idProfessor": [502,503,504,505,506,501],
    "idParticipante": [1,2,3,4,5,6]
})

# Estado da etapa
if 'step' not in st.session_state:
    st.session_state.step = 0

# 1. Tabelas relevantes (expansíveis)
st.subheader("Tabelas Relevantes")
with st.expander("alunos"):
    st.dataframe(alunos)
with st.expander("alunos_participante"):
    st.dataframe(alunos_participante)
with st.expander("evento_participante"):
    st.dataframe(evento_participante)
with st.expander("professores"):
    st.dataframe(professores)
with st.expander("professores_participante"):
    st.dataframe(professores_participante)

st.divider()
# 2. Objetivo
st.subheader("Objetivo: Listar nomes e e-mails dos participantes (alunos e professores) geados em >1 evento")
st.write("Como fazer: unir participações e filtrar agrupamentos com COUNT > 1")

# 3. Botão 1: Join ep + ap
if st.session_state.step == 0:
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        if st.button("1. Juntar evento_participante com alunos_participante"):
            st.session_state.step = 1

# 4. Etapa 1: exibir join1 + Botão 2
if st.session_state.step >= 1:
    st.subheader("1- ep ⨝ ap ON ep.idParticipante = ap.idParticipante")
    join1 = evento_participante.merge(alunos_participante, on="idParticipante")
    st.dataframe(join1)
    if st.session_state.step == 1:
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if st.button("2. Agrupar por aluno e filtrar COUNT(ep.idEvento) > 1"):
                st.session_state.step = 2

# 5. Etapa 2: exibir alunos finais + Botão 3
if st.session_state.step >= 2:
    st.subheader("2- ⨝ alunos a ON ap.idAluno = a.idAluno GROUP BY a.idAluno HAVING COUNT(ep.idEvento) > 1")
    agg_alunos = join1.groupby('idAluno').size().reset_index(name='count')
    part_alunos = agg_alunos[agg_alunos['count']>1].merge(alunos, on='idAluno')
    st.dataframe(part_alunos)
    st.subheader("SELECT a.nome, a.email")
    st.dataframe(part_alunos[['nome','email']])
    if st.session_state.step == 2:
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if st.button("3. Juntar evento_participante com professores_participante"):
                st.session_state.step = 3

# 6. Etapa 3: exibir join2 + Botão 4
if st.session_state.step >= 3:
    st.subheader("3- ep ⨝ pp ON ep.idParticipante = pp.idParticipante")
    join2 = evento_participante.merge(professores_participante, on="idParticipante")
    st.dataframe(join2)
    if st.session_state.step == 3:
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if st.button("4. Agrupar por professor e filtrar COUNT(ep.idEvento) > 1"):
                st.session_state.step = 4

# 7. Etapa 4: exibir professores finais + Botão 5
if st.session_state.step >= 4:
    st.subheader("4- ⨝ professores p ON pp.idProfessor = p.idProfessor GROUP BY p.idProfessor HAVING COUNT(ep.idEvento) > 1")
    agg_prof = join2.groupby('idProfessor').size().reset_index(name='count')
    part_prof = agg_prof[agg_prof['count']>1].merge(professores, on='idProfessor')
    st.dataframe(part_prof)
    st.subheader("SELECT p.nome, p.email")
    st.dataframe(part_prof[['nome','email']])
    if st.session_state.step == 4:
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if st.button("5. Exibir resultado final e SQL completo"):
                st.session_state.step = 5

# 8. Etapa 5: exibir resultado final e SQL completo
if st.session_state.step >= 5:
    st.subheader("5- Resultado Final: Aplicação do UNION Entre os dois SELECTS")
    result = pd.concat([part_alunos, part_prof]).reset_index(drop=True)
    st.dataframe(result)
    st.divider()
    st.subheader("Consulta completa")
    sql = '''
    SELECT a.nome, a.email
      FROM evento_participante ep
      JOIN alunos_participante ap ON ep.idParticipante = ap.idParticipante
      JOIN alunos a ON ap.idAluno = a.idAluno
      GROUP BY a.idAluno
      HAVING COUNT(ep.idEvento) > 1
    UNION
    SELECT p.nome, p.email
      FROM evento_participante ep
      JOIN professores_participante pp ON ep.idParticipante = pp.idParticipante
      JOIN professores p ON pp.idProfessor = p.idProfessor
      GROUP BY p.idProfessor
      HAVING COUNT(ep.idEvento) > 1;
    '''
    st.code(sql, language="sql")
    c1,c2,c3 = st.columns([2,1,2])
    with c2:
        if st.button("Clique para recomeçar", key="btnRestart3"):
            st.session_state.step = 0
