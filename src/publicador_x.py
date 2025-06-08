from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import mysql.connector
from src.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def publicar_no_x():
    # Conecta no banco
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()

    # Link pré-definido para postar
    link_para_postar = "https://dev.to/devteam/exciting-community-news-were-partnering-with-google-ai-55c4"

    # Iniciar navegador
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get('https://x.com/compose/post')

    input("🛑 Faça login manualmente e pressione Enter para continuar...")

    # Espera até o campo de texto estar disponível
    wait = WebDriverWait(driver, 30)
    textarea = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='tweetTextarea_0']"))
    )

    # Envia o link para o campo de texto
    textarea.send_keys(link_para_postar)

    time.sleep(5)  # Espera prévia para preview carregar

    # Screenshot
    pasta_relatorios = os.path.join(os.path.dirname(__file__), '..', 'relatorios')
    os.makedirs(pasta_relatorios, exist_ok=True)
    screenshot_path = os.path.join(pasta_relatorios, 'preview_tweet.png')
    driver.save_screenshot(screenshot_path)

    print(f"✅ Screenshot salva em: {screenshot_path}")

    # (Opcional) Clicar no botão Postar
    try:
        post_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="tweetButton"]'))
        )
        # post_button.click()  # <<< Se quiser já postar, descomente esta linha!
        print("✅ Botão de Postar encontrado (não clicado para segurança).")
    except Exception as e:
        print(f"⚠️ Não foi possível localizar o botão de postar: {e}")

    driver.quit()
    print("✅ Tweet preparado com sucesso!")
