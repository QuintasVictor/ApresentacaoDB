import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Consulta 4", layout="wide")
st.title("Consulta 6")
st.subheader("Listar os nomes dos organizadores que coordenaram mais de três eventos.")
st.divider()
# Simulação das tabelas como DataFrames
evento_organizador = pd.DataFrame({
    "idEvento":    [1,4,7,8,9,10, 2,5,7,8,9,10, 3,6],
    "idOrganizador": [1,1,1,1,1,1, 2,2,2,2,2,2, 3,3]
})
alunos_organizador = pd.DataFrame({
    "idAluno": [1001,1002,1003],
    "idOrganizador": [1,2,3]
})
alunos = pd.DataFrame({
    "idAluno": list(range(1001, 1004)),
    "nome": ["Aluno 1001","Aluno 1002","Aluno 1003"],
    "email": ["aluno.1001@email.com","aluno.1002@email.com","aluno.1003@email.com"]
})
professores_organizador = pd.DataFrame({
    "idProfessor": [501,502,503],
    "idOrganizador": [1,2,3]
})
professores = pd.DataFrame({
    "idProfessor": [501,502,503,504,505,506],
    "nome": [f"Professor {i}" for i in range(501,507)],
    "email": [f"professor.{i}@email.com" for i in range(501,507)]
})

# Estado da etapa
if 'step' not in st.session_state:
    st.session_state.step = 0

# 1. Tabelas relevantes
st.subheader("Tabelas Relevantes")
with st.expander("evento_organizador"):
    st.dataframe(evento_organizador)
with st.expander("alunos_organizador"):
    st.dataframe(alunos_organizador)
with st.expander("alunos"):
    st.dataframe(alunos)
with st.expander("professores_organizador"):
    st.dataframe(professores_organizador)
with st.expander("professores"):
    st.dataframe(professores)

st.divider()
st.subheader("Objetivo: Vincular organizadores com alunos e professores e aplicar critério de coordenação > 3 eventos")
st.write("Como fazer: agrupar por organizador e filtrar COUNT(idEvento) > 3, unir alunos e professores")

# 3. Botão 1: ep ⨝ ao\ nif st.session_state.step == 0:
c1,c2,c3 = st.columns([1,2,1])
with c2:
    if st.button("1. Juntar evento_organizador com alunos_organizador"):
        st.session_state.step = 1

# 4. Etapa 1: join1 + Botão 2
if st.session_state.step >= 1:
    st.subheader("1- eo ⨝ ao ON eo.idOrganizador = ao.idOrganizador")
    join1 = evento_organizador.merge(alunos_organizador, on="idOrganizador")
    st.dataframe(join1)
    if st.session_state.step == 1:
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if st.button("2. Agrupar por aluno e filtrar COUNT > 3"):
                st.session_state.step = 2

# 5. Etapa 2: alunos finais + Botão 3
if st.session_state.step >= 2:
    st.subheader("2- SELECT a.nome, a.email FROM join1 JOIN alunos ON join1.idAluno = alunos.idAluno GROUP BY a.idAluno HAVING COUNT(eo.idEvento) > 3")
    agg_alunos = join1.groupby('idAluno').size().reset_index(name='count')
    result_alunos = agg_alunos[agg_alunos['count']>3].merge(alunos, on='idAluno')[['nome','email']]
    st.dataframe(result_alunos)
    if st.session_state.step == 2:
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if st.button("3. Juntar evento_organizador com professores_organizador"):
                st.session_state.step = 3

# 6. Etapa 3: join2 + Botão 4
if st.session_state.step >= 3:
    st.subheader("3- eo ⨝ po ON eo.idOrganizador = po.idOrganizador")
    join2 = evento_organizador.merge(professores_organizador, on="idOrganizador")
    st.dataframe(join2)
    if st.session_state.step == 3:
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if st.button("4. Agrupar por professor e filtrar COUNT > 3"):
                st.session_state.step = 4

# 7. Etapa 4: professores finais + Botão 5
if st.session_state.step >= 4:
    st.subheader("4- SELECT p.nome, p.email FROM join2 JOIN professores p ON join2.idProfessor = p.idProfessor GROUP BY p.idProfessor HAVING COUNT(eo.idEvento) > 3")
    agg_prof = join2.groupby('idProfessor').size().reset_index(name='count')
    result_prof = agg_prof[agg_prof['count']>3].merge(professores, on='idProfessor')[['nome','email']]
    st.dataframe(result_prof)
    if st.session_state.step == 4:
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if st.button("5. Exibir resultado final e SQL completo"):
                st.session_state.step = 5

# 8. Etapa 5: resultado final e SQL completo
if st.session_state.step >= 5:
    st.subheader("5- Resultado Final: Organizadores com >3 eventos")
    final = pd.concat([result_alunos, result_prof]).reset_index(drop=True)
    st.dataframe(final)
    st.divider()
    st.subheader("Consulta completa")
    sql = '''
    SELECT a.nome, a.email
      FROM evento_organizador eo
      JOIN alunos_organizador ao ON eo.idOrganizador = ao.idOrganizador
      JOIN alunos a ON ao.idAluno = a.idAluno
      GROUP BY a.idAluno
      HAVING COUNT(eo.idEvento) > 3
    UNION
    SELECT p.nome, p.email
      FROM evento_organizador eo
      JOIN professores_organizador po ON eo.idOrganizador = po.idOrganizador
      JOIN professores p ON po.idProfessor = p.idProfessor
      GROUP BY p.idProfessor
      HAVING COUNT(eo.idEvento) > 3;
    '''
    st.code(sql, language="sql")
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        if st.button("Clique para recomeçar", key="btnRestart4"):
            st.session_state.step = 0
