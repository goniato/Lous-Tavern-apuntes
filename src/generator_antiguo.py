import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime
import os

class GeneradorApuntes:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'))
        
    def cargar_datos(self, archivo_json):
        with open(archivo_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generar_pdf(self, datos, nombre_salida):
        # lectura de estilos.css
        with open('templates/estilos.css', 'r', encoding='utf-8') as f:
            css_content = f.read()

        # Renderizar portada
        template_portada = self.env.get_template('portada.html')
        logo_path = os.path.abspath('static/images/logo_empresa.jpg')
        html_portada = template_portada.render({
        'titulo': datos['titulo'],
        'css_content': css_content,
        'logo_path': logo_path,
        'estudiante': datos.get('estudiante_nombre', 'Estudiante'),
        'fecha_creacion': datetime.now().strftime('%d/%m/%Y'),
        'year': datetime.now().year
        })

        # Generar PDFs
        HTML(string=html_portada).write_pdf(f"output/{nombre_salida}_portada.pdf")
        
        # Renderizar secciones
        secciones_html = []
        template_seccion = self.env.get_template('seccion.html')

        for seccion in datos['secciones']:
            secciones_html.append(template_seccion.render({
                'css_content': css_content,
                'seccion': {
                    'titulo': seccion.get('titulo', 'Sección sin título'),
                    'nivel': seccion.get('nivel', 2),  # Por defecto h2
                    'contenido': seccion.get('contenido', [])
                },
                'year': datetime.now().year
            }))

        # Usar base.html para el contenido de las secciones
        template_base = self.env.get_template('base.html')
        html_secciones = template_base.render({
            'css_content': css_content,
            'contenido_123': '\n'.join(secciones_html)
        })
        HTML(string=html_secciones).write_pdf(f"output/{nombre_salida}_secciones.pdf")    
        
        # Combinar PDFs (opcional)
        self.combinar_pdfs(nombre_salida)

        os.remove(f"output/{nombre_salida}_secciones.pdf")
        os.remove(f"output/{nombre_salida}_portada.pdf")

        print(f"PDF generado exitosamente: output/{nombre_salida}_apuntes.pdf")
    
    def combinar_pdfs(self, nombre_base):
        from PyPDF2 import PdfMerger
        # Combinar los PDFs generados
        merger = PdfMerger()
        merger.append(f"output/{nombre_base}_portada.pdf")
        merger.append(f"output/{nombre_base}_secciones.pdf")
        merger.write(f"output/{nombre_base}_apuntes.pdf")
        merger.close()

# Ejemplo de uso
generador = GeneradorApuntes()
datos = generador.cargar_datos('data/apuntes.json')
generador.generar_pdf(datos, "esquiar")