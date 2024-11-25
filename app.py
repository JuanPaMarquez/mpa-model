from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Función para calcular la recomendación
def calcular_recomendacion(id, nombre, nota1, nota2, nota3, nota4, nota5, nota6):
  promedio = (nota1 * 0.15 + nota2 * 0.2 + nota3 * 0.15 + nota4 * 0.2 + nota5 * 0.1 + nota6 * 0.2)
  if promedio >= 4.5:
    recomendacion = "¡Excelente desempeño! Sigue así."
  elif 4 <= promedio < 4.5:
      recomendacion = "Muy buen trabajo, estás muy cerca de la excelencia."
  elif 3.5 <= promedio < 4:
      recomendacion = "Buen trabajo, pero puedes mejorar."
  elif 3 <= promedio < 3.5:
      recomendacion = "Buen esfuerzo, pero aún hay margen para mejorar."
  elif 2.5 <= promedio < 3:
      recomendacion = "Debes esforzarte más. ¡Tú puedes!"
  elif 2 <= promedio < 2.5:
      recomendacion = "Necesitas mejorar significativamente. ¡No te rindas!"
  elif 1.5 <= promedio < 2:
      recomendacion = "Esfuerzo insuficiente. ¡Puedes hacerlo mejor!"
  elif 1 <= promedio < 1.5:
      recomendacion = "Necesitas poner mucho más esfuerzo. ¡No te desanimes!"
  elif 0.5 <= promedio < 1:
      recomendacion = "Esfuerzo muy bajo. ¡Tienes que trabajar mucho más!"
  else:
      recomendacion = "Esfuerzo mínimo. ¡Debes esforzarte mucho más!"
    
  return {
    "idprediccion": id,
    "estudiante": nombre,
    "resultado": recomendacion
}

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
      nombre = estudiante['estudiante']
      nota1 = float(estudiante['nota15c1'])
      nota2 = float(estudiante['nota20c1'])
      nota3 = float(estudiante['nota15c2'])
      nota4 = float(estudiante['nota20c2'])
      nota5 = float(estudiante['nota10c3'])
      nota6 = float(estudiante['nota20c3'])
    except (KeyError, ValueError):
      return jsonify({"error": f"Datos inválidos para el estudiante {estudiante.get('estudiante', 'desconocido')}"}), 400
    
    # Calcular recomendación y agregar a la lista
    resultado = calcular_recomendacion(id, nombre, nota1, nota2, nota3, nota4, nota5, nota6)
    resultados.append(resultado)
  
  return jsonify(resultados)  # Devolver la lista de resultados

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
