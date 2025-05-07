from utils import cargar_modelo, cargar_csv, buscar_marcas_similares

modelo = "paraphrase-multilingual-MiniLM-L12-v2"
ruta_csv = "IGS - Consolidado.csv"

marca_textos = cargar_csv(ruta_csv)
model = cargar_modelo(modelo)
marca_embeddings = model.encode(marca_textos, convert_to_tensor=True)

def buscar_marcas_similares_sbert(input_marca, top_n=5):
    return buscar_marcas_similares(model, marca_textos, marca_embeddings, input_marca, top_n)
