from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Configuración principal de la API
app = FastAPI(
    title="Gestor de Inventario API",
    description="API para gestionar un catálogo de productos",
    version="1.0.0"
)

# Modelo de datos usando Pydantic para validación
class Producto(BaseModel):
    id: Optional[int] = None
    nombre: str
    categoria: str
    precio: float
    stock: int
    fecha_registro: Optional[datetime] = None

# Base de datos simulada (en memoria)
inventario = [
    Producto(id=1, nombre="Taza Blanca 11oz", categoria="Sublimación", precio=15.0, stock=50, fecha_registro=datetime.now()),
    Producto(id=2, nombre="Pack de Regalo Personalizado", categoria="Packs", precio=45.0, stock=10, fecha_registro=datetime.now()),
    Producto(id=3, nombre="Taza Mágica Negra", categoria="Sublimación", precio=25.0, stock=30, fecha_registro=datetime.now())
]

@app.get("/", tags=["Inicio"])
def ruta_principal():
    return {"mensaje": "Bienvenido al Sistema de Inventario", "estado": "Activo"}

# --- OPERACIONES CRUD ---

@app.get("/productos", response_model=List[Producto], tags=["Productos"])
def obtener_todos_los_productos():
    """Devuelve la lista completa de productos."""
    return inventario

@app.get("/productos/{producto_id}", response_model=Producto, tags=["Productos"])
def obtener_producto_por_id(producto_id: int):
    """Busca un producto específico por su ID."""
    for prod in inventario:
        if prod.id == producto_id:
            return prod
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.post("/productos", response_model=Producto, tags=["Productos"])
def crear_nuevo_producto(producto: Producto):
    """Agrega un nuevo producto al inventario."""
    nuevo_id = max([p.id for p in inventario]) + 1 if inventario else 1
    producto.id = nuevo_id
    producto.fecha_registro = datetime.now()
    inventario.append(producto)
    return producto

@app.put("/productos/{producto_id}", response_model=Producto, tags=["Productos"])
def actualizar_producto(producto_id: int, producto_actualizado: Producto):
    """Actualiza los datos de un producto existente."""
    for index, prod in enumerate(inventario):
        if prod.id == producto_id:
            producto_actualizado.id = producto_id
            producto_actualizado.fecha_registro = prod.fecha_registro
            inventario[index] = producto_actualizado
            return producto_actualizado
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.delete("/productos/{producto_id}", tags=["Productos"])
def eliminar_producto(producto_id: int):
    """Elimina un producto del inventario."""
    for index, prod in enumerate(inventario):
        if prod.id == producto_id:
            inventario.pop(index)
            return {"mensaje": f"Producto con ID {producto_id} eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")