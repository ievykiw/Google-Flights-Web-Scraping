from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time

def clicar(driver, e_type, selector):
    while True:
        try:
            driver.find_element(e_type, selector).click()
        except:
            pass
        else:
            break 

partida_User = input("Digite a sua cidade de partida: ").strip().title()
destino_User = input("Digite as cidades que você deseja, separado por vírgulas: ")
data_ida = input("Digite a Data de Partida DD/MM/AA¨: ").strip()
data_volta = input("Digite a Data de Retorn DD/MM/AA: ").strip()


lista_cidade = [cidade.strip().title() for cidade in destino_User.split(",")]
lista_info = []

print(lista_cidade)
driver = webdriver.Firefox()

driver.get('https://www.google.com/travel/flights?gl=BR&hl=pt-BR')

partida = driver.find_element(By.XPATH, '//input[@aria-label="De onde?"]')

partida.send_keys(Keys.CONTROL + "a") 
partida.send_keys(Keys.BACKSPACE)      
partida.send_keys(partida_User)

time.sleep(5)

clicar(driver, By.XPATH, f'//li[@aria-label="{partida_User}"]')

destino = driver.find_element(By.XPATH, '//input[@aria-label="Para onde? "]')
destino.send_keys(lista_cidade)

time.sleep(5)

clicar(driver, By.XPATH, f"(//div[@class='zsRT0d'][normalize-space()='{lista_cidade[0]}'])[1]")

data_partida = driver.find_element(By.XPATH, '//input[@aria-label="Partida"]')
data_partida.send_keys(data_ida)

time.sleep(3)

data_retorno = driver.find_element(By.XPATH, '//input[@aria-label="Volta"]')
data_retorno.send_keys(data_volta, Keys.ENTER)

search_button = driver.find_element(By.CLASS_NAME, 'xFFcie')
search_button.click()

time.sleep(5)

conclued_button = driver.find_element(By.CLASS_NAME, 'WXaAwc')
conclued_button.click()

time.sleep(5)

search_button = driver.find_element(By.CLASS_NAME, 'xFFcie')
search_button.click()

time.sleep(5)

# Raspagem de Dados de Viagem e Criação do Data Frame

button = driver.find_element(By.XPATH, "//span[text()='Mostrar mais voos']")
button.click()

time.sleep(5)

viagem_info = driver.find_elements(By.TAG_NAME, "li")

lista_info = []

for info in viagem_info:
    dados = info.text.split("\n")
    if len(dados) < 6:
        continue

    horario_ida = dados[0]
    companhia_aerea = dados[1]
    duracao_total = dados[2]
    origem_destino = dados[3]
    numero_paradas = dados[4]
    escala_tempo_local = dados[5] if "h" in dados[5] or "min" in dados[5] else "Direto"
    preco_total = dados[8] if len(dados) > 8 and dados[8].strip() else "Preço não informado"

    lista_info.append([
        partida_User,
        destino_User.title(),
        horario_ida,
        companhia_aerea,
        duracao_total,
        origem_destino,
        numero_paradas,
        escala_tempo_local,
        data_ida,
        data_volta,
        preco_total
    ])

print(lista_info)
