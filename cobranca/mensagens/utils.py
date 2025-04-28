import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

MENSAGEM_PADRAO = "Olá, somos do financeiro. Estamos enviando essa mensagem pois verificamos que o senhor possui um boleto pendente, teria alguma previsão para pagamento?"

# Caminho do ChromeDriver
CHROMEDRIVER_PATH = 'CAMINHO/para/chromedriver'  # 👉 Coloque o caminho aqui

def processar_planilha(arquivo):
    df = pd.read_excel(arquivo)
    contatos = df['contato'].tolist()

    enviar_mensagens_whatsapp(contatos)
    return contatos

def enviar_mensagens_whatsapp(lista_contatos):
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=./User_Data")  # mantém sessão logada no WhatsApp
    service = Service(CHROMEDRIVER_PATH)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://web.whatsapp.com/')

    input("Após escanear o QR Code no navegador e o WhatsApp Web carregar completamente, pressione ENTER aqui...")

    for numero in lista_contatos:
        try:
            link = f"https://web.whatsapp.com/send?phone={numero}&text={MENSAGEM_PADRAO}"
            driver.get(link)
            time.sleep(10)  # aguardar chat abrir

            enviar_botao = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            enviar_botao.click()
            print(f"Mensagem enviada para {numero}")

            time.sleep(10)  # esperar entre mensagens para evitar bloqueio
        except Exception as e:
            print(f"Erro ao enviar para {numero}: {e}")
            time.sleep(5)

    driver.quit()
