# Implementation Plan: Análisis de Sentimiento en Reseñas (WeLoveReviews)

Este documento detalla el plan de implementación guiado para resolver el reto de análisis de sentimiento con modelos NLP preentrenados, estructurado bajo las directrices pedagógicas y de calidad de **Code Refinement Suite**.

---

## 🎯 Resumen del Proyecto y Pregunta de Negocio

El cliente **WeLoveReviews** necesita comprobar si las 500 reseñas escritas de una empresa con puntuación media de **4.5 / 5 estrellas** reflejan en verdad ese optimismo, o si existen discrepancias ocultas en el texto.
El objetivo final es generar dos artefactos complementarios:
1. **Un Notebook narrativo y analítico (`src/explore.ipynb`)**: artefacto de comunicación completo para la account manager con EDA, justificación, inferencia, análisis de falsos negativos y conclusiones.
2. **Un Script de producción (`src/app.py`)**: canalización limpia y reproducible que genere `data/processed/reviews_with_sentiment.csv`.

---

## 🚦 Nivel de Complejidad y Estrategia

- **Clasificación:** **Nivel 2 (Complejidad Media)** con componentes de evaluación de dominio y separación exploratoria/producción.
- **Enfoque Pedagógico:** Guiado paso a paso por fases. La IA explica el fundamento teórico y la propuesta técnica en cada fase, y el usuario la aplica, valida sus salidas y confirma antes de avanzar a la siguiente.

---

## 🗺️ Mapa de Trabajo por Fases (Roadmap)

### Fase 1: Entorno y Dependencias
- [ ] Revisar el dataset base en `data/raw/reviews.csv` (formato, columnas, volumen).
- [ ] Fijar dependencias en `requirements.txt` (`transformers`, `torch`, `pandas`, `numpy`, `matplotlib`, `seaborn`).
- [ ] Instalar y verificar que el entorno reconozca PyTorch y Hugging Face Transformers sin conflictos.

### Fase 2: Encuadre Narrativo y EDA en el Notebook (`src/explore.ipynb`)
- [ ] Redactar la celda inicial de **Objetivos y Contexto de Negocio** (WeLoveReviews, 4.5 estrellas vs texto).
- [ ] Cargar los datos y realizar el Análisis Exploratorio de Datos (EDA):
  - Distribución de calificaciones por estrellas (`rating`).
  - Métricas de longitud de reseñas (palabras y caracteres).
  - Identificación de nulos, inconsistencias o textos anómalos.
- [ ] Propuesta y ejecución de limpieza de texto (manejo de espacios, formatos).
- [ ] Documentar *insights* preliminares con celdas Markdown transicionales.

### Fase 3: Selección y Justificación del Modelo NLP
- [ ] Documentar la justificación técnica del modelo elegido: `nlptown/bert-base-multilingual-uncased-sentiment`.
- [ ] Explicar en Markdown el **desajuste de dominio** (modelo entrenado en productos vs reseñas de servicios como restaurantes/cafés) y la hipótesis de falsos negativos.
- [ ] Formalizar la regla de mapeo:
  - 1 y 2 estrellas $\rightarrow$ **Negativo**
  - 3 estrellas $\rightarrow$ **Neutral**
  - 4 y 5 estrellas $\rightarrow$ **Positivo**
- [ ] Definir la arquitectura de carga: uso de `pipeline()` de Hugging Face cargado **una sola vez en memoria**.

### Fase 4: Inferencia y Comparativa con el Promedio de Negocio
- [ ] Implementar la función de inferencia por lotes o iteración optimizada en `src/explore.ipynb`.
- [ ] Extraer estrellas predichas y mapear a banda de sentimiento para las 500 reseñas.
- [ ] Calcular y visualizar la distribución porcentual (% positivo, % neutral, % negativo).
- [ ] Comparar formalmente la distribución contra el promedio reportado de 4.5 estrellas: ¿coinciden o difieren?

### Fase 5: Análisis Crítico de Falsos Negativos y Muestra Manual
- [ ] Filtrar y aislar discrepancias críticas: reseñas con 4–5 estrellas otorgadas por el cliente donde el modelo predijo 1–2 estrellas.
- [ ] Analizar los patrones lingüísticos (ironía, elogios a camareros, quejas menores sobre tiempos pero experiencia global positiva).
- [ ] Realizar una muestra de inspección manual detallada de 15 a 20 reseñas aleatorias y documentar observaciones cualitativas.
- [ ] Redactar las **Conclusiones de Negocio** orientadas a la account manager (takeaways claros y accionables).

### Fase 6: Industrialización a Producción (`src/app.py`)
- [ ] Estructurar `src/app.py` siguiendo buenas prácticas de software (funciones limpias, `main()`, sin dependencias interactivas).
- [ ] Cargar el dataset crudo, instanciar el pipeline fijado y ejecutar la inferencia de forma automatizada.
- [ ] Exportar el resultado final a `data/processed/reviews_with_sentiment.csv`.
- [ ] Verificar la integridad del archivo CSV resultante (500 filas, nuevas columnas presentes).

### Fase 7: Auditoría Final y Cierre (PACK 4)
- [ ] Comprobar que `src/explore.ipynb` esté guardado con todas las celdas y salidas ejecutadas.
- [ ] Comprobar que no se hayan subido pesos de modelos al repositorio.
- [ ] Verificar `requirements.txt` con versiones congeladas y reproducibles.
- [ ] Solicitar confirmación explícita antes de cualquier commit o push a Git.

---

## ⚙️ Métodos Aplicados (Code Refinement Suite)

1. **Abstracción y Step-Back Prompting (PACK 2):**
   Antes de escribir código de modelado, se separaron las preocupaciones en dos carriles: la *historia narrativa* y comunicación para el cliente (en el notebook) y la *ejecución reproducible* (en el script de producción).

2. **Mitigación de Sesgo y Falsos Positivos de Validación (Tree of Thoughts):**
   Se reconoció desde el inicio el desajuste de dominio (*domain mismatch*). En lugar de asumir ciegamente la salida del modelo como verdad absoluta, se diseñó una fase de análisis de falsos negativos y muestreo manual para auditar la calidad real de las predicciones frente a la puntuación humana.

3. **Verificación Fáctica (Chain of Verification - CoVe) (PACK 3):**
   Se valida que la carga de Hugging Face se realice mediante `pipeline('sentiment-analysis', model=...)` instanciada una sola vez para evitar sobrecarga de memoria o fugas en loops de inferencia sobre 500 registros.

4. **Auditoría Previa y Control de Git (PACK 4):**
   Se garantiza que los pesos pesados del modelo permanezcan en la caché local y no contaminen el control de versiones de Git, respetando la regla inviolable de solicitar confirmación antes de cualquier push al repositorio remoto.
