# =============================================================================
# Proyecto: Análisis de gastos de mantenimiento (2020 - 2023)
# Autores: Israel Arias, Martha Enriquez, Karolay Hernandéz
# Descripción: Análisis interactivo de datos de mantenimiento
# =============================================================================

import streamlit as st           # Librería para app web interactiva
import pandas as pd              # Manejo de datos tipo Excel/CSV
import numpy as np               # Estadística básica
import matplotlib.pyplot as plt  # Librería de visualización (asegúrate que esté en requirements.txt)

# ------------------------------
# CONFIGURACIÓN INICIAL DE LA APP
# ------------------------------
st.set_page_config(page_title="Análisis de gastos de mantenimiento", layout="wide")

# ------------------------------
# ENCABEZADO CON IMÁGENES
# ------------------------------
col1, col2, col3 = st.columns([1, 1, 1])  # Tres columnas de igual ancho

with col1:
    st.image("imagen1 (1).png", use_column_width=True, caption="ESPE")

with col2:
    st.image("MANT.jpeg", use_column_width=True, caption="Innovativa")

with col3:
    st.image("imagen2.png", use_column_width=True, caption="Mantenimiento")

# ------------------------------
# TÍTULO Y DESCRIPCIÓN
# ------------------------------
st.title("📊 Análisis de gastos de mantenimiento (2020-2023)")
st.markdown("Este dashboard analiza los **gastos de mantenimiento** por equipo, "
            "considerando gastos **reactivos, fallas, mejoras, preventivos y CBM**. "
            "Se aplican conceptos de **estadística descriptiva** y **matemática básica**.")

# ------------------------------
# CARGA DE DATOS DESDE EXCEL
# ------------------------------
@st.cache_data
def cargar_datos():
    # Leer archivo Excel
    df = pd.read_excel("Gasto x Equipo 2020 a 2023 (PYTHON).xlsx")
    
    # Renombrar columnas importantes
    df = df.rename(columns={
        "Descripción Equipo": "Descripcion",
        "Fecha Instal.": "Fecha_Instalacion",
        "GOT Reactivas (USD)": "Reactivas",
        "GOT A Falla (USD)": "Falla",
        "GOT Mejoras (USD)": "Mejoras",
        "GOT Preven. (USD)": "Preventivo",
        "GOT CBM (USD)": "CBM"
    })
    
    # Crear columna de gasto total
    df["Gasto_Total"] = df[["Reactivas", "Falla", "Mejoras", "Preventivo", "CBM"]].sum(axis=1)
    
    # Crear columna de año (extraída de la fecha de instalación)
    df["Año"] = pd.to_datetime(df["Fecha_Instalacion"], errors="coerce").dt.year
    
    return df

df = cargar_datos()

# ------------------------------
# PANEL LATERAL DE OPCIONES
# ------------------------------
st.sidebar.header("⚙️ Opciones de análisis")

equipo_sel = st.sidebar.selectbox("Seleccione un equipo:", df["Equipo"].unique())
tipos_gasto = st.sidebar.multiselect(
    "Seleccione tipos de gasto a comparar:",
    ["Reactivas", "Falla", "Mejoras", "Preventivo", "CBM"],
    default=["Falla", "Preventivo"]
)

# ------------------------------
# ESTADÍSTICA DESCRIPTIVA
# ------------------------------
st.subheader("📌 Estadística básica del gasto total (todos los equipos)")

gastos = df["Gasto_Total"].values
st.write(f"- Promedio: {np.mean(gastos):,.2f} USD")
st.write(f"- Mediana: {np.median(gastos):,.2f} USD")
st.write(f"- Desviación estándar: {np.std(gastos):,.2f} USD")
st.write(f"- Máximo: {np.max(gastos):,.2f} USD")
st.write(f"- Mínimo: {np.min(gastos):,.2f} USD")

# ------------------------------
# VISUALIZACIÓN 1: Top equipos
# ------------------------------
st.subheader("🏆 Top 10 equipos con mayor gasto total")
top_equipos = df.groupby("Descripcion")["Gasto_Total"].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(8, 5))
top_equipos.plot(kind="barh", color="darkred", ax=ax)
ax.set_xlabel("Gasto total (USD)")
ax.set_title("Top 10 equipos más costosos")
st.pyplot(fig)

# ------------------------------
# VISUALIZACIÓN 2: Distribución por tipo de gasto
# ------------------------------
st.subheader("📊 Distribución de gastos por tipo (global)")

gastos_tipo = df[tipos_gasto].sum()

fig, ax = plt.subplots()
gastos_tipo.plot(kind="bar", color=["purple", "orange", "green", "blue", "gray"], ax=ax)
ax.set_ylabel("Monto total (USD)")
ax.set_title("Distribución de gastos seleccionados")
st.pyplot(fig)

# ------------------------------
# VISUALIZACIÓN 3: Serie temporal de gastos
# ------------------------------
st.subheader("📈 Evolución temporal de los gastos (según año de instalación)")

ts = df.groupby("Año")["Gasto_Total"].sum().sort_index()

fig, ax = plt.subplots()
ax.plot(ts.index, ts.values, marker="o", color="darkblue")
ax.fill_between(ts.index, ts.values*0.9, ts.values*1.1, alpha=0.2, color="blue")
ax.set_xlabel("Año de instalación")
ax.set_ylabel("Gasto total (USD)")
ax.set_title("Serie temporal de gastos")
st.pyplot(fig)

# ------------------------------
# TABLA DETALLADA DEL EQUIPO
# ------------------------------
st.subheader(f"📋 Detalle del equipo seleccionado: {equipo_sel}")
st.dataframe(df[df["Equipo"] == equipo_sel])

# ------------------------------
# CONCLUSIONES
# ------------------------------
st.subheader("✅ Conclusiones")
st.markdown("""
1. El **gasto total** se compone de 5 categorías: Reactivas, Fallas, Mejoras, Preventivo y CBM.  
2. Algunos equipos presentan un gasto acumulado mucho mayor que otros (se reflejan en el **Top 10**).  
3. El mantenimiento preventivo y las fallas representan la mayor parte del gasto global.  
4. Con estadística básica (promedio, mediana, desviación estándar) se puede tener un panorama inicial del gasto.  
""")



