from fastapi import FastAPI, Body, HTTPException
from sqlalchemy import inspect, text
from src.config.db import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#FUNCION PARA TRAER LAS TABLAS | PARA "Área de Selección de Tablas y Campos"
@app.get("/tablas")
def obtener_tablas():
    try:
        inspector = inspect(engine)
        tablas = {}
        # Iterar sobre cada tabla de la base de datos para obtener su nombre y tipo de dato
        for table_name in inspector.get_table_names():
            columns = [
                {"nombre": column["name"], "tipo": str(column["type"])}
                for column in inspector.get_columns(table_name)
            ]
            # Detectar claves foráneas
            foreign_keys = [
                {
                    "column": fk["constrained_columns"],
                    "referenced_table": fk["referred_table"],
                    "referenced_column": fk["referred_columns"]
                }
                for fk in inspector.get_foreign_keys(table_name)
            ]
            tablas[table_name] = {"campos": columns, "foreign_keys": foreign_keys}

        return {"tablas": tablas}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la información de la base de datos: {str(e)}")
    
 #FUNCION PARA OBTENER LAS FOREIGN KEYS/ LLAVES FORANEAS   
def get_foreign_keys_for_table(inspector, table, direction="outgoing"):
    foreign_keys = []
    if direction == "outgoing":
        # Get outgoing foreign keys
        for fk in inspector.get_foreign_keys(table):
            foreign_keys.append({
                "column": fk["constrained_columns"][0],
                "referenced_table": fk["referred_table"],
                "referenced_column": fk["referred_columns"][0]
            })
    else:
        # Get incoming foreign keys
        for other_table in inspector.get_table_names():
            if other_table != table:
                for fk in inspector.get_foreign_keys(other_table):
                    if fk["referred_table"] == table:
                        foreign_keys.append({
                            "column": fk["constrained_columns"][0],
                            "table": other_table,
                            "referenced_column": fk["referred_columns"][0]
                        })
    return foreign_keys

#FUNCION PARA OBTENER DATOS PARA "Área de Visualización de Datos" CON SUS RESPECTIVAS RELACIONES DE LAS TABLAS
@app.post("/data")
def obtener_datos_seleccionados(
    table: str = Body(...),
    selected_fields: list[str] = Body(...),  # Campos seleccionados
):
    with engine.connect() as connection:
        inspector = inspect(engine)
        
        try:
            # Obtener claves foráneas con la funcion de arriba
            outgoing_foreign_keys = get_foreign_keys_for_table(inspector, table, "outgoing")
            incoming_foreign_keys = get_foreign_keys_for_table(inspector, table, "incoming")

            #Esto soluciona el error de "ambiguous column name" en consultas con JOIN para las tablas de empresa por el parecido de nombre en emp unidas
            prefixed_fields = [] 
            for field in selected_fields:
                if "empresa" in table and "." not in field:
                    prefixed_fields.append(f"{table}.{field}")
                else:
                    prefixed_fields.append(field)
            fields = ", ".join(prefixed_fields)
            
            # Construir la y ejecutar consulta SQL 
            query = f"SELECT DISTINCT {fields} FROM {table}"
            for fk in outgoing_foreign_keys:
                query += f" LEFT JOIN {fk['referenced_table']} ON {table}.{fk['column']} = {fk['referenced_table']}.{fk['referenced_column']}"
            for fk in incoming_foreign_keys:
                query += f" LEFT JOIN {fk['table']} ON {fk['table']}.{fk['column']} = {table}.{fk['referenced_column']}"
            result = connection.execute(text(query))
            data = [dict(row._mapping) for row in result]
            
            return {"data": data}

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al obtener los datos: {str(e)}")    

