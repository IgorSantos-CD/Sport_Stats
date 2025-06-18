
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