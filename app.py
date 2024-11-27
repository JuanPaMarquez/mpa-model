from flask import Flask, request, jsonify
from flask_cors import CORS
from mensajes import message
import os
import random
from flask import make_response

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://juanpamarquez.github.io"}})

@app.after_request
def add_cors_headers(response):
  response.headers['Access-Control-Allow-Origin'] = 'https://juanpamarquez.github.io'
  response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
  response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
  return response

@app.route('/evaluar/<int:id>', methods=['POST'])
def evaluar_estudiantes(id):
  data = request.get_json()  # Obtener JSON del cuerpo de la solicitud
  
  # Validación para asegurarse de que la entrada es una lista
  if not isinstance(data, list):
      return jsonify({"error": "Se espera una lista de estudiantes"}), 400
  
  resultados = []  # Lista para almacenar las recomendaciones
  
  # Iterar sobre cada estudiante en la lista
  for estudiante in data:
    try:
      nombre = estudiante['nombre']
      nota1 = float(estudiante['nota15c1'])
      nota2 = float(estudiante['nota20c1'])
      nota3 = float(estudiante['nota15c2'])
      nota4 = float(estudiante['nota20c2'])
      nota5 = float(estudiante['nota10c3'])
      nota6 = float(estudiante['nota20c3'])
      promedio = (nota1 * 0.15 + nota2 * 0.2 + nota3 * 0.15 + nota4 * 0.2 + nota5 * 0.1 + nota6 * 0.2)
      if promedio < 2.0:
          recomendacion = random.choice(message[1])  # Escoge un mensaje aleatorio de la categoría urgente
      elif promedio < 3.0:
          recomendacion = random.choice(message[2])  # Escoge un mensaje aleatorio de la categoría menor urgencia
      elif promedio < 4.0:
          recomendacion = random.choice(message[3])  # Escoge un mensaje aleatorio de la categoría normal
      elif promedio < 4.5:
          recomendacion = random.choice(message[4])  # Escoge un mensaje aleatorio de la categoría sugerencias
      else:
          recomendacion = random.choice(message[5])  # Escoge un mensaje aleatorio de la categoría ánimo

            
      resultados.append({
        "idprediccion": id,
        "estudiante": nombre,
        "resultado": recomendacion
      })
    except KeyError as e:
      return jsonify({"error": f"Falta la clave {str(e)} en el JSON del estudiante"}), 400
    except ValueError:
      return jsonify({"error": "Las notas deben ser valores numéricos"}), 400
  
  return jsonify(resultados), 200  # Devolver la lista de resultados

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
