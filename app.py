from flask import Flask, jsonify, render_template
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from api.herramientas_manuales import herramientas_manual_bp

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

@app.route('/pago')
def vista_pago():
    return render_template('pago.html')

if __name__ == "__main__":
    app.run(debug=True)
