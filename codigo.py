import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Define la URL base de la tabla de valores de la UF del SII
base_url = 'https://www.sii.cl/valores_y_fechas/uf/uf{}.htm'

# Define la fecha mínima que se puede consultar
min_date = '01-01-2013'

# Define la ruta de la API para consultar la UF por fecha


@app.route('/uf/<date>')
def get_uf(date):
    # Verifica si la fecha ingresada es válida
    if date < min_date:
        return jsonify({'error': 'La fecha mínima que se puede consultar es el 01-01-2013'}), 400
    # Obtiene el año de la fecha ingresada
    year = date.split('-')[0]
    # Construye la URL de la tabla de valores de la UF del SII para el año correspondiente
    url = base_url.format(year)
    # Realiza la solicitud HTTP GET a la URL construida
    response = requests.get(url)
    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        # Obtiene el contenido HTML de la respuesta
        html_content = response.content.decode('utf-8')
        # Busca el valor de la UF correspondiente a la fecha ingresada en el contenido HTML
        uf_value = None
        for line in html_content.split('\n'):
            if date in line:
                uf_value = line.split(
                    '>')[-2].split('<')[0].replace('.', '').replace(',', '.')
                break
        # Verifica si se encontró el valor de la UF correspondiente a la fecha ingresada
        if uf_value is not None:
            # Retorna el valor de la UF en formato JSON
            return jsonify({'uf': uf_value}), 200
        else:
            # Retorna un error si no se encontró el valor de la UF correspondiente a la fecha ingresada
            return jsonify({'error': 'No se encontró el valor de la UF para la fecha ingresada'}), 404
    else:
        # Retorna un error si la solicitud HTTP no fue exitosa
        return jsonify({'error': 'No se pudo obtener la tabla de valores de la UF del SII'}), 500


# Ejecuta la aplicación en el puerto 5000
if __name__ == '__main__':
    app.run(port=5000)
