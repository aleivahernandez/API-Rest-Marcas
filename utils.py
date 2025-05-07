import pandas as pd
from sentence_transformers import SentenceTransformer, util

def cargar_modelo(modelo):
    try:
        return SentenceTransformer(modelo)
    except Exception as e:
        print(f"⚠️ Error cargando modelo: {e}")
        return None

def cargar_csv(ruta_csv):
    try:
        df = pd.read_csv(ruta_csv)
        return df["NombreProducto"].astype(str).str.lower().tolist()
    except Exception as e:
        print(f"⚠️ Error cargando CSV: {e}")
        return []

def buscar_marcas_similares(model, marca_textos, marca_embeddings, input_marca, top_n=5):
    input_marca = input_marca.lower()
    input_embedding = model.encode(input_marca, convert_to_tensor=True)
    similitudes = util.pytorch_cos_sim(input_embedding, marca_embeddings)[0]
    top_resultados = sorted(
        zip(marca_textos, similitudes),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]
    return [(marca, float(score) * 100) for marca, score in top_resultados]
