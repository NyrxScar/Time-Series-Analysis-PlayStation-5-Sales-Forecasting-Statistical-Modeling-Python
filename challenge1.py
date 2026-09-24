import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. CRIANDO O HISTÓRICO DE VENDAS DO PLAYSTATION 5 (24 MESES)
np.random.seed(465)
meses_historico = pd.date_range(start="2024-09-01", periods=24, freq="MS")

# Tendência de crescimento + variação aleatória
tendencia = np.linspace(8000, 15000, 24)
ruido = np.random.normal(0, 1500, 24)
vendas_historicas = tendencia + ruido

# Desafio 1 - Com a alteração da semente aleatória para 0465 e do desvio
# padrão do ruído de 600 para 1.500 unidades, o histórico de vendas apre-
# sentou maior volatilidade. Essa alteração também modificou o crescimento
# médio mensal calculado pelo modelo, que passou de aproximadamente 254,22
# para 178,94 unidades por mês, representando uma redução de aproximadamen-
# te 29,6%. Como o crescimento médio é utilizado diretamente na projeção, 
# essa redução contribuiu para que as previsões futuras apresentassem valo-
# res inferiores aos obtidos com a configuração original.


# DataFrame
df = pd.DataFrame(
    {"Data": meses_historico, "Vendas": vendas_historicas}
).set_index("Data")

# 2. SIMULANDO A LÓGICA DO ARIMA (Tendência + AutoRegressão)
# Calculamos a taxa média de crescimento mês a mês (Diferenciação d=1)
crescimento_medio = np.diff(df["Vendas"]).mean()
ultima_venda = df["Vendas"].iloc[-1]

# Projetando os próximos 6 meses
meses_futuros = pd.date_range(
    start="2026-09-01", periods=6, freq="MS"
)  # 2026
projeçao_vendas = []
margem_erro = []

venda_atual = ultima_venda
for i in range(1, 7):
    # O valor futuro depende da tendência + variação do mês anterior (ARIMA)
    venda_atual = venda_atual + crescimento_medio + np.random.normal(0, 100)
    projeçao_vendas.append(venda_atual)
    # A incerteza aumenta conforme avançamos no futuro
    margem_erro.append(800 * np.sqrt(i))

df_futuro = pd.DataFrame(
    {"Data": meses_futuros, "Previsão": projeçao_vendas}, index=meses_futuros
)

# 3. EXIBINDO OS RESULTADOS NO TERMINAL
print("--- PROJEÇÃO DE VENDAS (PRÓXIMOS 6 MESES) ---")
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