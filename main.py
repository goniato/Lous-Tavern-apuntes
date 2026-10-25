from src.generator import GeneradorApuntes
from src.textos_to_data import texto_json_resumen , leer_documento , leer_documento_pdf_1
import json
import re



tema = "Primo_de_rivera"
nombre_archivo = f"{tema}.pdf"
ruta_archivo = f"documentos/{nombre_archivo}"
texto = leer_documento_pdf_1(ruta_archivo)
respuesta_txt = texto_json_resumen(texto)
print("RESPUESTA AI RECIBIDA")
with open('textos/respuesta.txt', 'w' , encoding="utf-8") as f:
    f.write(respuesta_txt)
    print(f"Respuesta guardada en data/respuesta.txt")


match = re.search(r'\{.*\}', respuesta_txt, re.DOTALL)

if match:
    datos_json = json.loads(match.group(0))

    with open('data/apuntes.json', 'w') as f:
        json.dump(datos_json, f, indent=4)
        print(f"JSON guardado en data/apuntes.json")
else:
    print("No se encontró un JSON válido en el texto.")


generador = GeneradorApuntes()
datos = generador.cargar_datos('data/apuntes.json')
generador.generar_pdf(datos, tema)