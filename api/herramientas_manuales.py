from flask import Blueprint, jsonify
import json
import os

herramientas_manual_bp = Blueprint('herramientas_manual', __name__)
BASE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'herramientas_manuales')

@herramientas_manual_bp.route("/api/herramientas-manuales/<nombre_archivo>", methods=["GET"])
def get_herramienta(nombre_archivo):
    try:
        file_path = os.path.join(BASE_DIR, f"{nombre_archivo}.json")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Archivo no encontrado"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error al decodificar el archivo JSON"}), 500
