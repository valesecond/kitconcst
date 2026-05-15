import os
import shutil
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from kitconc.kit_corpus import Corpus

st.set_page_config(layout="wide")

st.title("Kitconc com streamlit")

# ========================= CONFIG =========================

UPLOAD_FOLDER = "Corpus"
WORKSPACE = "Workspace"
CORPUS_NAME = "Corpus1"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ========================= SIDEBAR =========================

with st.sidebar:

    st.header("Corpus do corpus")

    uploaded_files = st.file_uploader(
        "Escolha os arquivos",
        accept_multiple_files=True,
        type=['txt']
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

    corpus = Corpus(
        WORKSPACE,
        CORPUS_NAME,
        language='portuguese'
    )

    if uploaded_files:

        with st.spinner("Processando corpus..."):

            # remove corpus antigo
            if os.path.exists(f"{WORKSPACE}/{CORPUS_NAME}"):

                shutil.rmtree(
                    f"{WORKSPACE}/{CORPUS_NAME}"
                )

            # recria corpus
            corpus = Corpus(
                WORKSPACE,
                CORPUS_NAME,
                language='portuguese'
            )

            # processa textos
            corpus.add_texts(
                UPLOAD_FOLDER,
                verbose=True
            )

            # verifica se criou npy
            npy_path = f"{WORKSPACE}/{CORPUS_NAME}/data/npy"

            if os.path.exists(npy_path):

                CORPUS_READY = True

                st.success(
                    "Corpus processado corretamente!"
                )

            else:

                st.error(
                    "Erro ao criar índices do corpus."
                )

except Exception as e:

    st.error(f"Erro ao processar corpus: {e}")

# ========================= ABAS =========================

aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs([
    "📊 Workspace",
    "📈 Wordlist",
    "⚙️ Keywords",
    "Kwic",
    "Concordance",
    "Collocates"
])

# ========================= ABA 1 =========================

with aba1:

    with st.container(border=True):

        st.header("Wordspace")

        st.markdown("""
No kitconc, para realizar a criação de um corpus manipulável pela ferramenta, é preciso deﬁnir uma pasta de trabalho (workspace), um nome de identiﬁcação para o corpus e o idioma dos textos.

É preciso também adicionar textos ao corpus criado por meio de uma pasta.

Nas atividades desenvolvidas aqui, não se faz necessário criar nenhuma dessas pastas, pois elas são criadas automaticamente quando executamos esta interface.

Confira na barra ao lado clicando no símbolo de uma pasta e você verá que há duas pastas Corpus, onde colocaremos os arquivos do nosso corpus, e a Workspace.
""")

        st.subheader("Carregue os arquivos")

        st.markdown("""
Inicialmente, envie arquivos .txt utilizando o menu lateral.
""")

# ========================= ABA 2 =========================

with aba2:

    st.header("Wordlist")

    st.markdown('''
A ferramenta wordlist faz uma listagem ordenada por frequência de todas as formas (vocábulos) que ocorrem em um corpus.

A partir da lista de frequência, é possível deﬁnir quais são as palavras mais relevantes para a análise do corpus.
''')

    st.markdown("""
> Pesquise no google sobre as expressões:
> **riqueza lexical (TTR - Type/Token Ratio)**,
> **Densidade Lexical (DeL)** e
> **Diversidade Lexical (DiL)** na linguística de corpus.
""")

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
                    x='WORD',
                    y='FREQUENCY',
                    title="Frequência das palavras"
                )

                figline = px.line(
                    wordlist.df.head(30),
                    x='WORD',
                    y='FREQUENCY',
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
                "Envie arquivos para processar o corpus."
            )

# ========================= ABA 3 =========================

with aba3:

    st.header("Keywords")

    st.markdown("""
O recorte pode ser feito a partir da extração de palavras-chave.

Para tanto, há programas que realizam uma comparação estatística a partir das frequências observadas e esperadas das palavras de um corpus de estudo e um corpus de referência de língua geral.
""")

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
                    x='WORD',
                    y='FREQUENCY',
                    title="Frequência das palavras"
                )

                figline = px.line(
                    keywords.df.head(30),
                    x='WORD',
                    y='FREQUENCY',
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

                st.error(f"Erro Keywords: {e}")

        else:

            st.warning(
                "Envie arquivos para processar o corpus."
            )

# ========================= ABA 4 =========================

with aba4:

    st.header("Kwic")

    st.markdown('''
A análise somente de listas de palavras não é suficiente para determinar os padrões de uso de itens lexicais.

Esse propósito pode ser conseguido pela observação dos itens lexicais em seu contexto de uso.
''')

    contextword = st.text_input(
        "Escreva uma palavra",
        placeholder="Qual palavra você quer ver o contexto?"
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
                "Envie arquivos para processar o corpus."
            )

# ========================= ABA 5 =========================

with aba5:

    st.header("Concordance")

    st.markdown("""
A concordância refere-se à listagem das ocorrências de uma palavra de busca em um corpus.
""")

    concordanceword = st.text_input(
        "Escreva uma palavra",
        placeholder="Qual palavra você quer ver a concordância?"
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
                "Envie arquivos para processar o corpus."
            )

# ========================= ABA 6 =========================

with aba6:

    st.header("Find Collocates")

    st.markdown('''
A análise de colocados permite identificar padrões de associação entre palavras.
''')

    collocateword = st.text_input(
        "Escreva o termo de busca",
        placeholder="A colocação de qual palavra?"
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
                    x='WORD',
                    y='ASSOCIATION',
                    title="Nível de associação"
                )

                figline2 = px.line(
                    collocates.df.head(20),
                    x='WORD',
                    y='FREQUENCY',
                    title="Nível de frequência"
                )

                st.plotly_chart(
                    figline,
                    use_container_width=True
                )

                st.plotly_chart(
                    figline2,
                    use_container_width=True
                )

            except Exception as e:

                st.error(f"Erro Collocates: {e}")

        else:

            st.warning(
                "Envie arquivos para processar o corpus."
            )