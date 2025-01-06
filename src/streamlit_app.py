import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from main import Finanzas

# Inicializar la clase Finanzas
finanzas = Finanzas()

# Título de la aplicación
st.title("FINANSMART")

# Sección para agregar ingresos y gastos
st.header("Agregar Ingresos y Gastos")

tipo = st.selectbox("Selecciona el tipo", ["ingreso", "gasto"])
monto = st.number_input("Introduce el monto", min_value=0.0, format="%.2f")
descripcion = st.text_input("Introduce una descripción")
categoria = st.text_input("Introduce una categoría")

if st.button("Agregar"):
    if tipo == "ingreso":
        finanzas.agregar_ingreso(monto, descripcion, categoria)
    else:
        finanzas.agregar_gasto(monto, descripcion, categoria)
    st.success(f"{tipo.capitalize()} agregado exitosamente")

# Mostrar balance
balance = finanzas.calcular_balance()
st.header(f"Tu balance mensual es: {balance}")

# Generar gráficos
st.header("Gráficos")
df_ingresos = pd.DataFrame(finanzas.ingresos)
df_gastos = pd.DataFrame(finanzas.gastos)

fig, ax = plt.subplots(4, 1, figsize=(12, 24))

if not df_ingresos.empty:
    sns.barplot(x="descripcion", y="monto", hue="categoria", data=df_ingresos, ax=ax[0], palette="viridis")
    ax[0].set_title("Ingresos")
    ax[0].set_xlabel("Descripción")
    ax[0].set_ylabel("Monto")
else:
    ax[0].text(0.5, 0.5, 'No hay datos de ingresos', horizontalalignment='center', verticalalignment='center')
    ax[0].set_title("Ingresos")

if not df_gastos.empty:
    sns.barplot(x="descripcion", y="monto", hue="categoria", data=df_gastos, ax=ax[1], palette="magma")
    ax[1].set_title("Gastos")
    ax[1].set_xlabel("Descripción")
    ax[1].set_ylabel("Monto")

    # Pie chart para los gastos
    df_gastos_grouped = df_gastos.drop(columns=["fecha"]).groupby("descripcion").sum()
    ax[2].pie(df_gastos_grouped["monto"], labels=df_gastos_grouped.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("magma", len(df_gastos_grouped)))
    ax[2].set_title("Distribución de Gastos")

    # Gráfico de líneas para la evolución de los gastos
    df_gastos['fecha'] = pd.to_datetime(df_gastos['fecha'])
    df_gastos.sort_values('fecha', inplace=True)
    sns.lineplot(x='fecha', y='monto', hue='categoria', data=df_gastos, ax=ax[3], palette="magma", marker='o')
    ax[3].set_title("Evolución de los Gastos")
    ax[3].set_xlabel("Fecha")
    ax[3].set_ylabel("Monto")
else:
    ax[1].text(0.5, 0.5, 'No hay datos de gastos', horizontalalignment='center', verticalalignment='center')
    ax[1].set_title("Gastos")
    ax[2].text(0.5, 0.5, 'No hay datos de gastos', horizontalalignment='center', verticalalignment='center')
    ax[2].set_title("Distribución de Gastos")
    ax[3].text(0.5, 0.5, 'No hay datos de gastos', horizontalalignment='center', verticalalignment='center')
    ax[3].set_title("Evolución de los Gastos")

st.pyplot(fig)

# Mostrar tabla de ingresos y gastos
st.header("Tabla de Ingresos y Gastos")
st.subheader("Ingresos")
st.dataframe(df_ingresos)
st.subheader("Gastos")
st.dataframe(df_gastos)

# Generar recomendaciones
st.header("Recomendaciones")
recomendaciones = finanzas.generar_recomendaciones()
for recomendacion in recomendaciones:
    st.write(f"- {recomendacion}")