import os
import streamlit as st
import pandas as pd
from pathlib import Path

import matplotlib.pyplot as plt
import plotly_express as px

from kitconc.kit_corpus import Corpus

st.set_page_config(layout="wide")

st.title("Kitconc com streamlit")
########################## ---------------sidebar------------------------ ##################################
# Define a pasta de destino

UPLOAD_FOLDER = "Corpus"
# Cria a pasta se ela não existir
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Sidebar para upload
with st.sidebar:
    st.header("Corpus do corpus")
    uploaded_files = st.file_uploader(
        "Escolha os arquivos", 
        accept_multiple_files=True,
        type=['txt'] # Define tipos permitidos
    )

    # Processa os arquivos enviados
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Cria o caminho completo do arquivo
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            
            # Salva o arquivo no disco (binário)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
    
########################## ---------------Abas------------------------ ##################################
# 1. Definir os nomes das abas
aba1, aba2, aba3, aba4,aba5,aba6 = st.tabs(["📊 Workspace", "📈 Wordlist", "⚙️ Keywords", "Kwic", "Concordance","Collocates"])

corpus = Corpus("Workspace", "Corpus1", language='portuguese')
corpus.add_texts(UPLOAD_FOLDER)

# 2. Adicionar conteúdo à primeira aba
with aba1:
    with st.container(border=True):
        st.header("Wordspace")
        st.markdown("No kitconc, para realizar a criação de um corpus manipulável pela ferramenta, é preciso deﬁnir uma pasta de trabalho (workspace), um nome de identiﬁcação para o corpus e o idioma dos textos. É preciso também adicionar textos ao corpus criado por meio de uma pasta.Nas atividades desenvolvidas aqui, não se faz necessário criar nenhuma dessas pastas, pois elas são criadas automaticamente quando executamos esta interface. Confira na barra ao lado clicando no símbolo de uma pasta e você verá que há duas pastas Corpus, onde colocaremos os arquivos do nosso corpus, e a workspace.")
        st.subheader("Carregue os arquivos")
        st.markdown("Inicialmente, crie uma pasta escrevendo o nome no espaço abaixo e clicando no botão.")

 ################# ================================== #############################   
# 3. Adicionar conteúdo à segunda aba
with aba2:
    st.header("Wordlist")
    st.markdown('''
A ferramenta wordlist faz uma listagem ordenada por frequência de todas as formas (vocábulos) que ocorrem em um corpus. A partir da lista de frequência, é possível deﬁnir quais são as palavras mais relevantes para a análise do corpus.
''')
    st.markdown(">Pesquise no google sobre as expressões: **riqueza lexical(TTR - Type/Token Ratio)**, **Densidade Lexical (DeL)** e **Diversidade Lexical (DiL)** na linguistica de corpus.")
    
    btn_wordlist = st.button("Create Wordlist",width=200)
    
    @st.cache_data
    def wordlistfunction():
        wordlist = corpus.wordlist(verbose=True)
        st.dataframe(wordlist.df,hide_index=True)

        figbar = px.bar(wordlist.df.head(30), x='WORD',y='FREQUENCY', title="Frequência das palavras")
        figline = px.line(wordlist.df.head(30), x='WORD',y='FREQUENCY', title="Frequência das palavras")

        st.plotly_chart(figbar,use_container_width=True)
        st.plotly_chart(figline, use_container_width=True)

    if btn_wordlist == True:
        wordlistfunction()
    

################# ================================== #############################
# 4. Adicionar conteúdo à terceira aba
with aba3:
    st.header("Keywords")
    st.markdown("O recorte pode ser feito a partir da extração de palavras-chave. Para tanto, há programas que realizam uma comparação estatística a partir das frequências observadas e esperadas das palavras de um corpus de estudo e um corpus de referência de língua geral (muito maior que o corpus de estudo) a ﬁm de identiﬁcar palavras que se destacam. O resultado da comparação retorna uma lista classiﬁcada pelo valor de uma fórmula estatística empregada (log-likelihood ou chi-square), em ordem decrescente, em que as principais palavras do corpus de estudo estarão no topo, geralmente palavras de conteúdo, em contraponto a uma lista de frequência em que as primeiras palavras são gramaticais.")
    
    btn_keywords = st.button("Create Keywords",width=200)

    @st.cache_data
    def keywordsfunction():
        keywords = corpus.keywords(verbose=True)
        st.dataframe(keywords.df,hide_index=True)

        figbar = px.bar(keywords.df.head(30), x='WORD',y='FREQUENCY', title="Frequência das palavras")
        figline = px.line(keywords.df.head(30), x='WORD',y='FREQUENCY', title="Frequência das palavras")
        
        st.plotly_chart(figbar, use_container_width=True)
        st.plotly_chart(figline, use_container_width=True)

    if btn_keywords == True:
        keywordsfunction()
