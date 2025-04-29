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

partida.send_keys(Keys.CONTROL + "a")  # Seleciona tudo
partida.send_keys(Keys.BACKSPACE)      # Apaga
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
