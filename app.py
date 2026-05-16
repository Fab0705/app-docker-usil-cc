import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Panel de Inventario",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Panel de Control de Inventario")
st.markdown("---")

# Inicializar datos en la sesión para que sea interactivo
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame({
        'ID': [1, 2, 3, 4],
        'Producto': ["Taza Blanca 11oz", "Pack de Regalo Personalizado", "Taza Mágica Negra", "Tomatodo de Aluminio"],
        'Categoría': ["Sublimación", "Packs", "Sublimación", "Sublimación"],
        'Precio (S/)': [15.0, 45.0, 25.0, 20.0],
        'Stock': [50, 10, 30, 25]
    })

# --- BARRA LATERAL: Formulario para agregar productos ---
st.sidebar.header("➕ Agregar Nuevo Producto")
with st.sidebar.form("nuevo_producto"):
    nombre = st.text_input("Nombre del producto")
    categoria = st.selectbox("Categoría", ["Sublimación", "Packs", "Textil", "Otros"])
    precio = st.number_input("Precio de venta", min_value=0.0, value=15.0, step=0.5)
    stock = st.number_input("Stock inicial", min_value=0, value=10, step=1)
    submit = st.form_submit_button("Guardar Producto")

    if submit and nombre:
        nuevo_id = st.session_state.inventario['ID'].max() + 1
        nuevo_item = pd.DataFrame({
            'ID': [nuevo_id],
            'Producto': [nombre],
            'Categoría': [categoria],
            'Precio (S/)': [precio],
            'Stock': [stock]
        })
        # Agregar el nuevo item al dataframe
        st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo_item], ignore_index=True)
        st.sidebar.success(f"¡{nombre} agregado al catálogo!")

# --- SECCIÓN SUPERIOR: Métricas clave ---
col1, col2, col3 = st.columns(3)

total_productos = len(st.session_state.inventario)
# Calcular el valor total multiplicando precio por stock
valor_total = (st.session_state.inventario['Precio (S/)'] * st.session_state.inventario['Stock']).sum()
# Contar cuántos productos tienen menos de 15 unidades
stock_bajo = len(st.session_state.inventario[st.session_state.inventario['Stock'] < 15])

col1.metric("Total de Artículos", total_productos)
col2.metric("Valor del Inventario", f"S/ {valor_total:,.2f}")
col3.metric("Alertas (Stock < 15)", stock_bajo, delta="- Revisar", delta_color="inverse")

st.markdown("---")

# --- SECCIÓN PRINCIPAL: Tabla y Gráficos ---
col_tabla, col_grafico = st.columns([1.2, 1])

with col_tabla:
    st.header("📋 Catálogo Actual")
    # Mostrar la tabla sin el índice por defecto de Pandas
    st.dataframe(
        st.session_state.inventario,
        use_container_width=True,
        hide_index=True
    )

with col_grafico:
    st.header("📊 Nivel de Stock")
    # Crear un gráfico de barras con Plotly
    fig = px.bar(
        st.session_state.inventario, 
        x='Producto', 
        y='Stock', 
        color='Categoría',
        text='Stock',
        title="Unidades disponibles por producto"
    )
    # Inclinar los textos del eje X para que se lean mejor
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption(f"Reporte interactivo generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}")