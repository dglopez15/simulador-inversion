import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Función para elegir activo
def elegir_activo(key_suffix=""):
    activos = {
        "Airbus 🛫": (0.112, 0.14),
        "Alphabet (Google) 🔎": (0.22, 0.1024),
        "Amazon 📦": (0.27, 0.16),
        "Apple 🍏": (0.298, 0.1024),
        "Aston Martin 🏎️": (-0.4321, 0.25),
        "Bitcoin ₿": (1.761, 2.25),
        "Cacao 🍫": (0.0961, 0.0628),
        "Ferrari 🐎": (0.273, 0.0144),
        "IBEX 35 🇪🇸": (0.07, 0.04),
        "Johnson & Johnson 🧪": (0.09, 0.03),
        "Mercedes-Benz 🚘": (0.021, 0.0225),
        "Microsoft 🖥️": (0.174, 0.0625),
        "NVIDIA 💻": (0.472, 0.3025),
        "Oro 🟡": (0.102, 0.0361),
        "Petróleo (WTI) 🛢️": (0.12, 0.25),
        "S&P 500 📈": (0.09, 0.0324),
        "Tesla 🚗": (0.3379, 0.25),
        "TSMC (Taiwan Semi) 🔧": (0.1895, 0.10),
        "Volkswagen 🦁": (-0.0368, 0.01),
    }
    nombre = st.selectbox("Selecciona un activo:", list(activos.keys()), key=f"activo_select_{key_suffix}")
    return activos[nombre], nombre


# Simulación
def calcular_dinero_total(anios, cantidad_inicial, ingresos_anuales, rentabilidad_media, varianza, seed, nivel_aleatoriedad):
    np.random.seed(seed)
    meses = anios * 12
    saldo = [cantidad_inicial]
    deposito_total = [cantidad_inicial]

    mu_mensual = rentabilidad_media / 12
    sigma_mensual = np.sqrt(varianza) / np.sqrt(12) * (nivel_aleatoriedad / 5)  # Escala de 1 a 10 (5 = normal)

    for mes in range(1, meses + 1):
        anio_actual = (mes - 1) // 12
        ingreso_mensual = ingresos_anuales[anio_actual]

        rendimiento = np.random.normal(mu_mensual, sigma_mensual)
        nuevo_saldo = saldo[-1] * (1 + rendimiento) + ingreso_mensual

        saldo.append(nuevo_saldo)
        deposito_total.append(deposito_total[-1] + ingreso_mensual)

    return saldo, deposito_total


# === INTERFAZ WEB ===
# Estilo para diseño responsivo
st.markdown(
    """
    <style>
    /* Fuente para todo el body */
    html, body, [class*="css"]  {
        font-family: 'Futura', sans-serif !important;
    }
    /* Opcional: para los sliders y selectbox */
    .stSlider > div > div > div > div, 
    .stSelectbox > div > div > div > div {
        font-family: 'Futura', sans-serif !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        /* Estilo adaptativo: ancho fluido con margen razonable */
        .main .block-container {
            max-width: 1600px;
            padding-left: 3rem;
            padding-right: 3rem;
        }

        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            h1 {
                font-size: 1.6em !important;
            }
        }

        h1 {
            text-align: center;
            font-size: 2.8em;
        }
    </style>
""", unsafe_allow_html=True)


# Título moderno y centrado
st.markdown("""
    <h1 style='font-weight: 600; margin-top: 0.5em; color: #5dade2;'>
        SIMULADOR DE INVERSIÓN
    </h1>
    <hr style='border: none; height: 2px; background-color: #d6eaf8;'/>
""", unsafe_allow_html=True)

nivel_aleatoriedad = st.slider("Nivel de aleatoriedad (1 = baja, 10 = alta)", 1, 10, 5)

num_escenarios = st.slider("¿Cuántos escenarios quieres comparar?", 1, 3, 1)
seed = st.number_input("Semilla aleatoria (fija para comparar resultados):", value=np.random.randint(0, 100000))

resultados = []
max_anios = 0

for i in range(1, num_escenarios + 1):
    st.header(f"Escenario {i}")
    anios = st.number_input(f"Años de inversión)", min_value=1, max_value=50, value=20, key=f"a_{i}")
    cantidad_inicial = st.number_input(f"Capital inicial (€)", min_value=0.0, value=100.0, key=f"c_{i}")

    ingresos_anuales = []
    bloques = (anios + 4) // 5
    for j in range(bloques):
        inicio = j * 5 + 1
        fin = min((j + 1) * 5, anios)
        ingreso = st.number_input(f"Ingreso mensual de años {inicio}-{fin} (€)", value=300.0, key=f"ing_{i}_{j}")
        ingresos_anuales.extend([ingreso] * (fin - inicio + 1))

    (media, varianza), nombre_activo = elegir_activo(key_suffix=i)

    saldo, deposito_total = calcular_dinero_total(anios, cantidad_inicial, ingresos_anuales, media, varianza, seed, nivel_aleatoriedad)
    resultados.append((saldo, deposito_total, nombre_activo, f"Escenario {i}"))
    max_anios = max(max_anios, anios)

# === GRÁFICO ===
if resultados:
    st.subheader("📈 Evolución del Capital")

    meses = np.arange(0, max_anios * 12 + 1)
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='none')  # Fondo figura transparente
    ax.set_facecolor("none")  # Fondo área del gráfico transparente

    for saldo, deposito_total, nombre_activo, etiqueta in resultados:
        linea_principal, = ax.plot(
            meses, saldo,
            label=f"{etiqueta} ({nombre_activo})",
            linewidth=2.5
        )
        ax.plot(
            meses, deposito_total,
            linestyle=":",
            color=linea_principal.get_color(),
            alpha=0.4,
            linewidth=2
        )

    ax.set_xlabel("Meses")
    ax.set_ylabel("Capital (€)")
    ax.grid(False)

    # Colores blancos en los ejes
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')

    # Eliminar marco superior y derecho
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Leyenda fondo transparente y texto blanco
    leg = ax.legend()
    leg.get_frame().set_alpha(0)  # Fondo transparente
    for text in leg.get_texts():
        text.set_color("white")

    st.pyplot(fig)

# === RESULTADOS ===
st.subheader("📋 Resultados Finales")
for saldo, deposito_total, nombre_activo, etiqueta in resultados:
    st.markdown(f"**{etiqueta} ({nombre_activo})**")
    st.write(f"Total depositado: {deposito_total[-1]:,.2f} €")
    st.write(f"Capital final simulado: {saldo[-1]:,.2f} €")
    st.write(f"Ganancia neta simulada: {saldo[-1] - deposito_total[-1]:,.2f} €")

