import pandas as pd
from selenium_local import iniciar_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from time import sleep

#INICIALIZANDO O NAVEGADOR E ACESSANDO A PÁGINA PARA SCRAPPING
driver = iniciar_driver()
driver.get("https://www.sofascore.com/api/v1/sport/football/categories/all")

json_categorias = json.loads(driver.find_element(By.XPATH, "/html/body/pre").text)

dicionario_paises = {}
for item in json_categorias['categories']:
    name = item['name']
    name_id = item['id']
    dicionario_paises[name] = name_id

