from collector.selenium_local import iniciar_driver
from database import executar_query
from selenium.webdriver.common.by import By
from collector.utils import transformar_json, gerar_dataframe

def coletar_competicoes():
    driver = iniciar_driver()
    driver.get("https://www.sofascore.com/api/v1/config/default-unique-tournaments/BR/football")

    pre = driver.find_element(By.TAG_NAME, 'pre').text
    json_competitions = transformar_json(pre)

    competicoes = []
    for comp in json_competitions['uniqueTournaments']:
        location_name = comp.get('category', {}).get('name', None)
        try:
            location_id = executar_query(f"SELECT id FROM countries WHERE name = '{location_name}'", fetch='one')['id'][0]
        except Exception as e:
            location_id = None
            print("Não foi possivel localizar o id da competição")

        info = {
            'id' : comp.get('id', None),
            'name' : comp.get('name', None),
            'slug_name' : comp.get('slug', None),
            'primary_color' : comp.get('primaryColorHex', None),
            'secondary_color' : comp.get('secondaryColorHex', None),
            'location_name' : location_name,
            'location_id' : location_id,
            'location_flag' : comp.get('category', {}).get('flag', None),
            'sport_name' : comp.get('category',{}).get('sport', {}).get('name',None)
        }
        
        competicoes.append(info)
    
    colunas = [
        'id','name','slug_name','primary_color', 'secondary_color',
        'location_name','location_id','location_flag','sport_name'
        ]
    
    df = gerar_dataframe(competicoes, colunas=colunas)
    driver.quit()
    return df

    