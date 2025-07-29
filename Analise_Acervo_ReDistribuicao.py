import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_redistrbuicao = pd.read_excel('Processos para Redistribuição Direito Público.xlsx')

#print(df_redistrbuicao.head())
df_redistrbuicao.columns = df_redistrbuicao.columns.str.strip()
quantitativo_geral = df_redistrbuicao['Processo'].nunique()
#print(f"Quantitativo Geral de Processos para Redistribuição: {quantitativo_geral}")


sistema_counts = df_redistrbuicao['Sistema'].value_counts()
#print("\nQuantitativo por Sistema:")
#print(sistema_counts)

# 3. Quantitativo por Relator
relator_counts = df_redistrbuicao['Relator'].value_counts()
print("\nQuantitativo por Relator:")
print(relator_counts)


# Quantitativo por Relator dentro de cada Sistema (tabela cruzada)
relator_sistema = df_redistrbuicao.groupby(['Sistema', 'Relator'])['Processo'].count().unstack(fill_value=0)
relator_sistema['Total por Sistema'] = relator_sistema.sum(axis=1) #Adiciona coluna "Total por Relator"
relator_sistema.loc['Total Geral'] = relator_sistema.sum(numeric_only=True) # Adiciona linha "Total por Relator"

print("\nQuantitativo por Relator em cada Sistema (com totais):")
print(relator_sistema)


import pandas as pd
import matplotlib.pyplot as plt

# === 1. Carregamento dos dados ===
arquivo = "Processos para Redistribuição Direito Público.xlsx"
df = pd.read_excel(arquivo, sheet_name="Painel Desempenho")
df.columns = df.columns.str.strip()

# === 2. Agrupamento e totais ===
tabela = df.groupby(['Sistema', 'Relator'])['Processo'].count().unstack(fill_value=0)
tabela['Total por Sistema'] = tabela.sum(axis=1)
tabela.loc['Total Geral'] = tabela.sum(numeric_only=True)

# === 3. Exporta a tabela para Excel com estilo ===
tabela.style.format("{:.0f}").set_caption("Processos por Relator e Sistema") \
    .background_gradient(axis=1, cmap="Blues") \
    .to_excel("tabela_processos_por_relator.xlsx", engine='openpyxl')

# === 4. Gráfico com barras horizontais e rótulos ===

# Remove a linha "Total Geral" e a coluna "Total por Sistema" para o gráfico
dados_grafico = tabela.drop("Total Geral", errors="ignore").drop(columns="Total por Sistema", errors="ignore")

# Cria figura
fig, ax = plt.subplots(figsize=(14, 8))

# Cores diferentes para cada relator
colors = plt.cm.tab20.colors

# Plot empilhado horizontal
bottom = [0] * len(dados_grafico)
sistemas = dados_grafico.index.tolist()

for i, relator in enumerate(dados_grafico.columns):
    valores = dados_grafico[relator]
    ax.barh(sistemas, valores, left=bottom, label=relator, color=colors[i % len(colors)])

    # Adiciona rótulos
    for j, val in enumerate(valores):
        if val > 0:
            ax.text(bottom[j] + val / 2, j, str(val), ha='center', va='center', fontsize=8, color='white')
    bottom = [bottom[k] + valores[k] for k in range(len(valores))]

# Estilização do gráfico
ax.set_xlabel("Quantidade de Processos")
ax.set_title("Distribuição de Processos por Relator e Sistema")
ax.legend(title="Relator", bbox_to_anchor=(1.05, 1), loc='upper left')
ax.set_ylabel("Sistema")

# === 5. Adiciona tabela descritiva abaixo do gráfico ===
# Converte a tabela para string formatada
tabela_exibicao = tabela.copy().astype(str)
# Formata linha por linha para inserir na tabela do matplotlib
cell_text = [tabela_exibicao.iloc[i].tolist() for i in range(len(tabela_exibicao))]
col_labels = tabela_exibicao.columns.tolist()
row_labels = tabela_exibicao.index.tolist()

# Adiciona a tabela na parte inferior do gráfico
plt.table(cellText=cell_text,
          colLabels=col_labels,
          rowLabels=row_labels,
          cellLoc='center',
          rowLoc='center',
          loc='bottom',
          bbox=[0, -0.6, 1, 0.5])  # ajusta posição e tamanho da tabela

# Ajusta layout para não cortar nada
plt.subplots_adjust(left=0.1, bottom=0.35, right=0.75)

# Exporta imagem
plt.savefig("grafico_tabela_processos.png", dpi=300, bbox_inches='tight')
plt.show()
