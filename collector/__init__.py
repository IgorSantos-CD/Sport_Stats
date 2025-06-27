from.scrapers import coletar_paises, coletar_competicoes, coletar_seasons, coletar_rodadas, coletar_partidas_por_rodada, coletar_stats_partida
from .selenium_local import iniciar_driver
from .utils import transformar_json, delay_aleatorio, conversao_segura, gerar_dataframe, classificar_formato, atualizar_db, atualizar_registros, buscar_partidas_para_coletar_stats