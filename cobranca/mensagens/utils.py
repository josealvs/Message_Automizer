import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

MENSAGEM_PADRAO = "Olá, somos do financeiro. Estamos enviando essa mensagem pois verificamos que o senhor possui um boleto pendente, teria alguma previsão para pagamento?"

# Caminho do ChromeDriver
CHROMEDRIVER_PATH = 'CAMINHO/para/chromedriver'  # 👉 ajuste aqui para o seu caminho

def processar_planilha(arquivo):
    df = pd.read_excel(arquivo)
    contatos = df['contato'].tolist()

    enviar_mensagens_whatsapp(contatos)
    return contatos

def enviar_mensagens_whatsapp(lista_contatos):
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=./User_Data")  # mantém a sessão logada no WhatsApp Web
    service = Service(CHROMEDRIVER_PATH)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://web.whatsapp.com/')

    input("🚀 Escaneie o QR Code no navegador e, quando o WhatsApp Web carregar completamente, pressione ENTER aqui...")

    for numero in lista_contatos:
        try:
            link = f"https://web.whatsapp.com/send?phone={numero}&text={MENSAGEM_PADRAO}"
            driver.get(link)

            time.sleep(10)  # aguarda chat abrir
            
            enviar_botao = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            enviar_botao.click()
            print(f"✅ Mensagem enviada para {numero}")

            # Sleep aleatório entre 5 e 15 segundos
            tempo_espera = random.randint(5, 15)
            print(f"⌛ Aguardando {tempo_espera} segundos antes do próximo envio...")
            time.sleep(tempo_espera)
        
        except Exception as e:
            print(f"❌ Erro ao enviar para {numero}: {e}")
            time.sleep(5)  # pequeno delay mesmo em erro

    driver.quit()
