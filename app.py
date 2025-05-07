from flask import Flask, request, jsonify
import pandas as pd
from SBERT_Multilingue import buscar_marcas_similares as modelo_sbert
from BETO import buscar_marcas_similares as modelo_beto

app = Flask(__name__)

def combinar_modelos_v2_unicos(marca_input, umbral=80.0):
    resultados = []
    for modelo_func, nombre_modelo in [
        (modelo_beto, "BETO"),
        (modelo_sbert, "SBERT")
    ]:
        try:
            salida = modelo_func(marca_input)
            for i, (marca, similitud) in enumerate(salida, start=1):
                if similitud >= umbral:
                    resultados.append({
                        "Marca": marca.strip().lower(),
                        "Similitud (%)": round(similitud, 2),
                        "Modelo": nombre_modelo
                    })
        except Exception as e:
            print(f"Error en {nombre_modelo}: {e}")

    if not resultados:
        return pd.DataFrame(columns=["Modelo", "Marca", "Similitud (%)"])

    df = pd.DataFrame(resultados)
    df = df.sort_values("Similitud (%)", ascending=False)
    df = df.drop_duplicates(subset="Marca", keep="first")
    df["Marca"] = df["Marca"].str.title()
    df = df.reset_index(drop=True)
    df.index += 1
    df.index.name = "Índice"
    return df

@app.route('/buscar_marcas', methods=['POST'])
def buscar_marcas():
    data = request.json
    marca = data.get('marca')
    umbral = data.get('umbral', 80.0)

    if not marca:
        return jsonify({'error': 'No se proporcionó la marca'}), 400

    try:
        df_resultados = combinar_modelos_v2_unicos(marca.strip(), umbral=umbral)
        resultados = df_resultados.to_dict(orient='records')
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
