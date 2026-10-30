import os
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db import obtener_conexion

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

class BusquedaRequest(BaseModel):
    texto: str

@router.post("/tienda/busqueda-ia")
def buscar_con_ia(req: BusquedaRequest, conexion=Depends(obtener_conexion)):
    prompt_sistema = (
        "Eres un asistente de una tienda de empaques. El usuario describirá lo que necesita. "
        "Tu tarea es devolver SOLO una palabra clave o categoría técnica para buscar en la base de datos "
        "(ejemplos de categorías: 'empaque', 'etiquetado', 'proteccion'). No agregues texto adicional."
    )
    
    try:
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": req.texto}
            ],
            max_tokens=10,
            timeout=5.0
        )
        
        palabra_clave = respuesta.choices[0].message.content.strip()
        
        productos = conexion.execute(
            "SELECT nombre, precio, codigo FROM producto WHERE nombre LIKE ? OR categoria_id IN (SELECT id FROM categoria WHERE nombre LIKE ?)",
            (f"%{palabra_clave}%", f"%{palabra_clave}%")
        ).fetchall()
        
        return {
            "metodo": "IA",
            "palabra_clave_usada": palabra_clave,
            "productos": [dict(p) for p in productos]
        }

    except Exception as e:
        print(f"Fallo la IA ({e}). Activando fallback.")
        

        palabras = req.texto.split()
        termino_busqueda = f"%{palabras[0]}%" if palabras else "%"
        
        productos = conexion.execute(
            "SELECT nombre, precio, codigo FROM producto WHERE nombre LIKE ?",
            (termino_busqueda,)
        ).fetchall()
        
        return {
            "metodo": "Fallback (Búsqueda tradicional)",
            "palabra_clave_usada": termino_busqueda,
            "productos": [dict(p) for p in productos]
        }