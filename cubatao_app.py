import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import xml.etree.ElementTree as ET

st.set_page_config(page_title="PI - Abandono Escolar Cubatão", layout="wide")
st.title("Abandono Escolar — Estudo de Caso Cubatão")

aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs([
    "Contexto Oficial (INEP)",
    "Censo Escolar",
    "Frequência 2026",
    "Machine Learning",
    "Panorama Regional",
    "Mapa das Escolas"
])

with aba1:
    st.header("Taxas de Rendimento — Município de Cubatão")

    df_2024 = pd.read_csv("dados_escola_cubatao_completo/2024_cubatao_taxas_rendimento_municipio.csv")
    df_2025 = pd.read_csv("dados_escola_cubatao_completo/2025_cubatao_taxas_rendimento_municipio.csv")

    df_2024["Ano"] = 2024
    df_2025["Ano"] = 2025
    df_rendimento = pd.concat([df_2024, df_2025])

    df_rendimento = df_rendimento.rename(columns={
        "1_CAT_FUN_AF": "Aprovação",
        "2_CAT_FUN_AF": "Reprovação",
        "3_CAT_FUN_AF": "Abandono"
    })

    st.subheader("Anos Finais do Fundamental (6º ao 9º ano)")
    st.dataframe(df_rendimento[["Ano", "Aprovação", "Reprovação", "Abandono"]])

    df_long = df_rendimento.melt(
        id_vars="Ano",
        value_vars=["Aprovação", "Reprovação", "Abandono"],
        var_name="Indicador",
        value_name="Percentual"
    )

    fig = px.bar(df_long, x="Indicador", y="Percentual", color="Ano", barmode="group",
                 title="Comparação 2024 x 2025 — Anos Finais")
    st.plotly_chart(fig)

with aba2:
    st.header("Censo Escolar 2025")

    df_escola = pd.read_csv("dados_escola_cubatao_completo/2025_cubatao_escola.csv", sep=";", encoding="latin1")
    df_matricula = pd.read_csv("dados_escola_cubatao_completo/2025_cubatao_matricula.csv", sep=";", encoding="latin1")
    df_docente = pd.read_csv("dados_escola_cubatao_completo/2025_cubatao_docente.csv", sep=";", encoding="latin1")

    df_mat_escola = df_matricula[df_matricula["QT_MAT_FUND_AF"] > 0][
        ["NO_ENTIDADE", "QT_MAT_FUND_AF"]
    ].sort_values("QT_MAT_FUND_AF", ascending=False)

    col1, col2, col3 = st.columns(3)
    col1.metric("Escolas com Anos Finais (6º-9º)", len(df_mat_escola))
    col2.metric("Matrículas — Anos Finais", int(df_matricula["QT_MAT_FUND_AF"].sum()))
    col3.metric("Docentes — Anos Finais", int(df_docente["QT_DOC_FUND_AF"].sum()))

    st.subheader("Matrículas nos Anos Finais por escola")
    fig = px.bar(df_mat_escola, x="NO_ENTIDADE", y="QT_MAT_FUND_AF",
                 title="Matrículas (6º ao 9º ano) por escola — 2025")
    fig.update_layout(xaxis_title="Escola", yaxis_title="Matrículas")
    st.plotly_chart(fig)

with aba3:
    st.header("Frequência 2026 — Estudo de Caso")

    escolas_disponiveis = ["Escola Municipal de Cubatão (fictícia)"]
    escola_selecionada = st.selectbox("Escolha a escola", escolas_disponiveis)

    st.caption(
        "📍 Apenas esta escola possui registro digital de chamada em 2026. "
        "As demais escolas do município não têm dado de frequência digitalizado — "
        "por isso não há opção de comparar entre escolas ou ver a rede toda nesta aba."
    )

    df_freq = pd.read_csv("dados_escola_cubatao_completo/2026_frequencia_mensal_por_aluno_6a9.csv")

    turmas = sorted(df_freq["turma"].unique())
    turma_selecionada = st.selectbox("Escolha a turma", turmas)

    df_turma = df_freq[df_freq["turma"] == turma_selecionada]

    media_por_mes = df_turma.groupby("mes")["frequencia_pct"].mean().reset_index()

    ordem_meses = ["MAIO", "JUNHO", "JULHO", "AGOSTO"]
    media_por_mes["mes"] = pd.Categorical(media_por_mes["mes"], categories=ordem_meses, ordered=True)
    media_por_mes = media_por_mes.sort_values("mes")

    st.subheader(f"Frequência média — Turma {turma_selecionada}")
    fig = px.line(media_por_mes, x="mes", y="frequencia_pct", markers=True,
                  title=f"Evolução da frequência — {turma_selecionada}")
    fig.update_layout(xaxis_title="Mês", yaxis_title="Frequência (%)", yaxis_range=[0, 100])
    st.plotly_chart(fig)

    st.subheader("Alunos em risco (frequência abaixo de 75%)")
    df_risco = df_turma[df_turma["risco_abaixo_75pct"] == True][
        ["aluno_numero", "mes", "frequencia_pct", "faltas"]
    ].sort_values("frequencia_pct")

    if df_risco.empty:
        st.success("Nenhum aluno em risco nesta turma.")
    else:
        st.dataframe(df_risco)

