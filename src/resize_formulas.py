import os
from PIL import Image , ImageFilter , ImageOps
import uuid






def resize_formula(input_path, output_path = "static/formulas/redimension", scale_factor=0.3):
    try:
        
        
        #if os.path.exists(output_path):
            #return output_path  # Si ya existe, devolver la ruta existente
        # Abrir imagen original
        img = Image.open(input_path)
        
        # Calcular nuevo tamaño
        width, height = img.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        if img.mode != 'RGBA' and os.path.splitext(input_path)[1].lower() == '.png':
            img = img.convert('RGBA')

        img = img.convert('L')
            
            # 2. Aplicar umbralización (binarización)
        img = img.point(lambda x: 0 if x < 200 else 255)
            
            # 3. Redimensionar con algoritmo especial para texto
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # 4. Aplicar sharpening para mejorar nitidez
        resized_img = resized_img.filter(ImageFilter.SHARPEN)

        #resized_img = ImageOps.invert(resized_img)
        #resized_img = resized_img.point(lambda x: 0 if x < 50 else 255)
        #resized_img = ImageOps.invert(resized_img)
        original_filename = os.path.basename(input_path)
        name, ext = os.path.splitext(original_filename)
        new_filename = f"{name}_red{ext}"
        full_output_path = os.path.join(output_path, new_filename)
        extension = ext.lower()

        if extension == '.png':
            # Para PNG, usar compresión máxima pero sin pérdida
            resized_img.save(full_output_path, 'PNG', optimize=True, compress_level=9)
        else:
            # Para JPEG, usar calidad máxima y subsampling 0 (4:4:4)
            if resized_img.mode == 'RGBA':
                resized_img = resized_img.convert('RGB')
            resized_img.save(full_output_path, 'JPEG', quality=100, subsampling=0)

    except Exception as e:
        raise RuntimeError(f"Error procesando {input_path}: {str(e)}")
    

if __name__ == '__main__':
    # Ejemplo básico
    input_image = "static/images/logo_empresa.jpg"
    resize_formula(input_image, "static/images")
#    print(f"Imagen redimensionada guardada en: {resized_path}")