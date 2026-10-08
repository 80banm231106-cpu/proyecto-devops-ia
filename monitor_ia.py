import docker
import time
from datetime import datetime

# Conectar al cliente de Docker de tu sistema operativo
# Requiere que Docker Desktop o el demonio de Docker esté corriendo
try:
    client = docker.from_env()
    print("Conectado a Docker exitosamente.")
except Exception as e:
    print(f"Error al conectar con Docker: {e}")
    exit()

def analizar_log_con_ia(log_text):
    """
    Aquí es donde entra la Inteligencia Artificial.
    En un entorno empresarial, aquí harías una petición a una API como OpenAI,
    o usarías un modelo de Machine Learning (ej. NLP) para clasificar el log.
    
    Para este código, simularemos la lógica de la IA buscando patrones
    que indican una caída inminente o un error crítico de software.
    """
    log_text = log_text.lower()
    
    # Patrones críticos que una IA identificaría como "Fallo en el servicio"
    patrones_criticos = ["fatal", "error", "exception", "segmentation fault", "connection refused"]
    
    for patron in patrones_criticos:
        if patron in log_text:
            return True # La IA determinó que el contenedor está fallando
            
    return False # El log es normal (informativo)

def auto_sanar_contenedor(container):
    """
    Función DevOps de Auto-Recuperación.
    Toma el tiempo de detección (MTTD) y el de reparación (MTTR).
    """
    nombre = container.name
    print(f"\n[ALERTA IA] Anomalía crítica detectada en el contenedor: {nombre}")
    
    # 1. Registrar tiempo de inicio de falla (Para métrica MTTD)
    tiempo_falla = time.time()
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando protocolo de auto-sanación...")
    
    # Reiniciar el contenedor
    container.restart()
    
    # 2. Registrar tiempo de recuperación (Para métrica MTTR)
    tiempo_recuperacion = time.time()
    mttr = tiempo_recuperacion - tiempo_falla
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Contenedor {nombre} reiniciado exitosamente.")
    print(f" MÉTRICA DE PROCESO OBTENIDA - Tiempo de recuperación (MTTR): {mttr:.2f} segundos\n")

def iniciar_monitoreo():
    print("Iniciando monitoreo inteligente de contenedores...")
    while True:
        # Buscar solo contenedores que tengan nuestra etiqueta "monitoreo_ia=activo"
        contenedores = client.containers.list(filters={"label": "monitoreo_ia=activo"})
        
        for container in contenedores:
            # Obtener las últimas líneas de los registros del contenedor
            logs = container.logs(tail=5).decode('utf-8')
            
            # Pasar los logs al análisis de IA
            es_critico = analizar_log_con_ia(logs)
            
            if es_critico:
                auto_sanar_contenedor(container)
                # Pausa breve para no ciclar el reinicio de inmediato
                time.sleep(10)
                
        # El monitor revisa el sistema cada 5 segundos
        time.sleep(5)

if __name__ == "__main__":
    iniciar_monitoreo()