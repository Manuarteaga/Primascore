import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="PrimaScore - Evaluador de Opciones",
    page_icon="📈",
    layout="centered",
)

st.title("📈 PrimaScore")
st.markdown(
    "Evalúa si una acción es apta para **vender primas** (*Covered Calls* / *The Wheel*)."
)

# Buscador de Ticker
ticker_input = st.text_input(
    "Introduce el Ticker de la acción", value="AAPL"
).upper()

if st.button("Evaluar Ticker"):
    with st.spinner(f"Analizando la cadena de opciones para {ticker_input}..."):
        try:
            stock = yf.Ticker(ticker_input)
            expirations = stock.options

            if not expirations:
                st.error(
                    f"El ticker **{ticker_input}** no tiene cadena de opciones disponible o no es válido."
                )
            else:
                # Obtener precio actual
                hist = stock.history(period="1d")
                if hist.empty:
                    st.error("No se pudo obtener el precio actual de la acción.")
                else:
                    precio_actual = hist["Close"].iloc[-1]

                    # Tomar la expiración más cercana
                    chain = stock.option_chain(expirations[0])
                    calls = chain.calls

                    # Filtrar opciones ATM (At-The-Money)
                    atm_calls = calls[
                        (calls["strike"] >= precio_actual * 0.95)
                        & (calls["strike"] <= precio_actual * 1.05)
                    ]

                    if atm_calls.empty:
                        st.warning(
                            "No hay suficientes opciones líquidas cerca del precio actual."
                        )
                    else:
                        oi_promedio = atm_calls["openInterest"].mean()
                        vol_promedio = atm_calls["volume"].fillna(0).mean()

                        atm_calls = atm_calls[atm_calls["ask"] > 0]
                        spread_pct = (
                            (atm_calls["ask"] - atm_calls["bid"])
                            / atm_calls["ask"]
                        ).mean()

                        # Algoritmo de puntuación simple
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

                        # Mostrar resultados en la interfaz
                        st.divider()
                        col1, col2, col3 = st.columns(3)
                        col1.metric(
                            label="Precio Subyacente",
                            value=f"${precio_actual:.2f}",
                        )
                        col2.metric(
                            label="PrimaScore", value=f"{score} / 100"
                        )

                        es_viable = score >= 60
                        col3.metric(
                            label="Apto para Primas",
                            value="SÍ" if es_viable else "NO",
                        )

                        st.subheader("Desglose de Métricas")
                        st.write(
                            f"- **Interés Abierto Promedio (ATM):** {int(oi_promedio):,}"
                        )
                        st.write(
                            f"- **Volumen Diario Promedio (ATM):** {int(vol_promedio):,}"
                        )
                        st.write(
                            f"- **Horquilla (Spread) Promedio:** {spread_pct*100:.2f}%"
                        )
                        st.write(
                            f"- **Próximo Vencimiento Analizado:** {expirations[0]}"
                        )

        except Exception as e:
            st.error(
                f"Ocurrió un error al procesar el ticker. Comprueba que sea correcto. Detalle: {e}"
            )
