import streamlit as st
import pandas as pd
import Final_Project_V1 as proc

def main():

    st.set_page_config(
        page_title="DataLuva FIFA21",
        page_icon="⚽")

    st.image("https://www.ufrgs.br/nepemigra/wp-content/uploads/2020/05/UFRGS-BRANCO_VERMELHO-png.png",width=100)
    st.title("DataLuva: [FIFA 21 Players](https://www.kaggle.com/stefanoleone992/fifa-21-complete-player-dataset) Search")

    st.caption("1. player <name or prefix>\n2. user top <userID>\n3. user bottom <userID>\n4. top<N> ‘<position>’\n5. bottom<N> ‘<position>’\n6. tags <list of tags>")

    command = st.text_input('Receba:', '')

    placeholder = st.empty()

    if(command != ""):
        st.dataframe([""])
        with st.spinner("Preparando o lance..."):
            data = proc.search(command)
            with placeholder.container():
                st.dataframe(data)
            
        st.balloons()

    

    

    st.text("")
    st.image("https://static1-br.millenium.gg/articles/3/93/33/@/116688-luva-de-pedreiro-article_m-1.jpg", caption="Receba.")
    st.subheader("INF01124 - Classificação e Pesquisa de Dados")

    st.text("Erick Larratéa Knoblich e Leonardo Azzi Martins, 2022/1")
    st.text("Prof. João Comba")
    st.caption("[GitHub](https://github.com/leonardoazzi/cpd-fifa21)")
    st.text("")


if __name__ == "__main__":
    main()
