from fastapi import HTTPException

from database import Categoria
from schemas.sch_categorias import CategoriaCrear, CategoriaUpdate


async def create_categoria(categoria_request: CategoriaCrear):

    if Categoria.select().where(Categoria.nombre == categoria_request.nombre).exists():
        raise HTTPException(status_code=400, detail="La categoria ya existe")

    categoria_request = Categoria.create(
        nombre = categoria_request.nombre,
        identificador= categoria_request.identificador
    )
    return {"mensaje": "Categoria creada exitosamente"}

async def get_all_incomes():
    categorias_ingresos  = []

    for category in Categoria.select().where(Categoria.identificador == "ing"):
        try:
            category_dict = {      
                "nombre": category.nombre,
            }
            categorias_ingresos.append(category_dict)

        except Categoria.DoesNotExist:
            raise HTTPException(status_code=404, detail="No existen categorias de ingresos")
    return categorias_ingresos


async def get_all_expenses():
    categorias_egresos  = []

    for category in Categoria.select().where(Categoria.identificador == "egr"):
        try:
            category_dict = {
                "nombre": category.nombre,
            }
            categorias_egresos.append(category_dict)

        except Categoria.DoesNotExist:
            raise HTTPException(status_code=404, detail="No existen categorias de egresos")
    return categorias_egresos

async def consult_categoria_income():
    categorias_ingresos  = []

    for category in Categoria.select().where(Categoria.identificador == "ing"):
        try:
            category_dict = {
                "id": category.id,
                "nombre": category.nombre,
                "identificador": category.identificador,
            }
            categorias_ingresos.append(category_dict)

        except Categoria.DoesNotExist:
            raise HTTPException(status_code=404, detail="No existen categorias de ingresos")
    return categorias_ingresos

async def consult_categoria_expenses():
    categorias_egresos  = []

    for category in Categoria.select().where(Categoria.identificador == "egr"):
        try:
            category_dict = {
                "id": category.id,
                "nombre": category.nombre,
                "identificador": category.identificador,
            }
            categorias_egresos.append(category_dict)

        except Categoria.DoesNotExist:
            raise HTTPException(status_code=404, detail="No existen categorias de egresos")
    return categorias_egresos

async def update_categoria(categoria_nombre, categoria_tipo,categoria_request: CategoriaUpdate):
    category = Categoria.select().where((Categoria.nombre == categoria_nombre) & (Categoria.identificador == categoria_tipo)).first()

    if category:
        category.nombre = categoria_request.nombre
        category.identificador = categoria_request.identificador
        category.save()
        return True
    else:
        return HTTPException(status_code=404, detail='Category not found')
