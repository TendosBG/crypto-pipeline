import streamlit as st
import duckdb
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Crypto Analytics", layout="wide")

db = Path(__file__).parent.parent / "data" / "gold" / "crypto.duckdb"
con = duckdb.connect(str(db), read_only=True)

df_dominance   = con.execute("SELECT * FROM gold_dominance").df()
df_volatility  = con.execute("SELECT * FROM gold_volatility").df()
df_pumps       = con.execute("SELECT * FROM gold_pumps").df()
df_correlation = con.execute("SELECT * FROM gold_btc_correlation").df()

st.title("Crypto Analytics Dashboard")

# --- Métriques clés ---
total_mcap = df_dominance["market_cap"].sum()
btc_dom    = df_dominance[df_dominance["id"] == "bitcoin"]["dominance"].values[0]
eth_dom    = df_dominance[df_dominance["id"] == "ethereum"]["dominance"].values[0]

col1, col2, col3 = st.columns(3)
col1.metric("Market Cap Totale (Top 50)", f"${total_mcap / 1e12:.2f}T")
col2.metric("BTC Dominance", f"{btc_dom:.1f}%")
col3.metric("ETH Dominance", f"{eth_dom:.1f}%")

st.divider()

# --- Dominance ---
st.header("Market Cap Dominance")
top10 = df_dominance.head(10).copy()
others_dominance = df_dominance.iloc[10:]["dominance"].sum()
import pandas as pd
others_row = pd.DataFrame([{"symbol": "Others", "dominance": others_dominance}])
top10_with_others = pd.concat([top10[["symbol", "dominance"]], others_row], ignore_index=True)
fig_dom = px.pie(top10_with_others, names="symbol", values="dominance", hole=0.4)
fig_dom.update_traces(textposition="inside", textinfo="percent+label")
st.plotly_chart(fig_dom, use_container_width=True)

st.divider()

# --- Volatilité ---
st.header("Volatilité 30 jours")
fig_vol = px.bar(
    df_volatility.head(20).sort_values("volatility_30d"),
    x="volatility_30d", y="symbol",
    orientation="h",
    color="volatility_30d",
    color_continuous_scale="Reds",
    labels={"volatility_30d": "Volatilité 30j (%)", "symbol": "Coin"},
)
fig_vol.update_layout(coloraxis_showscale=False, height=600)
st.plotly_chart(fig_vol, use_container_width=True)

st.divider()

# --- Pumps & Dumps ---
st.header("Pumps & Dumps (24h)")
if df_pumps.empty:
    st.info("Aucun pump/dump significatif aujourd'hui (seuil ±15%).")
else:
    df_pumps["color"] = df_pumps["price_change_percentage_24h"].apply(
        lambda x: "green" if x > 0 else "red"
    )
    fig_pumps = px.bar(
        df_pumps,
        x="symbol", y="price_change_percentage_24h",
        color="color",
        color_discrete_map={"green": "#00CC96", "red": "#EF553B"},
        labels={"price_change_percentage_24h": "Variation 24h (%)", "symbol": "Coin"},
    )
    fig_pumps.update_layout(showlegend=False)
    st.plotly_chart(fig_pumps, use_container_width=True)

st.divider()

# --- Corrélation BTC ---
st.header("Corrélation vs BTC (24h)")
fig_corr = px.bar(
    df_correlation.head(20),
    x="symbol", y="difference",
    color="difference",
    color_continuous_scale="RdYlGn",
    color_continuous_midpoint=0,
    labels={"difference": "Écart vs BTC (%)", "symbol": "Coin"},
)
st.plotly_chart(fig_corr, use_container_width=True)
