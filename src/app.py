import os
import re
import time
import pandas as pd
from transformers import pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "..", "data", "raw", "reviews.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "data", "processed", "reviews_with_sentiment.csv")
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"



def parse_sentiment(result):
    """
    Convierte la salida del modelo en estrellas (1 a 5) y banda de negocio:
    - 1-2 estrellas -> Negativo
    - 3 estrellas   -> Neutral
    - 4-5 estrellas -> Positivo
    """
    label = result["label"]
    stars = int(re.search(r"\d+", label).group())

    if stars in [1, 2]:
        band = "Negativo"
    elif stars == 3:
        band = "Neutral"
    else:
        band = "Positivo"
    
    return stars, band, round(result["score"], 4)

def main():
    print("=" * 60)
    print("🚀 Iniciando Pipeline de Producción - WeLoveReviews")
    print("=" * 60)

    # 1. carga de datos
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {INPUT_PATH}")
    
    print(f"Cargando dataset desde {INPUT_PATH}")
    df = pd.read_csv(INPUT_PATH)
    print(f"Total de registros a procesar: {len(df)}")

    # 2 normalización básica
    df["review_text"] = df["review_text"].astype(str).str.strip()

    # 3 carga única del modelo en memoria
    print(f"Cargando modelo fijado: '{MODEL_NAME}'...")
    classifier = pipeline("sentiment-analysis", model=MODEL_NAME)
    print("Modelo instanciado en memoria.")

    # 4 Inferencia por lotes
    print("\n Ejecutando inferencia por lotes...")
    start_time = time.time()
    texts = df["review_text"].tolist()
    raw_results = classifier(texts, batch_size=32, truncation=True)

    # 5 Mapeo de predicciones
    parsed = [parse_sentiment(r) for r in raw_results]
    df["pred_stars"] = [p[0] for p in parsed]
    df["pred_sentiment"] = [p[1] for p in parsed]
    df["pred_score"] = [p[2] for p in parsed]

    elapsed = time.time() - start_time
    print(f"Inferencia completada en {elapsed:.2f} s ({elapsed / len(df) * 1000:.1f} ms/reseña).")

    # 6 exportar salida a csv
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\n💾 Archivo enriquecido exportado exitosamente a:\n   {OUTPUT_PATH}")

    # 7 resumen de resultado
    print("\n📊 Resumen de distribución generada:")
    dist = df["pred_sentiment"].value_counts(normalize=True) * 100
    for band in ["Positivo", "Neutral", "Negativo"]:
        count = (df["pred_sentiment"] == band).sum()
        pct = dist.get(band, 0.0)
        print(f"   - {band:8s}: {count:3d} reseñas ({pct:5.1f}%)")

    print("\n🏁 Pipeline finalizado con éxito.")

if __name__ == "__main__":
    main()