with aba4:
    st.header("Machine Learning — Prova de Conceito")

    st.subheader("1. Base pública UCI (Realinho et al., 2021)")
    df_uci = pd.read_csv("dados_escola_cubatao_completo/uci_dropout_dataset.csv")
    df_uci["Target"] = df_uci["Target"].replace({
        "Graduate": "Diplomado",
        "Dropout": "Evasão",
        "Enrolled": "Matriculado"
    })

    st.write(
        "Como os dados de Cubatão não têm um rótulo de resultado por aluno "
        "(Abandono, Matriculado, Diplomado), usamos a base pública UCI como "
        "prova de conceito para explorar padrões associados à evasão."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.caption("Distribuição do resultado (Target)")
        contagem = df_uci["Target"].value_counts().reset_index()
        contagem.columns = ["Resultado", "Quantidade"]
        fig1 = px.pie(contagem, names="Resultado", values="Quantidade")
        st.plotly_chart(fig1)

    with col2:
        st.caption("Idade na matrícula x Resultado")
        fig2 = px.box(df_uci, x="Target", y="Age at enrollment",
                      title="Distribuição de idade por resultado")
        st.plotly_chart(fig2)

    st.caption("Bolsista x Situação Acadêmica")
    tabela_bolsa = pd.crosstab(df_uci["Scholarship holder"], df_uci["Target"], normalize="index") * 100
    tabela_bolsa = tabela_bolsa.round(1).reset_index()
    tabela_bolsa["Scholarship holder"] = tabela_bolsa["Scholarship holder"].map({0: "Sem bolsa", 1: "Com bolsa"})
    st.dataframe(tabela_bolsa)

    st.divider()

    st.subheader("2. Extensão: estrutura de dados de Cubatão")
    df_cubatao_ml = pd.read_csv("dados_escola_cubatao_completo/tabela_completa_ficticia_cubatao.csv")
    df_cubatao_ml["resultado_sintetico"] = df_cubatao_ml["resultado_sintetico"].replace("Evasão", "Abandono")

    st.write(
        "Extensão do experimento acima, usando a própria estrutura de dados de "
        "Cubatão (turno da manhã real + turno da tarde fictício, 7º A-D), com "
        "um rótulo de resultado sintético por aluno. No notebook do PI, um "
        "modelo treinado sobre esses dados atingiu **51% de acurácia** — um "
        "resultado moderado, não superestimado, dado o tamanho pequeno da "
        "amostra e a natureza parcialmente sintética dos dados."
    )

    col3, col4 = st.columns(2)

    with col3:
        st.caption("Frequência média x Resultado sintético")
        fig3 = px.box(df_cubatao_ml, x="resultado_sintetico", y="frequencia_media",
                      title="Frequência média por resultado")
        st.plotly_chart(fig3)

    with col4:
        st.caption("Faltas consecutivas (máximo) x Resultado sintético")
        fig4 = px.box(df_cubatao_ml, x="resultado_sintetico", y="faltas_consecutivas_max",
                      title="Faltas consecutivas por resultado")
        st.plotly_chart(fig4)

with aba5:
    st.header("Panorama Regional — Brasil → São Paulo → Cubatão")
    st.write(
        "Como o abandono escolar em Cubatão se compara ao retrato nacional e "
        "estadual? A ideia aqui é um funil: começamos no Brasil, estreitamos "
        "para o estado de São Paulo, e terminamos no município."
    )

    df_brasil = pd.read_csv("dados_escola_cubatao_completo/brasil.csv")

    # DIAGNÓSTICO TEMPORÁRIO — remover depois de resolvido
    st.write("Colunas de brasil.csv:", df_brasil.columns.tolist())
    st.write(df_brasil.head())

    df_sp = pd.read_csv("dados_escola_cubatao_completo/sao_paulo.csv")
    df_municipios = pd.read_csv("dados_escola_cubatao_completo/mapa_municipios_sp.csv")

    st.subheader("1. Brasil (2013–2025)")
    fig_brasil = px.line(
        df_brasil, x="ano", y=["taxa_abandono_ef", "taxa_abandono_em"],
        markers=True, title="Taxa de abandono — Brasil"
    )
    fig_brasil.update_layout(yaxis_title="Taxa de abandono (%)", legend_title="Etapa")
    st.plotly_chart(fig_brasil)
    st.caption("EF = Ensino Fundamental · EM = Ensino Médio")

    st.subheader("2. Estado de São Paulo (2013–2022)")
    fig_sp = px.line(
        df_sp, x="ano", y=["taxa_abandono_ef", "taxa_abandono_em"],
        markers=True, title="Taxa de abandono — Estado de São Paulo"
    )
    fig_sp.update_layout(yaxis_title="Taxa de abandono (%)", legend_title="Etapa")
    st.plotly_chart(fig_sp)
    st.caption("Série do estado disponível até 2022; a série do Brasil segue até 2025.")

    st.subheader("3. Cubatão — retrato mais recente")
    cubatao = df_municipios[df_municipios["municipio"] == "Cubatão"].iloc[0]

    comparacao = pd.DataFrame({
        "Nível": ["Brasil (2025)", "Estado de SP (2022)", "Cubatão"],
        "Abandono EF (%)": [
            df_brasil.iloc[-1]["taxa_abandono_ef"],
            df_sp.iloc[-1]["taxa_abandono_ef"],
            cubatao["taxa_abandono_ef"]
        ],
        "Abandono EM (%)": [
            df_brasil.iloc[-1]["taxa_abandono_em"],
            df_sp.iloc[-1]["taxa_abandono_em"],
            cubatao["taxa_abandono_em"]
        ]
    })

    df_comp_long = comparacao.melt(id_vars="Nível", var_name="Indicador", value_name="Taxa (%)")

    fig_comp = px.bar(
        df_comp_long, x="Nível", y="Taxa (%)", color="Indicador", barmode="group",
        title="Cubatão x Brasil x Estado de SP — retrato mais recente"
    )
    st.plotly_chart(fig_comp)
    st.caption(
        "⚠️ Os anos não coincidem entre as três séries (Brasil = 2025, SP = 2022, "
        "Cubatão = retrato único mais recente do mapa municipal) — a comparação "
        "é de nível, não do mesmo ano exato."
    )

    st.subheader("4. Onde Cubatão está entre os municípios de SP")
    df_municipios_ordenado = df_municipios.sort_values("taxa_abandono_ef").reset_index(drop=True)
    posicao = df_municipios_ordenado[df_municipios_ordenado["municipio"] == "Cubatão"].index[0] + 1
    total_municipios = len(df_municipios_ordenado)

    st.metric(
        "Posição de Cubatão (abandono EF, do menor para o maior)",
        f"{posicao}º de {total_municipios}"
    )

    df_municipios["destaque"] = df_municipios["municipio"].apply(
        lambda x: "Cubatão" if x == "Cubatão" else "Outros municípios"
    )

    fig_ranking = px.histogram(
        df_municipios, x="taxa_abandono_ef", color="destaque",
        title="Distribuição da taxa de abandono (EF) entre municípios de SP",
        nbins=40
    )
    fig_ranking.update_layout(xaxis_title="Taxa de abandono EF (%)", yaxis_title="Nº de municípios")
    st.plotly_chart(fig_ranking)

with aba6:
    st.header("Mapa das Escolas Municipais de Cubatão")

    @st.cache_data
    def carregar_escolas_mapa():
        url = "https://www.google.com/maps/d/kml?mid=1yXMMfgrOSjSOsSUYJr8qqAWenPHI8SKl&forcekml=1"
        resposta = requests.get(url)
        root = ET.fromstring(resposta.content)
        ns = "{http://www.opengis.net/kml/2.2}"

        escolas = []
        for placemark in root.iter(f"{ns}Placemark"):
            nome = placemark.find(f"{ns}name")
            coords = placemark.find(f".//{ns}coordinates")
            if nome is not None and coords is not None:
                lon, lat, *_ = coords.text.strip().split(",")
                escolas.append({"Escola": nome.text, "lat": float(lat), "lon": float(lon)})

        return pd.DataFrame(escolas)

    df_escolas_mapa = carregar_escolas_mapa()

    st.write(f"{len(df_escolas_mapa)} unidades carregadas do mapa oficial da Prefeitura de Cubatão.")

    centro_lat = df_escolas_mapa["lat"].mean()
    centro_lon = df_escolas_mapa["lon"].mean()

    fig_mapa = px.scatter_map(
        df_escolas_mapa, lat="lat", lon="lon", hover_name="Escola",
        zoom=12.5, height=550,
        center={"lat": centro_lat, "lon": centro_lon}
    )
    fig_mapa.update_layout(map_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig_mapa.update_traces(marker=dict(size=13, color="#d62728"))
    st.plotly_chart(fig_mapa, use_container_width=True)

    st.subheader("Lista de unidades")
    st.dataframe(df_escolas_mapa)