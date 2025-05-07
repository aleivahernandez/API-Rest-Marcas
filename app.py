from flask import Flask, request, jsonify
from SBERT_Multilingue import buscar_marcas_similares_sbert
from BETO import buscar_marcas_similares_beto

app = Flask(__name__)

@app.route('/buscar_marcas', methods=['POST'])
def buscar_marcas():
    data = request.json
    input_marca = data.get('marca')
    top_n = data.get('top_n', 5)

    resultados_sbert = buscar_marcas_similares_sbert(input_marca, top_n)
    resultados_beto = buscar_marcas_similares_beto(input_marca, top_n)

    return jsonify({'resultados_sbert': resultados_sbert, 'resultados_beto': resultados_beto})

if __name__ == '__main__':
    app.run(debug=True)
