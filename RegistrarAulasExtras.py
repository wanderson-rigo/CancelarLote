import json
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select

def registrarExtra(browser, diasLetivo, aulasEncontro):
    try:
        data = browser.find_element(By.ID, "formAva:data")
        data.send_keys(diasLetivo)

        select_element = browser.find_element(By.ID, "formAva:tipo")

        # Crie um objeto Select com o elemento localizado
        select = Select(select_element)

        # Selecione a opção "Adicional" pelo seu valor
        select.select_by_value('2')

        aulas = browser.find_element(By.ID, "formAva:numeroAulas")
        aulas.send_keys(aulasEncontro)

        descricao = browser.find_element(By.ID, "formAva:descricao")
        descricao.send_keys("Aula Extra")

        botaoCadastrar = browser.find_element(By.XPATH, "//input[@type='submit' and @value='Cadastrar']")
        botaoCadastrar.click()


    except NoSuchElementException as e:
        #print("Erro ao extrair dias letivos:", e)
        pass
    except StaleElementReferenceException as e:
        #print("Erro ao extrair dias letivos:", e)
        pass
                


def pedir_senha(USERNAME):
        senha = simpledialog.askstring("Senha do SIGAA", "Ei " + USERNAME + ", digite sua senha do SIGAA:", initialvalue="", show='*')
        return senha

def registrarAulasExtras(config, datasSelecionadas, aulasEncontro):
    URL = config.get("URL")
    USERNAME = config.get("USERNAME")
    PASSWORD = config.get("PASSWORD")
    SUBJECT =  config.get("SUBJECT")

    #se não tem password, deve pedir
    if not PASSWORD:
        PASSWORD = pedir_senha(USERNAME)


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
    
    indiceDasDatas = 0

    while (indiceDasDatas < len(datasSelecionadas)):
        browser.find_element(By.XPATH, "//div[contains(text(), 'Registrar Aula Extra')]").click()
        browser.find_element(By.XPATH, "//p[contains(text(), 'Cadastrar Aula Extra')]").click()
        data = datasSelecionadas[indiceDasDatas]
        registrarExtra(browser, data, aulasEncontro)
        indiceDasDatas += 1