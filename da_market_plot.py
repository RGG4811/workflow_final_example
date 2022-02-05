#!/usr/bin/python
"""
 Author: Roldán Gutiérrez García
 Email: <roldan.gutierrez@alumnos.unican.es><roldanggarcia@gmail.com>
 Created: 04/02/2021
 Description: Reads da_market_data.csv file containing OMIE day ahead hourly prices for each day and plots a graph comparing
    month averages through different systems.
"""
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("da_market_data.csv", parse_dates=["fecha", "fecha_actualizacion"])

df.set_index("fecha", inplace=True)
df = df.groupby([pd.Grouper(freq="M"), "sistema"])["precio"].agg(["mean", "max", "min"])

df.reset_index(inplace=True)
df = df.loc[(df["fecha"].dt.year == 2021) & (~df["sistema"].isin(["SICI", "SUD", "NORD", "CNOR", "CSUD", "SARD", "CALA"]))]

# configuración de la gráfica
fig, ax = plt.subplots(figsize=(12, 6))

ax.grid(which="major", axis="y", color="#758D99", alpha=0.6, zorder=1)

for country in df["sistema"].unique():
    ax.plot(df[df["sistema"] == country]["fecha"].dt.month,
            df[df["sistema"] == country]["mean"],
            alpha=0.8,
            linewidth=3)
    
# adición de línea y tag
ax.plot([0.12, 0.9],
       [0.98, 0.98],
       transform=fig.transFigure,
       clip_on=False,
       color="#E3120B",
       linewidth=0.6)
ax.add_patch(plt.Rectangle((0.12, 0.98),
                          0.04,
                          -0.02,
                          facecolor="#E3120B",
                          transform=fig.transFigure,
                          clip_on=False,
                          linewidth=0))

# título, subtítulo y fuente
ax.text(x=0.12, y=0.93, s="Precios medios mercado electricidad Europa", 
        transform=fig.transFigure, ha="left", fontsize=13, weight="bold", alpha=0.8)
ax.text(x=0.12, y=0.89, s="Precios medios del mercado spot por mes, comparación por países", 
        transform=fig.transFigure, ha="left", fontsize=11,  alpha=0.8)
ax.text(x=0.12, y=0.01, 
        s="""Fuente: "Aldro" via https://zenodo.org/record/5900902#.YfxGpurMKCp""", 
        transform=fig.transFigure, ha="left", fontsize=9,  alpha=0.7)

# eliminación de líneas exteriores del gráfico
ax.spines["top"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)

# texto de los ejes y leyenda
plt.xlabel("Mes")
plt.ylabel("Precio medio mercado spot (€/MWh)")
plt.legend(df["sistema"].unique(), title="Sistema", bbox_to_anchor=(1, 1.2))

plt.show()

fig.savefig("da_avg_price_plot.png")
