import requests

catalogo = "CAT-002"

local = "http://127.0.0.1:8000"
cloud = "https://faesvx.herokuapp.com"

host = local

# URL del API REST que quieres consumir
url = host + "/api/api-token-auth/"
url_items_by_catalogo = host + "/api/listitemsbycatalog/"
url_catalogos = host + "/api/listcatalog"
url_receptor = host + "/api/receptor"
url_emisor = host + "/api/emisor"
url_departamentos = host + "/api/listdepartamentos"
url_municipios_by_departamento = host + "/api/listmunicipiosbydepartamento/"

url_categoriaseco = host + "/api/listcategoriaseconomicas"
url_subcategoriasecobycat = host + "/api/listsubcategoriaseconomicasbycategoria/"
url_actividadesecobysub = host + "/api/listactividadesconomicasbysubcategoria/"
url_tributos = host + "/api/listtributos"
url_factura = host + "/api/facturatest"
# Credenciales de usuario

username = "raraniva2"
password = "oitechla123$"

# Datos de solicitud en formato JSON
data = {"username": username, "password": password}

# Realizamos una solicitud POST a la URL con los datos de autenticación
response = requests.post(url, data=data)

# Verificamos si la solicitud fue exitosa
if response.status_code == 200:
    # Si la solicitud fue exitosa, mostramos el token de autenticación
    print("Token:", response.json()["token"])
    tok = response.json()["token"]

    headers = {"Authorization": f"Token " + tok}
    url_ = url_factura

    data = [
  {
    "id": 43,
    "fecha": "2023-07-25",
    "codigo": "F12345",
    "detalle": [
      {
        "producto": "Producto A",
        "cantidad": 2,
        "monto": "250.00000000"
      },
      {
        "producto": "Producto B",
        "cantidad": 10,
        "monto": "250.00000000"
      },
      {
        "producto": "Producto C",
        "cantidad": 10,
        "monto": "250.00000000"
      }
    ]
  },
    ]
    response = requests.post(url_, headers=headers, json=data)
    if response.status_code == 201:
        print("La factura se ha creado exitosamente.")
        print(response.text)
        
        print(response.text)
    else:
        print(response.status_code)
        if response.status_code == 500:
            error_message = response.text
            max_lines_to_display = (
                500  # Puedes ajustar este número según tus necesidades
            )

            for line in error_message.splitlines()[:max_lines_to_display]:
                print(line)
else:
    print(response.text)
    print("Error al consumir el API REST. Código de estado:", response.status_code)
