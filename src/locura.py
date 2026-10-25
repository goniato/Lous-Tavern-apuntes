import ctypes
from ctypes.util import find_library

# Verifica si GTK está accesible
print(find_library("libgobject-2.0-0"))  # Debería devolver la ruta de la librería