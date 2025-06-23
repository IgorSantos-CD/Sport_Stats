import pandas as pd
from selenium_local.automation import iniciar_driver
from selenium.webdriver.common.by import By
from utils import transformar_json, conversao_segura

def coletar_paises():
    driver = iniciar_driver()
    driver.get("https://www.sofascore.com/api/v1/sport/football/categories/all")

    pre = driver.find_element(By.TAG_NAME, 'pre').text
    json_categories = transformar_json(pre)

    lista_paises = []
    for i in json_categories['categories']:
        infos ={
            'id' : i.get('id',None),
            'name' : i.get('name', None),
            'slug' : i.get('slug',None),
            'priority' : conversao_segura(i.get('priority',None)),
            'flag' : i.get('flag', None)
        }
        lista_paises.append(infos)

    driver.quit()
    
    df_paises = pd.DataFrame(lista_paises, columns=['id', 'name','slug_name','priority','flag'])
    df_paises['priority'] = df_paises['priority'].astype('Int64')
    df_paises = df_paises.where(pd.notna(df_paises), None)

    df_paises = df_paises.astype(object)
    df_paises = df_paises.where(pd.notna(df_paises), None)

    return df_paises

    

