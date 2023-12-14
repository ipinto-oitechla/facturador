import psycopg2
import json

#Cambiar parametros dependiendo de la DB
conexion_params={
    'dbname':'micobroxdb',
    'user':'postgres',
    'password':'root',
    'host':'localhost',
    'port':'5432'
}
try:
    conn = psycopg2.connect(**conexion_params)
    cursor = conn.cursor()
    print("conexion establecida")
except psycopg2.Error as e:
    print("error al conectar con la base de datos")
#Query para seleccionar tablas
query = """SELECT
                      f.id AS factura_id,
                      f.fecha,
                      f.codigo,
                      df.producto,
                      df.cantidad,
                      df.monto
                  FROM
                      restser_factura f
                  LEFT JOIN
                      restser_detallefactura df
                  ON
                      f.id = df.fk_factura_id"""

cursor.execute(query)
data=[]
#Ordenar la data en una lista
for row in cursor.fetchall():
            factura_id, fecha, codigo, producto, cantidad, monto = row
            factura_encontrada = None
            for factura in data:
                if factura['id'] == factura_id:
                    factura_encontrada = factura
                    break

            if factura_encontrada:
                detalle = {
                    'producto': producto,
                    'cantidad': cantidad,
                    'monto': str(monto),
                }
                factura_encontrada['detalle'].append(detalle)
            else:
                factura = {
                    'id': factura_id,
                    'fecha': fecha.strftime('%Y-%m-%d'),
                    'codigo': codigo,
                    'detalle': [{
                        'producto': producto,
                        'cantidad': cantidad,
                        'monto': str(monto),
                    }]
                }
                data.append(factura)
conn.close()
print(data)
#Crear un documento 'datos_facturas.json' y guardar la información de las facturas dentro (el json corresponde a las tablas restser no a las de wsfacturae)
with open('datos_facturas.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)
print("Datos exportados a 'datos_facturas.json' en formato JSON correctamente.")


