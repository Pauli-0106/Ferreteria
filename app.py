from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)

DATA_PATH = "data"

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

@app.route("/")
def vista_inventario():
    # Cargar los datos desde los archivos JSON
    datos = cargar_todos_los_datos()
    return render_template("inventario.html", inventario=datos)

@app.route("/api")
def api_inventario():
    # Cargar los datos desde los archivos JSON y devolverlos como JSON
    datos = cargar_todos_los_datos()
    return jsonify(datos)

@app.route('/confirmacion')
def vista_confirmacion():
    return render_template('confirmacion.html')

@app.route('/index')
def vista_index():
    return render_template('index.html')

@app.route('/nosotros')
def vista_nosotros():
    return render_template('nosotros.html')

@app.route('/pago')
def vista_pago():
    return render_template('pago.html')

if __name__ == "__main__":
    app.run(debug=True)
