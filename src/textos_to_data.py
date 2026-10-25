from openai import OpenAI
import os
import json
from config import OPENAI_API_KEY

import PyPDF2


client = OpenAI(api_key=OPENAI_API_KEY)

def leer_documento(ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        return archivo.read()
    
prompt = leer_documento("textos/prompt.txt")

def leer_documento_pdf_1(ruta_archivo):
    with open(ruta_archivo, "rb") as archivo:
        lector = PyPDF2.PdfReader(archivo)
        texto = ""
        for pagina in lector.pages:
            texto += pagina.extract_text()
        return texto


def leer_documento_pdf_2(ruta_archivo):
    pass

#para pdf que no son legibles, sino que son imagenes o escaneados, se puede usar:

#Google Cloud Vision API (OCR para PDF escaneados).
#Adobe PDF Extract API (potente pero de pago).
#PDF.co (API en línea con plan gratuito).
#Tesseract OCR (instalación local, gratuito y de código abierto).



#def texto_json_resumen(texto):
#    respuesta = client.chat.completions.create(
#        model="gpt-4o-mini-2024-07-18",  # Usa el modelo GPT-4
#        messages=[
#            {"role": "system","content": "Eres un asistente académico especializado en crear resúmenes estructurados de temarios. Tu tarea es procesar el material de estudio proporcionado y generar un resumen, extenso, preciso y organizado en formato JSON con la siguiente estructura exacta:    1. Estructura básica: - `titulo`: Título principal del temario - `estudiante_nombre`: Nombre del estudiante (usar 'Estudiante' por defecto) - `secciones`: Array de objetos con la estructura de secciones.                2. Estructura de secciones: Cada sección debe tener:  - `titulo`: Título de la sección  - `nivel`: Número del 2 al 6  - `contenido`: Array que puede contener:* Objetos de tipo 'texto' con:- `texto`: Contenido textual que puede incluir ecuaciones LaTeX entre $$ (ej: $$E=mc^2$$)  * Objetos de tipo 'codigo' con: - `codigo`: Fragmento de código (identado correctamente) - `descripcion`: Explicación breve (opcional) *Objetos de tipo `columnas` con un array en su interior, que contiene dos o tres objetos de tipo texto (dos o tres columnas).  * Objetos de tipo 'subseccion' para anidamiento.     Instrucciones específicas: Mantén siempre la estructura JSON exacta del ejemplo proporcionado. Las ecuaciones matemáticas deben escribirse en LaTeX dentro del texto normal, entre símbolos $$ .Usa niveles de encabezado (2-6) para establecer jerarquía visual. Para código: conserva la indentación y añade descripción cuando sea relevante. Divide el contenido en secciones lógicas con buena progresión didáctica. Los ejemplos de código deben ser prácticos y relevantes. Explica conceptos complejos con claridad en los textos. Estructura de la salida esperada :{\"titulo\": \"titulo del temario tratado\",\"estudiante_nombre\": \"nombre del estudiante\",\"secciones\": [{\"titulo\": \"titulo de la seccion\",\"nivel\": 2,\"contenido\": [{\"tipo\": \"texto\",\"texto\": \"informacion seccion. Ejemplo de ecuacion: $$ E = mc^2 $$ \"},{\"tipo\": \"subseccion\",\"titulo\": \"titulo de subseccion\",\"nivel\": 3,\"contenido\": [{\"tipo\": \"texto\",\"texto\": \"informacion subseccion\"},{\"tipo\": \"codigo\",\"codigo\": \"codigo en el lenguaje que se explique\",\"descripcion\": \"descripcion del codigo, si fuese necesaria\"}]}]},{\"titulo\": \"titulo de la seccion\",\"nivel\": 2,\"contenido\": [{\"tipo\": \"texto\",\"texto\": \"texto de la seccion\"},{\"tipo\": \"texto\",\"texto\": \"informacion de la seccion \"},{\"tipo\": \"subseccion\",\"titulo\": \"titulo de subseccion\",\"nivel\": 3,\"contenido\": [ {\"tipo\": \"codigo\",\"codigo\": \"codigo escrito en lenguaje requerido\",\"descripcion\": \"descripcion del codigo si fuese necesaria\"}]}]]}"},
##            {"role": "user","content": texto}

#        ]
#    )
#    return respuesta.choices[0].message.content



def texto_json_resumen(texto):
    respuesta = client.chat.completions.create(
        model="gpt-4.1-mini",  
        messages=[
            {"role": "system","content": prompt},
            {"role": "user","content": texto}

        ]
    )
    return respuesta.choices[0].message.content



#ERROR CON LAS DESCRIPCIONES
