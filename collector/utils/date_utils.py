import re
import pandas as pd

def conversao_segura(value):
    try:
        return int(value)
    except(ValueError, TypeError):
        return None
    
def gerar_dataframe(lista, colunas):
    df = pd.DataFrame(lista, columns=colunas)
    return df


def format_stat_name(name):
    return name.lower().replace(' ', '_').replace('-', '_')

def map_period_to_half(period):
    if period == 'ALL':
        return 0
    elif period == '1ST':
        return 1
    elif period == '2ND':
        return 2
    else:
        return None
    
def dividir_lotes(jogos, tamanho_lote):
    for i in range(0, len(jogos), tamanho_lote):
        yield jogos[i : i + tamanho_lote]

def parse_statistics(json_data, match_id, home_team_id, away_team_id):
    registros = []
    try:
        for periodo in json_data.get('statistics', []):
                    period = periodo.get('period')
                    half = map_period_to_half(period)

                    for group in periodo.get('groups', []):
                        for stat in group.get('statisticsItems', []):
                            stat_name = format_stat_name(stat.get('name'))

                            registros.append({
                                'match_id': match_id,
                                'team_id': home_team_id,
                                'half': half,
                                'stat_name': stat_name,
                                'value': stat.get('home', 0) if stat.get('home') is not None else 0
                            })

                            registros.append({
                                'match_id': match_id,
                                'team_id': away_team_id,
                                'half': half,
                                'stat_name': stat_name,
                                'value': stat.get('away', 0) if stat.get('away') is not None else 0
                            })
    except Exception as e:
         print(f"Erro no parse do match {match_id}: {e}")
    
    return registros

def trata_stats(dataframe):
    df_tratado = expandir_estatisticas_em_linhas(dataframe)

    df_tratado['value'] = df_tratado['value'].apply(converter_percentual)

    return df_tratado
     

def expandir_estatisticas_em_linhas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Expande estatísticas no formato 'X/Y (Z%)' em três novas linhas:
    - stat_name_complete: X
    - stat_name_total: Y
    - stat_name_accurate: Z (em decimal)

    Args:
        df (pd.DataFrame): DataFrame no formato long, com colunas
            ['match_id',team_id, 'half', 'stat_name', 'value']

    Returns:
        pd.DataFrame: DataFrame com estatísticas expandidas.
    """

    def expandir_linha(row):
        # Tenta casar com o padrão 'X/Y (Z%)'
        match = re.match(r'(\d+)/(\d+)\s+\((\d+)%\)', str(row['value']))
        if not match:
            return pd.DataFrame([row])  # Retorna a linha original se não casar

        completo = int(match.group(1))
        total = int(match.group(2))
        acuracia = int(match.group(3)) / 100

        base = {
            'match_id': row['match_id'],
            'team_id' : row['team_id'],
            'half': row['half']
        }

        # Cria 3 novas linhas com os valores separados
        return pd.DataFrame([
            {**base, 'stat_name': f"{row['stat_name']}_complete", 'value': completo},
            {**base, 'stat_name': f"{row['stat_name']}_total",    'value': total},
            {**base, 'stat_name': f"{row['stat_name']}_accurate", 'value': acuracia},
        ])

    # Aplica a função linha a linha e concatena os resultados
    linhas_expandidas = df.apply(expandir_linha, axis=1)
    df_resultado = pd.concat(linhas_expandidas.to_list(), ignore_index=True)

    return df_resultado

def converter_percentual(valor):
    if isinstance(valor, str) and valor.strip().endswith('%'):
        try:
            return float(valor.strip().replace('%', '')) / 100
        except ValueError:
            return valor  # Retorna original se não for conversível
    return valor

def classificar_formato(rounds):
    nomes = [r.get("name", "").lower() for r in rounds if "name" in r]
    total_rodadas = len(rounds)

    # Misto: presença de fases como grupos + mata-mata
    if any("group" in nome or "qualification" in nome for nome in nomes) and any("final" in nome or "quarter" in nome or "semi" in nome for nome in nomes):
        return "misto"
    
    # Pontos corridos: rodadas numéricas, sem nome (ex: Brasileirão)
    if total_rodadas >= 30 and all("name" not in r for r in rounds):
        return "pontos_corridos"
    
    # Mata-mata: rodadas com nome e fases eliminatórias
    if any("final" in nome or "quarter" in nome or "semi" in nome for nome in nomes):
        return "mata-mata"
    
    return "desconhecido"