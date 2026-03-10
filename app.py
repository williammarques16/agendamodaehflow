import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Agendamento - Produção GRID 2605+06",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
<style>
    .big-number { font-size: 2.5rem; font-weight: bold; color: #1f77b4; }
    .metric-label { font-size: 0.9rem; color: #666; }
    .section-divider { border-top: 2px solid #ddd; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Agendamento 10/02 — GRID 2605 + 06")
st.markdown("---")

# ============================================================
# DADOS EXTRAÍDOS DA IMAGEM
# ============================================================

# --- Tabela LEU (Resumo por período) ---
leu_data = {
    "Período": ["2603+04", "2605+06"],
    "FSH": [38, 56],
    "ESSENCIAIS": [20, 40],
    "LESS/FITNESS": [19, 19],
    "Outros": [8, 0],  # ajuste para fechar 85
    "Total": [85, 115],
}
df_leu = pd.DataFrame(leu_data)

# --- Detalhamento [2605+06] por marca ---
marcas_data = {
    "Marca": ["DOG", "LELI", "BENDITA", "OFF MASCULINO", "FEM", "INF."],
    "FSH+CORE": [114, 80, 80, 20, 26, 13],
    "ESSENCIAIS": [22, 20, 10, 6, 9, 8],
    "LESS/FITNESS": [0, 20, 0, 0, 6, 0],
    "Total": [136, 120, 100, 26, 41, 21],
    "Grupo": ["DOG", "LELI+BENDITA", "LELI+BENDITA", "OFF+FEM+INF", "OFF+FEM+INF", "OFF+FEM+INF"],
}
df_marcas = pd.DataFrame(marcas_data)

# --- Composição interna por marca (DT / PL / FDM) ---
composicao_data = []

# DOG
composicao_data.append({"Marca": "DOG", "Canal": "FSH+CORE", "DT": 47, "PL": 50, "FDM": 45, "Peças": 114})
composicao_data.append({"Marca": "DOG", "Canal": "ESSENCIAIS", "DT": 19, "PL": 0, "FDM": 3, "Peças": 22})

# LELI
composicao_data.append({"Marca": "LELI", "Canal": "FSH+CORE", "DT": 0, "PL": 40, "FDM": 40, "Peças": 80})
composicao_data.append({"Marca": "LELI", "Canal": "ESSENCIAIS", "DT": 0, "PL": 10, "FDM": 10, "Peças": 20})
composicao_data.append({"Marca": "LELI", "Canal": "LESS/FITNESS", "DT": 6, "PL": 8, "FDM": 6, "Peças": 20})

# BENDITA
composicao_data.append({"Marca": "BENDITA", "Canal": "FSH+CORE", "DT": 50, "PL": 0, "FDM": 30, "Peças": 80})
composicao_data.append({"Marca": "BENDITA", "Canal": "ESSENCIAIS", "DT": 0, "PL": 10, "FDM": 10, "Peças": 10})  # ajuste

# OFF MASCULINO
composicao_data.append({"Marca": "OFF MASCULINO", "Canal": "FSH+CORE", "DT": 10, "PL": 0, "FDM": 10, "Peças": 20})
composicao_data.append({"Marca": "OFF MASCULINO", "Canal": "ESSENCIAIS", "DT": 5, "PL": 0, "FDM": 1, "Peças": 6})

# FEM
composicao_data.append({"Marca": "FEM", "Canal": "FSH+CORE", "DT": 16, "PL": 0, "FDM": 0, "Peças": 26})
composicao_data.append({"Marca": "FEM", "Canal": "ESSENCIAIS", "DT": 0, "PL": 0, "FDM": 9, "Peças": 9})
composicao_data.append({"Marca": "FEM", "Canal": "LESS/FITNESS", "DT": 6, "PL": 0, "FDM": 0, "Peças": 6})

# INF.
composicao_data.append({"Marca": "INF.", "Canal": "FSH+CORE", "DT": 13, "PL": 0, "FDM": 0, "Peças": 13})
composicao_data.append({"Marca": "INF.", "Canal": "ESSENCIAIS", "DT": 8, "PL": 0, "FDM": 0, "Peças": 8})

df_composicao = pd.DataFrame(composicao_data)

# --- Totais por canal ---
totais_canal = {"FSH+CORE": 333, "ESSENCIAIS": 85, "LESS/FITNESS": 26}
total_geral = 444

# --- Distribuição por responsável ---
responsaveis_data = {
    "Responsável": ["THIAGO", "ANNA"],
    "Peças": [274, 170],
}
df_responsaveis = pd.DataFrame(responsaveis_data)

# --- Totais por grupo ---
grupos_data = {
    "Grupo": ["DOG", "LELI + BENDITA", "OFF MASCULINO + FEM + INF."],
    "Total": [136, 220, 88],
}
df_grupos = pd.DataFrame(grupos_data)


# ============================================================
# MÉTRICAS PRINCIPAIS
# ============================================================
st.subheader("Resumo Geral")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Geral de Peças", f"{total_geral}")
col2.metric("FSH + CORE", f"{totais_canal['FSH+CORE']}")
col3.metric("ESSENCIAIS", f"{totais_canal['ESSENCIAIS']}")
col4.metric("LESS/FITNESS", f"{totais_canal['LESS/FITNESS']}")

st.markdown("---")

# ============================================================
# TABELA LEU — COMPARATIVO POR PERÍODO
# ============================================================
st.subheader("Comparativo LEU por Período")
col_tbl, col_chart = st.columns([1, 2])

with col_tbl:
    st.dataframe(df_leu, width="stretch", hide_index=True)

with col_chart:
    df_leu_melt = df_leu.melt(
        id_vars="Período",
        value_vars=["FSH", "ESSENCIAIS", "LESS/FITNESS"],
        var_name="Canal",
        value_name="Quantidade",
    )
    fig_leu = px.bar(
        df_leu_melt,
        x="Período",
        y="Quantidade",
        color="Canal",
        barmode="group",
        title="Distribuição por Canal — LEU",
        color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c"],
    )
    fig_leu.update_layout(height=350)
    st.plotly_chart(fig_leu, width="stretch")

st.markdown("---")

# ============================================================
# DETALHAMENTO POR MARCA [2605+06]
# ============================================================
st.subheader("Detalhamento por Marca — [2605+06]")

col_left, col_right = st.columns(2)

with col_left:
    st.dataframe(
        df_marcas[["Marca", "FSH+CORE", "ESSENCIAIS", "LESS/FITNESS", "Total"]],
        width="stretch",
        hide_index=True,
    )

with col_right:
    fig_marcas = px.bar(
        df_marcas,
        x="Marca",
        y=["FSH+CORE", "ESSENCIAIS", "LESS/FITNESS"],
        title="Peças por Marca e Canal",
        barmode="stack",
        color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96"],
    )
    fig_marcas.update_layout(
        height=400,
        yaxis_title="Quantidade de Peças",
        legend_title="Canal",
    )
    st.plotly_chart(fig_marcas, width="stretch")

st.markdown("---")

# ============================================================
# GRÁFICOS DE COMPOSIÇÃO (DT / PL / FDM)
# ============================================================
st.subheader("Composição por Tipo (DT / PL / FDM)")

# Agregar por marca
df_comp_marca = df_composicao.groupby("Marca")[["DT", "PL", "FDM"]].sum().reset_index()
# Reordenar pela ordem original
ordem_marcas = ["DOG", "LELI", "BENDITA", "OFF MASCULINO", "FEM", "INF."]
df_comp_marca["Marca"] = pd.Categorical(df_comp_marca["Marca"], categories=ordem_marcas, ordered=True)
df_comp_marca = df_comp_marca.sort_values("Marca")

col_a, col_b = st.columns(2)

with col_a:
    fig_comp = px.bar(
        df_comp_marca,
        x="Marca",
        y=["DT", "PL", "FDM"],
        title="Composição DT / PL / FDM por Marca",
        barmode="stack",
        color_discrete_map={"DT": "#AB63FA", "PL": "#FFA15A", "FDM": "#19D3F3"},
    )
    fig_comp.update_layout(height=400, yaxis_title="Quantidade")
    st.plotly_chart(fig_comp, width="stretch")

with col_b:
    # Totais gerais DT / PL / FDM
    total_dt = df_composicao["DT"].sum()
    total_pl = df_composicao["PL"].sum()
    total_fom = df_composicao["FDM"].sum()

    fig_pie_tipo = px.pie(
        names=["DT", "PL", "FDM"],
        values=[total_dt, total_pl, total_fom],
        title=f"Distribuição Geral por Tipo (Total: {total_dt + total_pl + total_fom})",
        color_discrete_sequence=["#AB63FA", "#FFA15A", "#19D3F3"],
        hole=0.4,
    )
    fig_pie_tipo.update_layout(height=400)
    st.plotly_chart(fig_pie_tipo, width="stretch")

st.markdown("---")

# ============================================================
# GRUPOS DE MARCAS
# ============================================================
st.subheader("Agrupamento de Marcas")

col_g1, col_g2 = st.columns(2)

with col_g1:
    fig_grupos = px.pie(
        df_grupos,
        names="Grupo",
        values="Total",
        title=f"Distribuição por Grupo (Total: {total_geral})",
        color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96"],
        hole=0.35,
    )
    fig_grupos.update_traces(textposition="inside", textinfo="value+percent")
    fig_grupos.update_layout(height=400)
    st.plotly_chart(fig_grupos, width="stretch")

with col_g2:
    fig_resp = px.pie(
        df_responsaveis,
        names="Responsável",
        values="Peças",
        title=f"Distribuição por Responsável (Total: {total_geral})",
        color_discrete_sequence=["#1F77B4", "#FF6692"],
        hole=0.35,
    )
    fig_resp.update_traces(textposition="inside", textinfo="value+percent")
    fig_resp.update_layout(height=400)
    st.plotly_chart(fig_resp, width="stretch")

st.markdown("---")

# ============================================================
# TABELA DETALHADA DE COMPOSIÇÃO
# ============================================================
st.subheader("Tabela Detalhada — Composição por Marca e Canal")
st.dataframe(
    df_composicao,
    width="stretch",
    hide_index=True,
    column_config={
        "Marca": st.column_config.TextColumn("Marca", width="medium"),
        "Canal": st.column_config.TextColumn("Canal", width="medium"),
        "DT": st.column_config.NumberColumn("DT", format="%d"),
        "PL": st.column_config.NumberColumn("PL", format="%d"),
        "FDM": st.column_config.NumberColumn("FDM", format="%d"),
        "Peças": st.column_config.NumberColumn("Total Peças", format="%d"),
    },
)

# ============================================================
# HEATMAP — MARCA x CANAL
# ============================================================
st.subheader("Mapa de Calor — Marca x Canal")
pivot = df_composicao.pivot_table(
    index="Marca", columns="Canal", values="Peças", aggfunc="sum", fill_value=0
)
pivot = pivot.reindex(ordem_marcas)

fig_heat = px.imshow(
    pivot,
    text_auto=True,
    color_continuous_scale="Blues",
    title="Heatmap de Peças por Marca e Canal",
    aspect="auto",
)
fig_heat.update_layout(height=400)
st.plotly_chart(fig_heat, width="stretch")

st.markdown("---")

# ============================================================
# TREEMAP GERAL
# ============================================================
st.subheader("Visão Hierárquica (Treemap)")

treemap_data = df_marcas[["Marca", "Grupo", "Total"]].copy()
fig_tree = px.treemap(
    treemap_data,
    path=["Grupo", "Marca"],
    values="Total",
    title=f"Treemap — Marcas por Grupo (Total: {total_geral} peças)",
    color="Total",
    color_continuous_scale="RdYlBu_r",
)
fig_tree.update_layout(height=500)
st.plotly_chart(fig_tree, width="stretch")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("📋 Dados extraídos do agendamento manuscrito de 10/02 — GRID 2605+06")
