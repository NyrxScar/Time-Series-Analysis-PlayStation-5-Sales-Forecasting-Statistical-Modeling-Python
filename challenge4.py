import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Criando o histórico de vendas do PlayStation 5 (24 meses)
np.random.seed(42)
meses_historico = pd.date_range(start="2024-09-01", periods=24, freq="MS")

# Tendência de crescimento + variação aleatória
tendencia = np.linspace(8000, 15000, 24)
ruido = np.random.normal(0, 600, 24)
vendas_historicas = tendencia + ruido

# DataFrame
df = pd.DataFrame(
    {"Data": meses_historico, "Vendas": vendas_historicas}
).set_index("Data")

# 2. Simulando a lógica do ARIMA
# Calculamos a taxa média de crescimento mês a mês
crescimento_medio = np.diff(df["Vendas"]).mean()
ultima_venda = df["Vendas"].iloc[-1]

    # Desafio 4 - Foram simulados três cenários para comparar diferentes
    # possibilidades de crescimento das vendas. O Cenário Base mantém as
    # regras dos Desafios 2 e 3, com projeção de 12 meses e aumento sazonal
    # de 35% em Novembro e Dezembro. O Cenário Otimista utiliza um crescimento
    # médio 15% superior ao histórico, enquanto o Cenário Pessimista utiliza
    # um crescimento médio 25% inferior. A margem de incerteza é apresentada
    # somente para o Cenário Base, permitindo visualizar a variação esperada
    # das previsões ao longo do horizonte projetado.

meses_futuros = pd.date_range(
    start="2026-09-01", periods=12, freq="MS"
)

# Utilizamos a mesma variação aleatória nos três cenários
# para tornar a comparação entre eles mais consistente.
variacoes_aleatorias = np.random.normal(0, 100, 12)

# Listas para armazenar as projeções
cenario_base = []
cenario_otimista = []
cenario_pessimista = []
margem_erro = []

# Taxas de crescimento dos cenários
crescimento_base = crescimento_medio
crescimento_otimista = crescimento_medio * 1.15
crescimento_pessimista = crescimento_medio * 0.75

# Valores iniciais
venda_base = ultima_venda
venda_otimista = ultima_venda
venda_pessimista = ultima_venda

for i in range(1, 13):

    # Cenário Base
    venda_base = (
        venda_base
        + crescimento_base
        + variacoes_aleatorias[i - 1]
    )

    # Desafio 3 aplicado ao cenário base:
    # Novembro e dezembro recebem aumento sazonal de 35%.
    if meses_futuros[i - 1].month in [11, 12]:
        venda_base = venda_base * 1.35

    cenario_base.append(venda_base)

    # Margem de incerteza do cenário base
    margem_erro.append(800 * np.sqrt(i))

    # Cenário Otimista
    venda_otimista = (
        venda_otimista
        + crescimento_otimista
        + variacoes_aleatorias[i - 1]
    )

    cenario_otimista.append(venda_otimista)

    # Cenário Pessimista
    venda_pessimista = (
        venda_pessimista
        + crescimento_pessimista
        + variacoes_aleatorias[i - 1]
    )

    cenario_pessimista.append(venda_pessimista)


# DataFrame com os cenários
df_cenarios = pd.DataFrame(
    {
        "Data": meses_futuros,
        "Cenário Base": cenario_base,
        "Cenário Otimista": cenario_otimista,
        "Cenário Pessimista": cenario_pessimista,
    },
    index=meses_futuros,
)


# 3. Exibindo os resultados
print("--- Simulação de Cenários (Próximos 12 Meses) ---")

for data in meses_futuros:
    print(
        f"Mês: {data.strftime('%m/%Y')} | "
        f"Base: {int(df_cenarios.loc[data, 'Cenário Base']):,} | "
        f"Otimista: {int(df_cenarios.loc[data, 'Cenário Otimista']):,} | "
        f"Pessimista: {int(df_cenarios.loc[data, 'Cenário Pessimista']):,}"
    .replace(",", ".")
    )


# 4. Gerando Dashboard Comparativo

plt.figure(figsize=(12, 6))

# Histórico de vendas
plt.plot(
    df.index,
    df["Vendas"],
    label="Histórico de Vendas (PS5)",
    color="#003791",
    marker="o",
)

# Cenário Base
plt.plot(
    df_cenarios.index,
    df_cenarios["Cenário Base"],
    label="Cenário Base",
    color="#d62728",
    linestyle="--",
    marker="o",
)

# Cenário Otimista
plt.plot(
    df_cenarios.index,
    df_cenarios["Cenário Otimista"],
    label="Cenário Otimista",
    color="green",
    marker="o",
)

# Cenário Pessimista
plt.plot(
    df_cenarios.index,
    df_cenarios["Cenário Pessimista"],
    label="Cenário Pessimista",
    color="orange",
    marker="o",
)


# Margem de incerteza do Cenário Base
limite_superior = df_cenarios["Cenário Base"] + margem_erro
limite_inferior = df_cenarios["Cenário Base"] - margem_erro

plt.fill_between(
    df_cenarios.index,
    limite_inferior,
    limite_superior,
    color="#ff9896",
    alpha=0.35,
    label="Margem de Incerteza - Cenário Base",
)


plt.title(
    "Simulação de Cenários de Vendas - PlayStation 5",
    fontsize=12
)
plt.xlabel("Mês")
plt.ylabel("Unidades Vendidas")
plt.legend()
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.show()

