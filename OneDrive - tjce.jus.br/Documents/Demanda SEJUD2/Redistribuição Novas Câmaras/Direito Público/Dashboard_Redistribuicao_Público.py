import streamlit as st
import pandas as pd
import plotly.express as px

# === Configurações iniciais ===
st.set_page_config(page_title="Dashboard - Redistribuição Direito Público", layout="wide")

# === Carrega os dados ===
arquivo = "Processos para Redistribuição Direito Público.xlsx"
df = pd.read_excel(arquivo, sheet_name="Painel Desempenho")
df.columns = df.columns.str.strip()

# === Agrupamento ===
df_agg = df.groupby(['Sistema', 'Relator']).agg({'Processo': 'count'}).reset_index()
df_agg.rename(columns={'Processo': 'Quantidade'}, inplace=True)

# === Título geral ===
st.title("📊 Dashboard – Redistribuição Direito Público")

# === Filtros ===
col1, col2 = st.columns(2)

with col1:
    relatores = st.multiselect(
        "Filtrar por Gabinete:",
        options=sorted(df_agg['Relator'].unique()),
        default=None
    )

with col2:
    sistemas = st.multiselect(
        "Filtrar por Sistema:",
        options=sorted(df_agg['Sistema'].unique()),
        default=None
    )

# === Filtragem ===
df_filtrado = df_agg.copy()
if relatores:
    df_filtrado = df_filtrado[df_filtrado['Relator'].isin(relatores)]
if sistemas:
    df_filtrado = df_filtrado[df_filtrado['Sistema'].isin(sistemas)]

# === Gráfico ===
st.subheader("📈 Quantidade de Processos Redistribuição por Gabinete e Sistema")
fig = px.bar(
    df_filtrado,
    x='Quantidade',
    y='Sistema',
    color='Relator',
    orientation='h',
    text='Quantidade',
)

# Centraliza os rótulos
fig.update_traces(textposition='inside')

fig.update_layout(
    barmode='stack',
    yaxis={'categoryorder': 'total ascending'}
)
st.plotly_chart(fig, use_container_width=True)

# === Tabela Detalhada Agrupada com Totais ===
st.subheader("📋 Detalhamento Quantitativo")

# Agrupa novamente por Relator e Sistema
df_grouped = df_filtrado.groupby(['Relator', 'Sistema'], as_index=False).agg({'Quantidade': 'sum'})

# Calcula o total geral
total_geral = pd.DataFrame({
    'Relator': ['TOTAL GERAL'],
    'Sistema': [''],
    'Quantidade': [df_grouped['Quantidade'].sum()]
})

# Concatena a tabela com o total
df_final = pd.concat([df_grouped, total_geral], ignore_index=True)

# Exibe a tabela formatada
st.dataframe(df_final, use_container_width=True)



