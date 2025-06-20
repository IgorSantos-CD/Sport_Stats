
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