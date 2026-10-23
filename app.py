from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

repositorio_asistencia = [
    {
        "id": 1,
        "empleado_id": "EMP-1020",
        "fecha": "2026-10-20",
        "hora": "08:00:22",
        "tipo": "ENTRADA"
    }
]

@app.route('/asistencia', methods=['GET'])
def obtener_historial():
    return jsonify({
        "mensaje": "Historial de asistencia recuperado con éxito",
        "datos": repositorio_asistencia
    }), 200

@app.route('/asistencia', methods=['POST'])
def registrar_marca():
    datos_recibidos = request.get_json()

    if not datos_recibidos or 'empleado_id' not in datos_recibidos or 'tipo' not in datos_recibidos:
        return jsonify({
            "error": "Datos inválidos. Se requiere 'empleado_id' y 'tipo' (ENTRADA/SALIDA)."
        }), 400

    tipo_marca = datos_recibidos['tipo'].upper()
    if tipo_marca not in ['ENTRADA', 'SALIDA']:
        return jsonify({
            "error": "El tipo de asistencia debe ser 'ENTRADA' o 'SALIDA'."
        }), 400

    ahora = datetime.now()
    
    nueva_asistencia = {
        "id": len(repositorio_asistencia) + 1,
        "empleado_id": datos_recibidos['empleado_id'],
        "fecha": ahora.strftime("%Y-%m-%d"),
        "hora": ahora.strftime("%H:%M:%S"),
        "tipo": tipo_marca
    }

    repositorio_asistencia.append(nueva_asistencia)

    return jsonify({
        "mensaje": "Registro de asistencia completado correctamente",
        "datos": nueva_asistencia
    }), 201

@app.route('/asistencia/<int:registro_id>', methods=['DELETE'])
def eliminar_registro(registro_id):
    global repositorio_asistencia
    
    existe = any(reg['id'] == registro_id for reg in repositorio_asistencia)
    
    if not existe:
        return jsonify({"error": "El registro de asistencia no fue encontrado."}), 404

    repositorio_asistencia = [reg for reg in repositorio_asistencia if reg['id'] != registro_id]

    return jsonify({
        "mensaje": f"Registro con ID {registro_id} eliminado correctamente del sistema"
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
