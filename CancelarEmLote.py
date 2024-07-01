import json
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.alert import Alert

def pedir_senha():
        senha = simpledialog.askstring("Senha", "Digite sua senha do SIGAA:", initialvalue="", show='*')
        return senha

def extrair_notas_sigaa(config, dates):
    URL = config.get("URL")
    USERNAME = config.get("USERNAME")
    PASSWORD = config.get("PASSWORD")
    #SUBJECT =  "INB0712-1 - LÓGICA DE PROGRAMAÇÃO - 03"
    SUBJECT =  config.get("SUBJECT")

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
    
    # 0 é Fevereiro
    # 1 é Março
    # 2 é Abril
    # 3 é Maio
    # 4 é Junho
    # 5 é Julho
    # 6 é Agosto
    # 7 é Setembro
    # 8 é Outubro
    # 9 é Novembro
    # 10 é Dezembro

    
    #pegando o mês da data inicial
    start_date = dates[0]
    start_date = start_date.split("/")
    start_mes = start_date[1]
    start_mes = int(start_mes) - 2

    #pegando o mês da data final
    end_date = dates[-1]
    end_date = end_date.split("/")
    end_mes = end_date[1]
    end_mes = int(end_mes) - 2
        
    tabelasMeses = browser.find_element(By.ID, "calendarios")
    meses = tabelasMeses.find_elements(By.TAG_NAME, "table")

    #iterando sobre o intervalo de meses
    for mes in range(start_mes, end_mes + 1):
        nomeMes = meses[mes].find_element(By.TAG_NAME, "caption").text
        # <caption>Junho - 2024</caption>
        ano = nomeMes.split(" - ")[1]
        print(nomeMes)
        tbody = meses[mes].find_element(By.TAG_NAME, "tbody")
        trs = tbody.find_elements(By.TAG_NAME, "tr")
        for tr in trs:
            tds = tr.find_elements(By.TAG_NAME, "td")
            for td in tds:
                estilo = td.get_attribute("style")
                # print("estilo: ", estilo)
                # deve ignorar se já foi ministrada aula (background: #6CDF46; / rgb(108, 223, 70);) ou 
                # se já foi cancelada (background: #FFFF99; / rgb(255, 255, 153);) 
                
                if estilo == "background: rgb(108, 223, 70);" or estilo == "background: rgb(255, 255, 153);":
                    continue
                else:
                    print(td.text)
                    # se tem link, é dia de aula
                    try:
                        a = td.find_element(By.TAG_NAME, "a")
                        dia = a.text
                        numDia = int(dia)

                        if numDia < 10:
                            dia = "0" + str(dia)

                        print("este é dia letivo: ", dia)

                        # se mes tiver só um dígito, adicionar um zero à esquerda
                        if mes < 10:
                            numMes = "0" + str(mes + 2)
                        else:
                            numMes = str(mes + 2)

                        data = dia + "/" + numMes + "/" + ano
                        print("data montada: ", data)

                        # se a aula estiver na lista de dates, cancelar
                        if data in dates:
                            print("cancelando aula: ", data)
                            a.click()# clicando no link
                            botaoCancelar = browser.find_element(By.XPATH, "//input[@type='submit' and @value='Cancelar Aula']")
                            botaoCancelar.click()
                            # Mudar o foco para o alerta
                            alerta = Alert(browser)
                            # Aceitar o alerta (clicar em "OK")
                            alerta.accept()
                            botaoCadastrar = browser.find_element(By.XPATH, "//input[@type='submit' and @value='Cadastrar']")
                            botaoCadastrar.click()

                            # voltar para a página de frequência
                            browser.find_element(By.XPATH, "//div[contains(text(), 'Alunos')]").click()

                            browser.find_element(By.XPATH, "//div[contains(text(), 'Lançar Frequência')]").click()
                        
                    except NoSuchElementException:
                        pass

    '''
    for mes in meses:
        nomeMes = mes.find_element(By.TAG_NAME, "caption").text
        print(nomeMes)
        # nos dias de aulas os elementos tem a propriedade css de background-color igual a #6CDF46
        #dias = mes.find_elements(By.XPATH, ".//tbody/tr/td[@style=' background: #6CDF46; ']")

        tbody = mes.find_element(By.TAG_NAME, "tbody")

        trs = tbody.find_elements(By.TAG_NAME, "tr")

        for tr in trs:
            tds = tr.find_elements(By.TAG_NAME, "td")
            for td in tds:
                print(td.text)
                # se tem link, é dia de aula
                try:
                    a = td.find_element(By.TAG_NAME, "a")
                    print("este é dia letivo: ", a.text)
                except NoSuchElementException:
                    pass
                
    '''

    setDates(dates)

def cancelar_aula(data):    
    pass

def setDates(dates):
    print(dates)