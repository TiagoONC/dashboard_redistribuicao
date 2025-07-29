import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === 1. Carregamento dos dados ===
arquivo = "Processos para Redistribuição Direito Público.xlsx"
df = pd.read_excel(arquivo, sheet_name="Painel Desempenho")
df.columns = df.columns.str.strip()

# === 2. Agrupamento e totais ===
tabela = df.groupby(['Sistema', 'Relator'])['Processo'].count().unstack(fill_value=0)
tabela['Total por Sistema'] = tabela.sum(axis=1)
tabela.loc['Total Geral'] = tabela.sum(numeric_only=True)

# === 3. Exporta tabela estilizada ===
tabela.style.format("{:.0f}").set_caption("Processos por Relator e Sistema") \
    .background_gradient(axis=1, cmap="Blues") \
    .to_excel("tabela_processos_por_relator.xlsx", engine='openpyxl')

# === 4. Gráfico com mais espaçamento no SAJ-SG ===

# Remove totais para o gráfico
dados_grafico = tabela.drop("Total Geral", errors="ignore").drop(columns="Total por Sistema", errors="ignore")

# Reordena os sistemas para manter SAJ-SG onde está
sistemas = dados_grafico.index.tolist()
valores_plot = dados_grafico.values

# Cores
colors = plt.cm.tab20.colors
n_relatores = dados_grafico.shape[1]

# Define posições Y com espaçamento maior para SAJ-SG
y_positions = []
espacamento_padrao = 1.0
espacamento_saj = 2.0
y_atual = 0
for sistema in sistemas:
    y_positions.append(y_atual)
    if sistema == "SAJ-SG":
        y_atual += espacamento_saj
    else:
        y_atual += espacamento_padrao

# Cria figura
fig, ax = plt.subplots(figsize=(14, 8))
bottom = np.zeros(len(sistemas))

for i, relator in enumerate(dados_grafico.columns):
    valores = dados_grafico[relator].values
    ax.barh(y_positions, valores, left=bottom, height=0.8, label=relator, color=colors[i % len(colors)])
    # Rótulos
    for j, val in enumerate(valores):
        if val > 0:
            pos_x = bottom[j] + val * 0.6 if sistemas[j] == 'SAJ-SG' else bottom[j] + val / 2
            ax.text(pos_x, y_positions[j], str(val), va='center', ha='center', fontsize=8, color='white')
    bottom += valores

# Rótulos Y
ax.set_yticks(y_positions)
ax.set_yticklabels(sistemas)
ax.set_xlabel("Quantidade de Processos")
ax.set_title("Distribuição de Processos por Relator e Sistema")
ax.legend(title="Relator", bbox_to_anchor=(1.05, 1), loc='upper left')

# === 5. Tabela descritiva abaixo ===
tabela_str = tabela.copy().astype(str)
cell_text = [tabela_str.iloc[i].tolist() for i in range(len(tabela_str))]
col_labels = tabela_str.columns.tolist()
row_labels = tabela_str.index.tolist()

plt.table(cellText=cell_text,
          colLabels=col_labels,
          rowLabels=row_labels,
          cellLoc='center',
          rowLoc='center',
          loc='bottom',
          bbox=[0, -0.6, 1, 0.5])

plt.subplots_adjust(left=0.1, bottom=0.35, right=0.75)
plt.savefig("grafico_tabela_processos.png", dpi=300, bbox_inches='tight')
plt.show()
