import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. CRIANDO O HISTÓRICO DE VENDAS DO PLAYSTATION 5 (24 MESES)
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

# 2. SIMULANDO A LÓGICA DO ARIMA (Tendência + AutoRegressão)
# Calculamos a taxa média de crescimento mês a mês (Diferenciação d=1)
crescimento_medio = np.diff(df["Vendas"]).mean()
ultima_venda = df["Vendas"].iloc[-1]

# Projetando os próximos 12 meses
meses_futuros = pd.date_range(
    start="2026-09-01", periods=12, freq="MS"
)  # 2026-2027

projeçao_vendas = []
margem_erro = []

venda_atual = ultima_venda

for i in range(1, 13):
    # O valor futuro depende da tendência + variação do mês anterior (ARIMA)
    venda_atual = venda_atual + crescimento_medio + np.random.normal(0, 100)
    projeçao_vendas.append(venda_atual)

    # Desafio 2 - A incerteza aumenta conforme avançamos no horizonte da
    # previsão. No 1º mês, a margem de erro é de 800 unidades e, no 12º
    # mês, chega a aproximadamente 2.771 unidades. Isso demonstra que,
    # quanto mais distante o período previsto, maior é a margem de incerteza.

    margem_erro.append(800 * np.sqrt(i))

df_futuro = pd.DataFrame(
    {"Data": meses_futuros, "Previsão": projeçao_vendas}, index=meses_futuros
)

# 3. EXIBINDO OS RESULTADOS NO TERMINAL
print("--- PROJEÇÃO DE VENDAS (PRÓXIMOS 12 MESES) ---")

for data, valor in zip(df_futuro["Data"], df_futuro["Previsão"]):
    print(
        f"Mês: {data.strftime('%m/%Y')} | Previsão: {int(valor):,} unidades".replace(
            ",", "."
        )
    )

# 4. GERANDO O GRÁFICO
plt.figure(figsize=(10, 5))

plt.plot(
    df.index,
    df["Vendas"],
    label="Histórico de Vendas (PS5)",
    color="#003791",
    marker="o",
)

plt.plot(
    df_futuro.index,
    df_futuro["Previsão"],
    label="Projeção ARIMA Simplificada",
    color="#d62728",
    linestyle="--",
    marker="o",
)

# Margem de Confiança (Sombra)
limite_superior = df_futuro["Previsão"] + margem_erro
limite_inferior = df_futuro["Previsão"] - margem_erro

plt.fill_between(
    df_futuro.index,
    limite_inferior,
    limite_superior,
    color="#ff9896",
    alpha=0.4,
    label="Margem de Incerteza",
)

plt.title("Simulação de Previsão de Vendas - PlayStation 5", fontsize=12)
plt.xlabel("Mês")
plt.ylabel("Unidades Vendidas")
plt.legend()
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.show()