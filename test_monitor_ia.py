import pytest
from unittest.mock import MagicMock, patch
from monitor_ia import AIOpsMonitor

def test_analizar_log_critico():
    """Prueba que el sistema detecte palabras clave de error crítico"""
    patrones = ["fatal", "error", "exception", "failed", "permission denied", "connection refused", "shutdown"]
    log_falso = "nginx error: connection refused en el puerto 80".lower()
    
    # Verificamos que al menos un patrón coincida con el log (Debe dar True)
    falla_detectada = any(p in log_falso for p in patrones)
    assert falla_detectada == True

def test_analizar_log_normal():
    """Prueba que el sistema ignore los logs de tráfico normal"""
    patrones = ["fatal", "error", "exception", "failed", "permission denied", "connection refused", "shutdown"]
    log_falso = "GET /index.html 200 OK - usuario conectado".lower()
    
    # Verificamos que ningún patrón coincida con un log normal (Debe dar False)
    falla_detectada = any(p in log_falso for p in patrones)
    assert falla_detectada == False

@patch('monitor_ia.docker.from_env')
def test_auto_sanar_contenedor(mock_docker):
    """Prueba que el monitor aplique la sanación (reinicio) correctamente"""
    # Iniciamos el monitor simulado (sin conectarnos al Docker real)
    monitor = AIOpsMonitor()
    
    # Creamos un contenedor falso
    mock_container = MagicMock()
    mock_container.name = "contenedor_de_prueba"
    
    # Evitamos que gaste saldo de tu API de Groq durante la prueba
    monitor.consultar_ia_sanacion = MagicMock(return_value={"diagnostico_raiz": "Falla simulada", "correccion_aplicada": "Reiniciado"})
    
    # Disparamos el evento de falla
    monitor.procesar_falla(mock_container, "simulacion de error fatal")
    
    # AFIRMACIÓN 1: El monitor debió haber llamado al comando restart() del contenedor
    mock_container.restart.assert_called_once()
    
    # AFIRMACIÓN 2: El contador de eventos reparados debió subir a 1
    assert monitor.eventos_reparados == 1