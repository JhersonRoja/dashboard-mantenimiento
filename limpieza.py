import psutil
import streamlit as st
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# --- Configuración de la página ---
st.set_page_config(page_title="Dashboard de Mantenimiento", layout="wide")
st.title("🖥️ Dashboard de Mantenimiento del Sistema")
st.markdown("Monitoreo en tiempo real de **CPU, RAM y Disco** con sugerencias automáticas.")

# --- Función para crear gauge ---
def create_gauge(title, value, max_value=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value if isinstance(value, (int, float)) else 0,
        title={'text': title},
        gauge={
            'axis': {'range': [0, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 60], 'color': "lightgreen"},
                {'range': [60, 85], 'color': "yellow"},
                {'range': [85, max_value], 'color': "red"}
            ]
        }
    ))
    fig.update_layout(height=250)
    return fig

# --- Refrescar automáticamente cada 2 segundos ---
# 👆 Eso estaba mal antes, ahora hacemos:


# Configuración del autorefresh
st_autorefresh(interval=2000, limit=None, key="system_refresh")

# Obtener datos
cpu_usage = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory()
disk = psutil.disk_usage('/')

# Layout en columnas
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(create_gauge("CPU (%)", cpu_usage), use_container_width=True)
with col2:
    st.plotly_chart(create_gauge("RAM (%)", ram.percent), use_container_width=True)
with col3:
    st.plotly_chart(create_gauge("Disco (%)", disk.percent), use_container_width=True)

# Recomendaciones dinámicas
st.subheader("🔧 Recomendaciones de Mantenimiento")
if cpu_usage > 80:
    st.warning("⚠️ La CPU está alta. Cierra procesos innecesarios.")
if ram.percent > 90:
    st.warning("⚠️ La memoria RAM está casi llena. Considera cerrar aplicaciones pesadas.")
if disk.percent > 85:
    st.warning("⚠️ El disco está casi lleno. Elimina archivos innecesarios.")
if cpu_usage <= 80 and ram.percent <= 90 and disk.percent <= 85:
    st.success("✅ El sistema funciona correctamente.")