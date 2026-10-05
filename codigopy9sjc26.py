import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Consulta de Notas - Biologia", page_icon="🧬")

@st.cache_data
def carregar_dados():
    # Atualizado para o nome do arquivo do 3º Trimestre
    df = pd.read_excel("Atividades e participação_FatorMultiplicação1 - 3ºTri.xlsx", sheet_name=0, header=2)
    
    # Limpa espaços em branco dos nomes das colunas
    df.columns = [str(c).strip() for c in df.columns]
    
    # Seleciona as colunas necessárias (Ajuste os nomes caso as colunas na nova planilha sejam diferentes)
    df = df[['RA', 'Alunos', 'Turma', 'Média']]
    
    # Remove linhas sem RA
    df = df.dropna(subset=['RA'])
    
    # Trata o formato do RA
    df['RA'] = df['RA'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    
    return df

df = carregar_dados()

st.title("🧬 Consulta de Notas - Bio (3ºTri)")
st.write("Digite seu RA para visualizar sua "nota de participação". **Atenção: digite o RA sem o zero no início do número.**")

# Entrada do RA como senha
ra_aluno = st.text_input("Digite o seu RA:", type="password")

if st.button("Ver Nota"):
    if ra_aluno:
        ra_digitado = ra_aluno.strip()
        aluno_encontrado = df[df['RA'] == ra_digitado]
        
        if not aluno_encontrado.empty:
            nome = aluno_encontrado.iloc[0]['Alunos']
            turma = aluno_encontrado.iloc[0]['Turma']
            nota = aluno_encontrado.iloc[0]['Média']
            
            nota_formatada = f"{float(nota):.1f}" if pd.notna(nota) else "Sem nota"
            
            st.success(f"Aluno(a): {nome} - Turma: {turma}")
            st.metric(label="Sua nota de atividades", value=nota_formatada)
        else:
            st.error("RA não encontrado. Verifique se o número foi digitado corretamente (lembre-se de não colocar o zero no início).")
    else:
        st.warning("Por favor, digite um RA válido.")
