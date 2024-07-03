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


def extrair_dias_letivos(browser, start_mes, end_mes, datasSelecionadas):
    diasLetivos = []
    try:
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
                        # se tem link, é dia de aula
                        try:
                            a = td.find_element(By.TAG_NAME, "a")
                            dia = a.text
                            numDia = int(dia)

                            if numDia < 10:
                                dia = "0" + str(dia)

                            #print("este é dia letivo: ", dia)

                            # se mes tiver só um dígito, adicionar um zero à esquerda
                            if (mes+2) < 10:
                                numMes = "0" + str(mes + 2)
                            else:
                                numMes = str(mes + 2)

                            data = dia + "/" + numMes + "/" + ano
                            #print("data montada: ", data)

                            if data in datasSelecionadas:
                                diasLetivos.append(data)

                        except NoSuchElementException as e:
                            #print("Erro ao extrair dias letivos:", e)
                            pass
    except StaleElementReferenceException as e:
        #print("Erro ao extrair dias letivos:", e)
        pass
    return diasLetivos

def cancelar_dias_letivos(browser, start_mes, end_mes, dates, diasLetivos):
    try:
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
                    # deve ignorar se:
                        # feriado (color: #FF0000;) ou
                        # já foi ministrada aula (background: #6CDF46; / rgb(108, 223, 70);) ou 
                        # se já foi cancelada (background: #FFFF99; / rgb(255, 255, 153);) 
                    
                    if estilo == "color: #FF0000;" or estilo == "background: rgb(108, 223, 70);" or estilo == "background: rgb(255, 255, 153);":
                        continue
                    else:
                        #print(td.text)
                        # se tem link, é dia de aula
                        try:
                            a = td.find_element(By.TAG_NAME, "a")
                            dia = a.text
                            numDia = int(dia)

                            if numDia < 10:
                                dia = "0" + str(dia)

                            #print("este é dia letivo: ", dia)

                            # se mes tiver só um dígito, adicionar um zero à esquerda
                            if (mes+2) < 10:
                                numMes = "0" + str(mes + 2)
                            else:
                                numMes = str(mes + 2)

                            data = dia + "/" + numMes + "/" + ano
                            #print("data montada: ", data)

                            # se a aula estiver na lista de dates, cancelar
                            if data in diasLetivos:
                                #print("cancelando aula: ", data)                            
                                a.click()# clicando no link
                                botaoCancelar = browser.find_element(By.XPATH, "//input[@type='submit' and @value='Cancelar Aula']")
                                botaoCancelar.click()

                                # Mudar o foco para o alerta
                                alerta = Alert(browser)
                                # Aceitar o alerta (clicar em "OK")
                                alerta.accept()

                                #print("alert OK", data)

                                botaoCadastrar = WebDriverWait(browser, 10).until(                            
                                    EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Cadastrar']"))
                                )
                                botaoCadastrar.click()
                                #print("cadastrando cancelamento da aula: ", data)

                                #remover de dates
                                diasLetivos.remove(data)
                        except NoSuchElementException as e:
                            #print("Erro ao extrair dias letivos:", e)
                            pass
    except StaleElementReferenceException as e:
        #print("Erro ao extrair dias letivos:", e)
        pass
                
'''
print("Dias letivos: ", diasLetivos)

for dia in diasLetivos:
    #extrair o dia. Ex: 01/01/2024
    quebrado = dia.split("/")

    numDia = quebrado[0]
    numMes = quebrado[1]
    numAno = quebrado[2]

    # tirar o zero à esquerda do dia
    if numDia[0] == "0":
        numDia = numDia[1]

    # tirar o zero à esquerda do mes
    if numMes[0] == "0":
        numMes = numMes[1]

    # Criar as partes da string
        parte1 = f"'dia':'{numDia}'"
        parte2 = f"'mes':'{numMes}'"
        parte3 = f"'ano':'{numAno}'"

    xpath = f"//a[contains(@onclick, {parte1}) and contains(@onclick, {parte2}) and contains(@onclick, {parte3})]"

    # Esperar até que o elemento esteja presente
    elemento = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    
    # Clicar no elemento
    elemento.click()
'''

def pedir_senha(USERNAME):
        senha = simpledialog.askstring("Senha do SIGAA", "Ei " + USERNAME + ", digite sua senha do SIGAA:", initialvalue="", show='*')
        return senha

def extrair_notas_sigaa(config, datasSelecionadas):
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
    
    browser.find_element(By.XPATH, "//div[contains(text(), 'Alunos')]").click()
    
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
    start_date = datasSelecionadas[0]
    start_date = start_date.split("/")
    start_mes = start_date[1]
    start_mes = int(start_mes) - 2

    #pegando o mês da data final
    end_date = datasSelecionadas[-1]
    end_date = end_date.split("/")
    end_mes = end_date[1]
    end_mes = int(end_mes) - 2

    #clicar em lançar frequência
    browser.find_element(By.XPATH, "//div[contains(text(), 'Lançar Frequência')]").click()

    #extrair os dias letivos do calendário
    diasLetivos = extrair_dias_letivos(browser, start_mes, end_mes, datasSelecionadas)

    # enquanto tiver elementos em diasLetivos, deve cancelar a aula
    while diasLetivos:
        browser.find_element(By.XPATH, "//div[contains(text(), 'Lançar Frequência')]").click()
        cancelar_dias_letivos(browser, start_mes, end_mes, datasSelecionadas, diasLetivos)
    
    #volta para a página de frequência
    browser.find_element(By.XPATH, "//div[contains(text(), 'Lançar Frequência')]").click()