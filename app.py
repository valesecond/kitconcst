import os
import shutil
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from kitconc.kit_corpus import Corpus

st.set_page_config(layout="wide")

st.title("Kitconc com Streamlit")

# ========================= CONFIG =========================

UPLOAD_FOLDER = "Corpus"
WORKSPACE = "Workspace"
CORPUS_NAME = "Corpus1"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ========================= SIDEBAR =========================

with st.sidebar:

    st.header("Upload do Corpus")

    uploaded_files = st.file_uploader(
        "Escolha arquivos TXT",
        accept_multiple_files=True,
        type=["txt"]
    )

    if uploaded_files:

        # limpa arquivos antigos
        for file in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, file)

            if os.path.isfile(file_path):
                os.remove(file_path)

        # salva novos arquivos
        for uploaded_file in uploaded_files:

            file_path = os.path.join(
                UPLOAD_FOLDER,
                uploaded_file.name
            )

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

# ========================= PROCESSAMENTO =========================

CORPUS_READY = False

try:

    if uploaded_files:

        st.info("Processando corpus...")

        # remove corpus antigo
        if os.path.exists(f"{WORKSPACE}/{CORPUS_NAME}"):

            shutil.rmtree(f"{WORKSPACE}/{CORPUS_NAME}")

        # recria corpus
        corpus = Corpus(
            WORKSPACE,
            CORPUS_NAME,
            language="portuguese"
        )

        # processa textos
        corpus.add_texts(
            UPLOAD_FOLDER,
            verbose=True
        )

        # debug
        st.write("Estrutura criada:")

        for root, dirs, files in os.walk(WORKSPACE):

            st.write(root)
            st.write("Dirs:", dirs)
            st.write("Files:", files)

        # verifica se processamento terminou
        npy_path = f"{WORKSPACE}/{CORPUS_NAME}/data/npy"

        if os.path.exists(npy_path):

            CORPUS_READY = True

            st.success("Corpus processado corretamente!")

        else:

            st.error(
                "Kitconc não criou a pasta data/npy."
            )

    else:

        corpus = Corpus(
            WORKSPACE,
            CORPUS_NAME,
            language="portuguese"
        )

except Exception as e:

    st.error(f"Erro ao processar corpus: {e}")

# ========================= ABAS =========================

aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs([
    "📊 Workspace",
    "📈 Wordlist",
    "⚙️ Keywords",
    "📚 Kwic",
    "📖 Concordance",
    "🔗 Collocates"
])

# ========================= ABA 1 =========================

with aba1:

    st.header("Workspace")

    st.markdown("""
    Faça upload de arquivos TXT na barra lateral.

    O sistema irá criar automaticamente o corpus.
    """)

# ========================= ABA 2 =========================

with aba2:

    st.header("Wordlist")

    btn_wordlist = st.button(
        "Create Wordlist",
        use_container_width=True
    )

    if btn_wordlist:

        if CORPUS_READY:

            try:

                wordlist = corpus.wordlist(
                    verbose=True
                )

                st.dataframe(
                    wordlist.df,
                    hide_index=True
                )

                figbar = px.bar(
                    wordlist.df.head(30),
                    x="WORD",
                    y="FREQUENCY",
                    title="Frequência das palavras"
                )

                figline = px.line(
                    wordlist.df.head(30),
                    x="WORD",
                    y="FREQUENCY",
                    title="Frequência das palavras"
                )

                st.plotly_chart(
                    figbar,
                    use_container_width=True
                )

                st.plotly_chart(
                    figline,
                    use_container_width=True
                )

            except Exception as e:

                st.error(f"Erro Wordlist: {e}")

        else:

            st.warning(
                "Corpus não processado."
            )

# ========================= ABA 3 =========================

with aba3:

    st.header("Keywords")

    btn_keywords = st.button(
        "Create Keywords",
        use_container_width=True
    )

    if btn_keywords:

        if CORPUS_READY:

            try:

                keywords = corpus.keywords(
                    verbose=True
                )

                st.dataframe(
                    keywords.df,
                    hide_index=True
                )

                figbar = px.bar(
                    keywords.df.head(30),
                    x="WORD",
                    y="FREQUENCY"
                )

                st.plotly_chart(
                    figbar,
                    use_container_width=True
                )

            except Exception as e:

                st.error(f"Erro Keywords: {e}")

        else:

            st.warning(
                "Corpus não processado."
            )

# ========================= ABA 4 =========================

with aba4:

    st.header("Kwic")

    contextword = st.text_input(
        "Palavra"
    )

    btn_kwic = st.button(
        "Create context",
        use_container_width=True
    )

    if btn_kwic:

        if CORPUS_READY:

            try:

                kwic = corpus.kwic(
                    contextword,
                    verbose=True
                )

                kwic.sort(
                    'R1',
                    'R2',
                    'R3'
                )

                st.dataframe(
                    kwic.df,
                    hide_index=True
                )

            except Exception as e:

                st.error(f"Erro Kwic: {e}")

        else:

            st.warning(
                "Corpus não processado."
            )

# ========================= ABA 5 =========================

with aba5:

    st.header("Concordance")

    concordanceword = st.text_input(
        "Palavra para concordância"
    )

    btn_concordance = st.button(
        "Create concordance",
        use_container_width=True
    )

    if btn_concordance:

        if CORPUS_READY:

            try:

                concordances = corpus.concordance(
                    concordanceword,
                    verbose=True
                )

                st.dataframe(
                    concordances.df,
                    hide_index=True
                )

            except Exception as e:

                st.error(f"Erro Concordance: {e}")

        else:

            st.warning(
                "Corpus não processado."
            )

# ========================= ABA 6 =========================

with aba6:

    st.header("Collocates")

    collocateword = st.text_input(
        "Palavra para colocação"
    )

    btn_collocate = st.button(
        "Create collocates",
        use_container_width=True
    )

    if btn_collocate:

        if CORPUS_READY:

            try:

                collocates = corpus.collocates(
                    collocateword,
                    left_span=2,
                    right_span=2,
                    verbose=True
                )

                st.dataframe(
                    collocates.df,
                    hide_index=True
                )

                figline = px.line(
                    collocates.df.head(20),
                    x="WORD",
                    y="ASSOCIATION",
                    title="Associação"
                )

                st.plotly_chart(
                    figline,
                    use_container_width=True
                )

            except Exception as e:

                st.error(f"Erro Collocates: {e}")

        else:

            st.warning(
                "Corpus não processado."
            )