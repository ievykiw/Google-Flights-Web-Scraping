from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
import streamlit as st


#Definição de Funções Auxiliares

def clicar(driver, e_type, selector):
    while True:
        try:
            driver.find_element(e_type, selector).click()
        except:
            pass
        else:
            break 

def case_exceptions(cidade):
    exceptions = ['de', 'do', 'da', 'dos', 'das', 'e', 'ou', 'a', 'an', 'in', 'at', 'for']
    cidade_texto = cidade.split()
    cidade_caps = []

    for texto in cidade_texto:
        if texto.lower() not in exceptions:
            cidade_caps.append(texto.capitalize())
        else:
            cidade_caps.append(texto.lower())
    
    return ' '.join(cidade_caps)

#Implementação de Interface para Usuário usando Streamlit

loading_placeholder = st.empty()

st.header("Consulta de Passagens Áeras")
st.subheader("Via Google Flights")

st.write("Este é um projeto pessoal de *Web Scraping* para consulta de preços e outras informações de passagens aéreas, utilizando o **Google Flights** para coleta de dados!")

with st.form("informacoes_voo"):
    
    navegador_opcao = st.selectbox("Selecione o navegador:", ("Chrome", "Edge", "Firefox", "Safari"))
    st.write("Digite as Informações dos Voos de seu interesse")

    partida_User = st.text_input("Digite a Cidade de Partida", placeholder="Ex: Aracaju").strip()
    destino_User = st.text_input("Digite a(s) Cidade(s) de Destino", placeholder="Ex: Fortaleza, São Paulo, Rio Grande do Sul", help="Seperado por Vírgulas").strip()
    
    data_ida = st.date_input("Selecione a Data de Ida", "today", min_value="today", format="DD/MM/YYYY")
    data_volta = st.date_input("Selecione a Data de Retorno", None,min_value="today", format="DD/MM/YYYY")


    html_code = f"""
        <head>
            <!-- Link para o Google Fonts -->
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=progress_activity" />
        </head>
        <body>
            <div class="loading-text">
                <span class="material-symbols-outlined icon">
                    progress_activity
                </span>
                Buscando viagens com partida em {case_exceptions(partida_User)} e destino em {case_exceptions(destino_User)}
            </div>
        </body>
        <style>
            /* Animação de piscar no texto */
            .loading-text {{
                display: flex;
                flex-direction: row;
                align-items: center;
                font-size: 20px;
                font-weight: light;
                color: #4CAF50;
                font-family: "Source Sans Pro", sans-serif;
            }}

            .icon {{
                margin-right: 10px;
                font-size: 24px;
                animation: rotateIcon 1.5s linear infinite;
            }}

            @keyframes rotateIcon {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        </style>
    """

    if st.form_submit_button(label="Buscar", icon=":material/search:"):
        if not partida_User:
            st.error("O campo Cidade de Partida é Obrigatório")
        elif not destino_User:
            st.error("O campo Cidade de Destino é Obrigatório")
        elif not data_ida:
            st.error("O campo Data de Ida é Obrigatório")
        elif not data_volta:
            st.error("O campo Data de Retorno é Obrigatório")
        else:
            loading_placeholder.markdown(html_code, unsafe_allow_html=True)
            lista_cidade = [cidade.strip().title() for cidade in destino_User.split(",")]

            if navegador_opcao == "Chrome":
                driver = webdriver.Chrome()
            elif navegador_opcao == "Edge":
                driver = webdriver.Edge()
            elif navegador_opcao == "Firefox":
                driver = webdriver.Firefox()
            elif navegador_opcao == "Safari":
                driver = webdriver.Safari()
            else:
                st.error("Navegador não suportado.")
            lista_info = []

            for cidade in lista_cidade:

                #Início da Raspagem de Dados no Navegador

                driver.get('https://www.google.com/travel/flights?gl=BR&hl=pt-BR')

                partida = driver.find_element(By.XPATH, '//input[@aria-label="De onde?"]')

                partida.send_keys(Keys.CONTROL + "a") 
                partida.send_keys(Keys.BACKSPACE)      
                partida.send_keys(case_exceptions(partida_User))

                time.sleep(5)

                clicar(driver, By.XPATH, f'//li[@aria-label="{case_exceptions(partida_User)}"]')

                destino = driver.find_element(By.XPATH, '//input[@aria-label="Para onde? "]')
                destino.send_keys(case_exceptions(cidade))

                time.sleep(5)

                clicar(driver, By.XPATH, f"(//div[@class='zsRT0d'][normalize-space()='{case_exceptions(cidade)}'])[1]")

                data_partida = driver.find_element(By.XPATH, '//input[@aria-label="Partida"]')
                data_partida.send_keys(str(data_ida).replace("-","/"), Keys.ENTER)

                time.sleep(5)

                data_retorno = driver.find_element(By.XPATH, '//input[@aria-label="Volta"]')
                data_retorno.send_keys(str(data_volta).replace("-","/"), Keys.ENTER)

                search_button = driver.find_element(By.CLASS_NAME, 'xFFcie')
                search_button.click()

                time.sleep(5)

                conclued_button = driver.find_element(By.CLASS_NAME, 'WXaAwc')
                conclued_button.click()

                time.sleep(5)

                search_button = driver.find_element(By.CLASS_NAME, 'xFFcie')
                search_button.click()

                time.sleep(5)

                #Raspagem de Dados de Viagem e Criação do Data Frame

                button = driver.find_element(By.XPATH, "//span[text()='Mostrar mais voos']")
                button.click()

                time.sleep(5)

                viagem_info = driver.find_elements(By.TAG_NAME, "li")

                for info in viagem_info:
                    dados = info.text.split("\n")
                    if len(dados) < 6:
                        continue

                    horarios_trajeto = dados[0]
                    companhia_aerea = dados[1]
                    duracao_total = dados[2]
                    origem_destino = dados[3]
                    numero_paradas = dados[4]
                    escala_tempo_local = dados[5] if "h" in dados[5] or "min" in dados[5] else "Direto"
                    preco_total = next((x for x in dados if "R$" in x), "Preço não informado")

                    lista_info.append([
                        partida_User,
                        cidade.title(),
                        horarios_trajeto,
                        companhia_aerea,
                        duracao_total,
                        origem_destino,
                        numero_paradas,
                        escala_tempo_local,
                        data_ida,
                        data_volta,
                        preco_total
                    ])
                    
        #Criação e Modelagem do DataFrame para Análise de Dados

        colunas = ['local_partida', 'local_destino', 'horarios_trajeto', 'companhia_aerea', 'duracao_total', 'origem_destino', 'numero_paradas', 'escalas', 'data_ida', 'data_volta', 'preco']

        df = pd.DataFrame(lista_info, columns=colunas)

        st.dataframe(df)
        loading_placeholder.empty()
        driver.quit()
        st.success(f"Viagens encontradas saindo de {case_exceptions(partida_User)} e partindo para {case_exceptions(destino_User)}!")
