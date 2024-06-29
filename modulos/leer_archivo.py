import json
from pathlib import Path

class Lectura_archivo:
    @classmethod # método abstracto
    def lee_archivo(cls, ruta): #Función silenciosa
        cls.path = Path(ruta)
        try:
            cls.usuarios = cls.path.read_text(encoding='utf-8')
        
        except FileExistsError:
            pass
        return cls.usuarios