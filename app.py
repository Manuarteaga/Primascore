import pandas as pd
import streamlit as st
import yfinance as yf

# Configuración de la página
st.set_page_config(
    page_title="PrimaScore | Evaluador de Opciones",
    page_icon="📈",
    layout="wide",
)

# Estilos CSS personalizados para darle un aspecto moderno y limpio
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
    }
    .metric-card {
        background-color: #1e2530;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #2d3748;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Cabecera principal
st.title("📈 PrimaScore")
st.markdown(
    "##### Analiza la liquidez y rentabilidad potencial para venta de primas (*Covered Calls* / *The Wheel*)"
)
st.markdown("---")

# Barra lateral para controles
with st.sidebar:
    st.header("⚙️ Parámetros")
    ticker_input = st.text_input(
        "Símbolo Ticker", value="AAPL", help="Ej: AAPL, TSLA, KO, F, NVDA"
    ).upper()
    capital_disponible = st.number_input(
        "Capital / Acciones a simular",
        min_value=100,
        value=10000,
        step=500,
        help="Dinero base o múltiplo de 100 acciones",
    )
    analizar_btn = st.button("🚀 Evaluar Ticker")

# Lógica principal al hacer clic
if analizar_btn or ticker_input:
    with st.spinner(f"Conectando con el mercado y analizando {ticker_input}..."):
        try:
            stock = yf.Ticker(ticker_input)
            expirations = stock.options

            if not expirations:
                st.error(
                    f"El ticker **{ticker_input}** no dispone de cadena de opciones o no es válido."
                )
            else:
                # Obtener precio actual
                hist = stock.history(period="5d")
                if hist.empty:
                    st.error(
                        "No se pudo obtener el precio histórico del subyacente."
                    )
                else:
                    precio_actual = hist["Close"].iloc[-1]

                    # Tomar la expiración más cercana
                    chain = stock.option_chain(expirations[0])
                    calls = chain.calls

                    # Filtrar opciones ATM (At-The-Money: +/- 5%)
                    atm_calls = calls[
                        (calls["strike"] >= precio_actual * 0.95)
                        & (calls["strike"] <= precio_actual * 1.05)
                    ]

                    if atm_calls.empty:
                        st.warning(
                            "No hay suficientes opciones líquidas cerca del precio actual (ATM)."
                        )
                    else:
                        oi_promedio = atm_calls["openInterest"].mean()
                        vol_promedio = atm_calls["volume"].fillna(0).mean()

                        atm_calls_valid = atm_calls[atm_calls["ask"] > 0]
                        spread_pct = (
                            (
                                atm_calls_valid["ask"]
                                - atm_calls_valid["bid"]
                            )
                            / atm_calls_valid["ask"]
                        ).mean()
                        if pd.isna(spread_pct):
                            spread_pct = 0.15

                        # Cálculo de Puntuación (0 a 100)
                        score = 0
                        if oi_promedio > 1000:
                            score += 40
                        elif oi_promedio > 250:
                            score += 20

                        if vol_promedio > 200:
                            score += 20
                        elif vol_promedio > 50:
                            score += 10

                        if spread_pct < 0.05:
                            score += 40
                        elif spread_pct < 0.12:
                            score += 20

                        # Contenedor visual de resultados principales
                        st.subheader(
                            f"Resultados del Análisis para: `{ticker_input}`"
                        )

                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric(
                                label="💵 Precio Subyacente",
                                value=f"${precio_actual:.2f}",
                            )
                        with col2:
                            st.metric(
                                label="⭐ PrimaScore",
                                value=f"{score} / 100",
                                delta=(
                                    "Excelente" if score >= 60 else "Precaución"
                                ),
                            )
                        with col3:
                            es_viable = score >= 60
                            st.metric(
                                label="✅ Apto para Primas",
                                value="SÍ" if es_viable else "NO",
                            )
                        with col4:
                            st.metric(
                                label="📅 Vencimiento",
                                value=expirations[0],
                            )

                        st.markdown("---")

                        # Desglose en pestañas para ordenar la información con estilo
                        tab1, tab2, tab3 = st.tabs(
                            [
                                "📊 Métricas Clave",
                                "💰 Simulación de Ingresos",
                                "📋 Cadena de Opciones ATM",
                            ]
                        )

                        with tab1:
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.markdown("##### Salud de Liquidez")
                                st.write(
                                    f"- **Interés Abierto (OI) Promedio:** `{int(oi_promedio):,}` contratos"
                                )
                                st.write(
                                    f"- **Volumen Diario Promedio:** `{int(vol_promedio):,}` negociados"
                                )
                            with col_b:
                                st.markdown("##### Estructura de Costes")
                                st.write(
                                    f"- **Spread Bid-Ask Promedio:** `{spread_pct*100:.2f}%`"
                                )
                                st.write(
                                    "- **Calidad de Ejecución:** "
                                    + (
                                        "🟢 Alta (Bajo impacto de fricción)"
                                        if spread_pct < 0.08
                                        else "🔴 Baja (Spread ancho)"
                                    )
                                )

                        with tab2:
                            coste_lote = precio_actual * 100
                            # Prima estimada conservadora basada en la prima media cercana si existe
                            prima_estimada = (
                                atm_calls_valid["lastPrice"].mean()
                                if not atm_calls_valid.empty
                                else precio_actual * 0.015
                            )
                            if pd.isna(prima_estimada):
                                prima_estimada = precio_actual * 0.01

                            st.markdown(
                                f"##### Estimación para 1 Lote (100 acciones) = `${coste_lote:,.2f}`"
                            )
                            col_s1, col_s2, col_s3 = st.columns(3)
                            col_s1.metric(
                                "Prima Bruta Estimada",
                                f"${prima_estimada * 100:.2f}",
                            )
                            col_s2.metric(
                                "Retorno sobre Capital",
                                f"{(prima_estimada / precio_actual)*100:.2f}%",
                            )
                            col_s3.metric(
                                "Lotes posibles con tu capital",
                                f"{int(capital_disponible // coste_lote)}",
                            )

                        with tab3:
                            st.markdown("##### Opciones Call disponibles (ATM)")
                            st.dataframe(
                                atm_calls[
                                    [
                                        "contractSymbol",
                                        "strike",
                                        "lastPrice",
                                        "bid",
                                        "ask",
                                        "volume",
                                        "openInterest",
                                    ]
                                ],
                                use_container_width=True,
                            )

        except Exception as e:
            st.error(
                f"No se pudo completar el análisis para '{ticker_input}'. Comprueba que el símbolo sea correcto. (Error: {e})"
            )
            
