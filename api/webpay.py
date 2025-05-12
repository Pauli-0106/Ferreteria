# proyecto/servicios/webpay.py
import os
import requests

def crear_transaccion(monto, orden_compra):
    # Simula una respuesta exitosa de WEBPAY
    return {
        "token": "TBK-ACADEMICO-123",
        "url_redireccion": "http://localhost:5000/confirmacion"
    }