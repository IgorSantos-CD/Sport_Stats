import time
import random

def delay_aleatorio(minimo=1.5, maximo=4.0):
    tempo = random.uniform(minimo, maximo)
    print(f"⏳ Aguardando {round(tempo, 2)} segundos para evitar bloqueio...")
    time.sleep(tempo)

def retry(max_tentativas=3, backoff=2):
    """
    Decorador para fazer retry com backoff exponencial.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            tentativas = 0
            while tentativas < max_tentativas:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    tentativas += 1
                    espera = backoff ** tentativas
                    print(f"⚠️ Erro: {e}. Tentando novamente em {espera} segundos...")
                    time.sleep(espera)
            raise Exception(f"❌ Falha após {max_tentativas} tentativas.")
        return wrapper
    return decorator