################# ================================== #############################
with aba4:
    st.header("Kwic")
    st.markdown('''A análise somente de listas de palavras não é suﬁciente para determinar os padrões de uso de itens lexicais. Esse propósito pode ser conseguido pela observação dos itens lexicais em seu contexto de uso. Todas as ocorrências de um item lexical e trazer parte de seu contexto em uma visualização privilegiada para análise.\n**O termo concordância** refere-se à listagem das ocorrências de uma palavra de busca de um corpus, a qual ﬁca centralizada, com uma quantidade deﬁnida de contextos em ambos os lados (esquerda e direita) (BERBER SARDINHA, 2004:187).é comum associar ou confundir o termo concordância com o termo utilizado em gramática (exemplo: concordância verbal/nominal). Quando se utiliza o termo concordância, queremos nos referir a um tipo de visualização privilegiada do uso de palavras, conforme já descrito.
    \n > **Pesquise no google sobre a palavra chaviamento e apresente a finalidade, aplicação prática e medida estatística.**''')
    
    contextword = st.text_input("Escreva uma palavra",placeholder="Qual palavra você quer ver o contexto?")
    
    btn_kwic = st.button("Create context",width=200)
    
    @st.cache_data
    def kwicfunction():  
        kwic = corpus.kwic(contextword,verbose=True)
        kwic.sort('R1','R2','R3')
        st.dataframe(kwic.df,hide_index=True)
    
    @st.cache_data
    def collocationfuncion():
        kwic = corpus.kwic(contextword,verbose=True)
        coll = corpus.collocations(kwic)
        st.dataframe(coll.df)

    if btn_kwic == True:
        kwicfunction()
    
    btncollocation = st.button("Collocation in context", width=250)
    
    if btncollocation==True:
        collocationfuncion()


################# ================================== #############################
with aba5:
    st.header("Concordance")
    st.markdown("A análise somente de l")
                
    concordanceword = st.text_input("Escreva uma palavra",placeholder="Qual palavra você quer ver a concordância?")
    
    btn_concordance = st.button("Create concordance",width=200)
    
    @st.cache_data
    def concordancefunction():
        concordances = corpus.concordance(concordanceword,verbose=True)
        st.dataframe(concordances.df,hide_index=True)

    if btn_concordance == True:
        concordancefunction()
################# ================================== #############################
with aba6:
    st.header("Find Collocates")
    st.markdown('''
A análise somente de listas de palavras não é suﬁciente para determinar os padrões de uso de itens lexicais. Esse propósito pode ser conseguido pela observação dos itens lexicais em seu contexto de uso. Todas as ocorrências de um item lexical e trazer parte de seu contexto em uma visualização privilegiada para análise.
\n
* N – é a numeração dos registros;
* WORD – é a palavra ou colocado;
* FREQUENCY – é a frequência total do colocado;
* LEFT – é a frequência do colocado à esquerda do termo de busca;
* RIGHT – é a frequência do colocado à direita do termo de busca;
* ASSOCIATION – é o valor da medida estatística de associação entre o colocado e o termo de busca.\n

> **Pesquise no google sobre o uso de fórmulas para calcular a associação dos colocados na Linguística de Corpus.**''')
                
    collocateword = st.text_input("Escreva o termo de busca",placeholder="A colocação de qual palavra?")
    
    btn_collocate = st.button("Create collocates",width=200)
    
    @st.cache_data
    def collocatesfunction():
        collocates = corpus.collocates(collocateword,left_span=2,right_span=2,verbose=True)
        #collocates = corpus.collocates('skills',left_span=3,right_span=3,coll_pos='NN JJ',verbose=True)
        st.dataframe(collocates.df,hide_index=True)

        figline = px.line(collocates.df.head(20), x='WORD',y='ASSOCIATION', title="Nível de associação entre elas")
        figline2 = px.line(collocates.df.head(20), x='WORD',y='FREQUENCY', title="Nível de frequência")
        
        st.plotly_chart(figline, use_container_width=True)
        st.plotly_chart(figline2,use_container_width=True)

        st.pyplot(collocates.plot_collgraph(node=collocateword))

    if btn_collocate == True:
        collocatesfunction()
################# ================================== #############################
