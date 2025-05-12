from flask import Flask, jsonify, render_template , request
from api.webpay import crear_transaccion
import json
import os
import sys
from dotenv import load_dotenv
load_dotenv() 
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from api.herramientas_manuales import herramientas_manual_bp
from api.banco_central import obtener_tipo_cambio


app = Flask(__name__)

DATA_PATH = "data"
app.register_blueprint(herramientas_manual_bp)

def cargar_articulos():
    with open("data/articulos.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

@app.route("/api/articulos", methods=["GET"])
def obtener_articulos():
    articulos = cargar_articulos()
    return jsonify(articulos)

def cargar_todos_los_datos():
    inventario = {}
    for archivo in os.listdir(DATA_PATH):
        if archivo.endswith(".json"):
            nombre_categoria = archivo.replace(".json", "")
            ruta = os.path.join(DATA_PATH, archivo)
            with open(ruta, "r", encoding="utf-8") as f:
                inventario[nombre_categoria] = json.load(f)
    return inventario

@app.route("/api/categoria/<nombre_categoria>")
def api_categoria(nombre_categoria):
    ruta_archivo = os.path.join(DATA_PATH, f"{nombre_categoria}.json")
    ruta_carpeta = os.path.join(DATA_PATH, nombre_categoria)

    if os.path.isfile(ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return jsonify(datos)

    elif os.path.isdir(ruta_carpeta):
        todos_los_datos = []
        for archivo_nombre in os.listdir(ruta_carpeta):
            if archivo_nombre.endswith(".json"):
                ruta_json = os.path.join(ruta_carpeta, archivo_nombre)
                with open(ruta_json, "r", encoding="utf-8") as archivo:
                    datos = json.load(archivo)
                    todos_los_datos.extend(datos)
        return jsonify(todos_los_datos)

    return jsonify({"error": "Categoría no encontrada"}), 404


# Página principal e index
@app.route("/")
@app.route("/index")
def vista_index():
    return render_template("index.html")

# Vista inventario (ahora se accede con /inventario)
@app.route("/inventario")
def vista_inventario():
    datos = cargar_todos_los_datos()
    return render_template("inventario.html", inventario=datos)

# API de inventario completo
@app.route("/api")
def api_inventario():
    datos = cargar_todos_los_datos()
    return jsonify(datos)

# Otras páginas
@app.route('/confirmacion')
def vista_confirmacion():
    return render_template('confirmacion.html')

@app.route('/nosotros')
def vista_nosotros():
    return render_template('nosotros.html')

# Endpoint para buscar productos por código
@app.route("/api/producto/<codigo_producto>")
def obtener_producto(codigo_producto):
    inventario = cargar_todos_los_datos()
    for categoria, productos in inventario.items():
        for producto in productos:
            if producto.get("codigo_producto") == codigo_producto:
                return jsonify(producto)
    return jsonify({"error": "Producto no encontrado"}), 404

# Endpoint para verificar stock
@app.route("/api/stock/<codigo_producto>")
def verificar_stock(codigo_producto):
    producto = obtener_producto(codigo_producto).get_json()
    if "error" in producto:
        return jsonify(producto), 404
    return jsonify({"stock": producto["stock"]})

@app.route("/procesar-pago", methods=["POST"])
def procesar_pago():
    try:
        data = request.get_json()
        respuesta = crear_transaccion(
            monto=data["monto"],
            orden_compra=data["orden_compra"]
        )
        return jsonify(respuesta), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tipo-cambio")
def tipo_cambio():
    return jsonify(obtener_tipo_cambio())

if __name__ == "__main__":
    app.run(debug=True)
