import csv
import json
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def pedir_senha():
        senha = simpledialog.askstring("Senha", "Digite sua senha do SIGAA:", initialvalue="", show='*')
        return senha

def extrair_notas_sigaa(config):
    URL = config.get("URL")
    USERNAME = config.get("USERNAME")
    PASSWORD = config.get("PASSWORD")
    SUBJECT = "INB0712-1 - LÓGICA DE PROGRAMAÇÃO - 03" #config.get("SUBJECT")

    #se não tem password, deve pedir
    if not PASSWORD:
        PASSWORD = pedir_senha()


    # Inicialize o driver do navegador
    browser = webdriver.Firefox()
    browser.maximize_window()  # Maximize a janela do navegador
    browser.get(URL)

    # Faça login
    username_field = browser.find_element(By.NAME, "user.login")
    username_field.send_keys(USERNAME)
    password_field = browser.find_element(By.NAME, "user.senha")
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)

    # Aguarde até que a página da tabela seja carregada
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[@class='listagem table tabela-selecao-vinculo']")))

    # Navegue até a página desejada
    browser.find_element(
        By.XPATH, "//a[@class='withoutFormat' and contains(text(),'Servidor')]").click()
    
    WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//li[@class='docente on']")))
    
    browser.find_element(
        By.XPATH, "//a[@href='/sigaa/verPortalDocente.do']").click()
    
    browser.find_element(
        By.XPATH, "//a[contains(text(),'" + SUBJECT + "')]").click()
    
    # Ciente
    browser.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()
    
    browser.find_element(By.XPATH, "//div[contains(text(), 'Alunos')]").click()

    browser.find_element(
        By.XPATH, "//div[contains(text(), 'Lançar Frequência')]").click()
    
    # Localize o botão usando o seletor CSS e clique nele
    button = browser.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
    button.click()


    # Ciente
    browser.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()

    

# Verifica se o arquivo está sendo executado diretamente
if __name__ == "__main__":
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            print("Configurações carregadas com sucesso!")
            extrair_notas_sigaa(config)
        print("Notas extraídas do SIGAA com sucesso!")
    except Exception as e:
        print("Erro ao carregar as configurações:", e)