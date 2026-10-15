import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="CBDA - Pontuação de Clubes",
    page_icon="🏊‍♂️",
    layout="wide"
)

CAMINHO_LOCAL = "dados_cbda.json"

CATEGORIAS = {
    "🏆 Geral (Todas as Categorias)": "geral",
    "Pré-Mirim (ID: 21)": "21",
    "Mirim 1 (ID: 6)": "6",
    "Mirim 2 (ID: 7)": "7",
    "Petiz 1 (ID: 8)": "8",
    "Petiz 2 (ID: 9)": "9"
}

# --- Barra Lateral: Upload e Persistência ---
with st.sidebar:
    st.header("📁 Fonte de Dados")
    arquivo_upload = st.file_uploader("Upload de dados_cbda.json", type=["json"])

    # Salva o arquivo no diretório local se um novo upload for realizado
    if arquivo_upload is not None:
        with open(CAMINHO_LOCAL, "wb") as f:
            f.write(arquivo_upload.getbuffer())
        st.success(f"✅ Arquivo salvo localmente como `{CAMINHO_LOCAL}`!")

    # Exibe informações do arquivo gravado em disco
    if os.path.exists(CAMINHO_LOCAL):
        mod_time = os.path.getmtime(CAMINHO_LOCAL)
        dt_str = datetime.fromtimestamp(mod_time).strftime("%d/%m/%Y às %H:%M:%S")
        st.caption(f"🕒 Versão em disco: **{dt_str}**")
    else:
        st.caption("⚠️ Nenhum arquivo salvo localmente ainda.")

    st.divider()

    st.header("🎯 Filtros")
    categoria_label = st.selectbox("Categoria / Visão", list(CATEGORIAS.keys()), index=0)
    id_selecionado = CATEGORIAS[categoria_label]

# --- Leitura do Arquivo Local Persistido ---
dados = None
if os.path.exists(CAMINHO_LOCAL):
    with open(CAMINHO_LOCAL, "r", encoding="utf-8") as f:
        dados = json.load(f)

# --- Corpo Principal ---
st.title("🏊 Classificação de Clubes")
st.caption("12º Troféu Pedro Nicolas Sena da Silva - CBDA")

if not dados:
    st.info("📌 Nenhum dado carregado. Faça o upload do arquivo `dados_cbda.json` na barra lateral para começar.")
else:
    registros = dados.get(id_selecionado, [])

    if not registros:
        st.warning(f"Nenhum clube pontuou na visão/categoria selecionada (**{categoria_label}**).")
    else:
        df = pd.DataFrame(registros)

        # Padronização e tratamento das colunas
        df["Posição"] = df["colocacao"]
        df["Clube"] = df["clube2"]
        df["Logo"] = df["logo"]
        df["Pontos"] = (
            df["pontos"]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

        df = df[["Posição", "Logo", "Clube", "Pontos"]].sort_values("Posição").reset_index(drop=True)

        # Cards com métricas principais
        c1, c2, c3 = st.columns(3)
        c1.metric("Líder", df.iloc[0]["Clube"])
        c2.metric("Maior Pontuação", f"{df.iloc[0]['Pontos']:.1f} pts")
        c3.metric("Clubes Pontuadores", len(df))

        st.subheader(f"Ranking - {categoria_label}")

        # Tabela formatada com imagem do escudo
        st.dataframe(
            df,
            column_config={
                "Posição": st.column_config.NumberColumn(format="%dº", width="small"),
                "Logo": st.column_config.ImageColumn("Escudo", width="small"),
                "Clube": st.column_config.TextColumn("Clube", width="large"),
                "Pontos": st.column_config.NumberColumn("Pontos", format="%.2f")
            },
            use_container_width=True,
            hide_index=True
        )

        # Exportação da tabela atual em CSV
        csv_data = df[["Posição", "Clube", "Pontos"]].to_csv(index=False, sep=";").encode("utf-8-sig")
        st.download_button(
            label="📥 Baixar Ranking em CSV",
            data=csv_data,
            file_name=f"ranking_{id_selecionado}.csv",
            mime="text/csv"
        )