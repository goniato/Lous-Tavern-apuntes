import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from datetime import datetime
import os
import requests
import re
from urllib.parse import quote
from resize_formulas import resize_formula 


def render_math_to_image(latex_code, output_dir="static/formulas/original"):
    """Renderiza fórmulas LaTeX a imágenes usando CodeCogs"""
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Nombre de archivo más robusto (usa hash MD5)
        codigo = f"{hash(latex_code)}"
        filename = f"{codigo}.png"  # Máscara para positivo
        filename_red = f"{codigo}_red.png"  # Máscara para negativo
        filepath = os.path.join(output_dir, filename)
        
        filepath_red= os.path.join("static/formulas/redimension" , filename_red)

        if not os.path.exists(filepath_red):
            encoded = quote(latex_code)
            url = f"https://latex.codecogs.com/png.latex?\\dpi{{500}} {encoded}"
            response = requests.get(url) #timeout=10
            #response.raise_for_status()
            
            with open(filepath, "wb") as f:
                f.write(response.content)

            resize_formula(filepath)
        
        return filepath_red
    
    except Exception as e:
        print(f"Error renderizando fórmula: {latex_code}\nError: {str(e)}")
        return None


def replace_math_with_images(html_content):
    """Reemplaza fórmulas LaTeX por imágenes en el HTML"""
    def replace_match(match):
        latex = match.group(1)
        img_path = render_math_to_image(latex)
        if img_path:
            return f'<img src="file:///{os.path.abspath(img_path)}" class="img-formula" alt="{latex}">'
        return match.group(0)  # Si falla, mantiene la fórmula original
    
    
    return re.sub(r'\$\$(.*?)\$\$', replace_match, html_content, flags=re.DOTALL)

def texto_negrita(html_content):
    """Reemplaza negritas en el HTML"""
    def replace_match(match):
        texto = match.group(1)
        return f'<span class="negrita">{texto}</span>'
    
    return re.sub(r'\*\*(.*?)\*\*', replace_match, html_content, flags=re.DOTALL)

class GeneradorApuntes:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'))
        
    def cargar_datos(self, archivo_json):
        with open(archivo_json, 'r', encoding='utf-8') as f:
            return json.load(f)
        
    
    def generar_pdf(self, datos, nombre_salida):
        # Cargar estilos CSS
        with open('templates/estilos.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        print("CSS cargado")
        # Renderizar portada
        template_portada = self.env.get_template('portada.html')
        logo_path = os.path.abspath('static/images/logo_empresa.png')
        html_portada = template_portada.render({
            'titulo': datos['titulo'].upper(),
            'css_content': css_content,
            'logo_path': logo_path,
            'estudiante': datos.get('estudiante_nombre', {}),
            'fecha_creacion': datos.get('fecha_creacion', datetime.now().strftime('%d/%m/%Y')),
            'year': datetime.now().year
        })
        print("Portada renderizada")
        # Generar PDFs
        HTML(string=html_portada).write_pdf(f"output/{nombre_salida}_portada.pdf")
        print("Portada PDF generada")

        # Renderizar secciones
        secciones_html = []
        template_seccion = self.env.get_template('seccion.html')

        for seccion in datos['secciones']:
            secciones_html.append(template_seccion.render({
                'css_content': css_content,
                'seccion': {
                    'titulo': seccion.get('titulo', 'Sección sin título'),
                    'nivel': seccion.get('nivel', 2),
                    'contenido': self._procesar_contenido(seccion.get('contenido', []))
                },
                'year': datetime.now().year
            }))

        print("Secciones renderizadas")

        template_base = self.env.get_template('base.html')
        html_secciones = template_base.render({
            'css_content': css_content,
            'contenido_123': texto_negrita(replace_math_with_images('\n'.join(secciones_html)))
        })
        print("HTML de secciones generado")
        #Resize de las imagenes

        #imagenes = [os.path.join("static/formulas/original", f) for f in os.listdir("static/formulas/original")]

        #for imagen in imagenes:
        #    resize_formula(imagen)

        HTML(string=html_secciones).write_pdf(f"output/{nombre_salida}_secciones.pdf",stylesheets=[CSS(string=css_content)])  ##cambio aqui##
        print("Secciones PDF generadas")

        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(html_secciones)


        # Combinar PDFs
        self.combinar_pdfs(nombre_salida)

        # Limpieza
        os.remove(f"output/{nombre_salida}_portada.pdf")
        os.remove(f"output/{nombre_salida}_secciones.pdf")

        print(f"PDF generado: output/{nombre_salida}_apuntes.pdf")



    def _procesar_contenido(self, contenido):
        processed = []
        for item in contenido:
            processed_item = {'tipo': item.get('tipo')}
            
            # Manejo para cada tipo de contenido
            if item.get('tipo') == 'texto' or item.get('tipo') == 'text':  # Compatible con ambos
                processed_item.update({
                    'texto': item.get('texto', '').replace('\n', '<br>')#.replace('**', ' <b> ')
                })

            elif item.get('tipo') == 'imagen':
                processed_item.update({
                    'ruta': item.get('ruta', ''),
                    'pie': item.get('pie', '')
                })
            
            elif item.get('tipo') == 'codigo':
                processed_item.update({
                    'codigo': item.get('codigo', ''),
                    'descripcion': item.get('descripcion', '')
                })
            
            elif item.get('tipo') == 'columnas' and True == False:  # Cambiar a True para habilitar
                columnas_procesadas = []
                for columna in item.get('columnas', []):
                    elementos_columna = []
                    for elemento in columna:
                        if elemento.get('tipo') in ['texto', 'text']:  # Compatible con ambos
                            elementos_columna.append({
                                'tipo': 'texto',
                                'texto': elemento.get('texto', '').replace('\n', '<br>').replace('\ n', '<br>')#.replace('**', ' <b> ')
                            })
                    columnas_procesadas.append(elementos_columna)
                processed_item['columnas'] = columnas_procesadas
            
            elif item.get('tipo') == 'columnas':
                columnas_procesadas = []
                for columna in item.get('columnas', []):
                    elementos_columna = []
                    for elemento in columna:
                        if elemento.get('tipo') in ['texto', 'text']:
                            elem = {
                                'tipo': 'texto',
                                'texto': elemento.get('texto', '').replace('\n', '<br>').replace('\ n', '<br>')#.replace('**', ' <b> ')
                            }
                            if 'titulo' in elemento:
                                elem['titulo'] = elemento['titulo']
                            elementos_columna.append(elem)
                    columnas_procesadas.append(elementos_columna)
                processed_item['columnas'] = columnas_procesadas
            
            elif item.get('tipo') == 'lista':
                processed_item.update({
                    'elementos': item.get('elementos', [])
                })
            
            elif item.get('tipo') == 'subseccion':
                processed_item.update({
                    'titulo': item.get('titulo', 'Subsección sin título'),
                    'nivel': item.get('nivel', 3),
                    'contenido': self._procesar_contenido(item.get('contenido', []))
                })
            
            # Asegurarse de que solo agregamos items con tipos conocidos
            if processed_item['tipo'] in ['texto', 'text', 'imagen', 'codigo', 'columnas', 'subseccion', 'lista']:
                processed.append(processed_item)
        print("Contenido procesado")
        return processed
    

    def combinar_pdfs(self, nombre_base):
        from PyPDF2 import PdfMerger
        merger = PdfMerger()
        merger.append(f"output/{nombre_base}_portada.pdf")
        merger.append(f"output/{nombre_base}_secciones.pdf")
        merger.write(f"output/{nombre_base}_apuntes.pdf")
        merger.close()
        print("PDFs combinados")