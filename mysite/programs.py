import requests

catalogo ='CAT-002'

local = 'http://127.0.0.1:8000'
cloud = 'https://faesvx.herokuapp.com'

host = local

# URL del API REST que quieres consumir
url = host + '/api/api-token-auth/'
url_items_by_catalogo = host + '/api/listitemsbycatalog/'
url_catalogos = host + '/api/listcatalog'
url_receptor = host + '/api/receptor'
url_emisor = host + '/api/emisor'
url_departamentos = host + '/api/listdepartamentos'
url_municipios_by_departamento = host + '/api/listmunicipiosbydepartamento/'

url_categoriaseco = host + '/api/listcategoriaseconomicas'
url_subcategoriasecobycat = host + '/api/listsubcategoriaseconomicasbycategoria/'
url_actividadesecobysub = host + '/api/listactividadesconomicasbysubcategoria/'
url_tributos = host + '/api/listtributos'
# Credenciales de usuario

username = 'facturador'
password = 'facturador123'

# Datos de solicitud en formato JSON
data = {
    'username': username,
    'password': password
}

# Realizamos una solicitud POST a la URL con los datos de autenticación
response = requests.post(url, data=data)

# Verificamos si la solicitud fue exitosa
if response.status_code == 200:
    # Si la solicitud fue exitosa, mostramos el token de autenticación
    print('Token:', response.json()['token'])
    tok = response.json()['token']

    headers = {
        "Authorization": f"Token "+ tok
    }
    print(headers)
    print('==========================================================================================')
    print('=======================INVOCANDO API======================================================')
    print(url_catalogos)
    print('==========================================================================================')
    response = requests.get(url_catalogos,headers= headers)
    print(response.json())

    for data in response.json():
        url_ = url_items_by_catalogo + data["codigo"]
        print(str(data["id"]) + ' '+ data["codigo"] + ' ' + data["descripcion"] + ' '+ url_)
        print('==========================================================================================')
        print('=======================INVOCANDO API======================================================')
        print(url_)
        print('==========================================================================================')
        ro = requests.get(url_,headers= headers)

        for item in ro.json():
            print(str(item["id"]) +' '+  item["codigo"] +' '+ item["descripcion"])

    url_ = url_departamentos
    print('==========================================================================================')
    print('=======================INVOCANDO API======================================================')
    print(url_)
    print('==========================================================================================')
    ro = requests.get(url_, headers=headers)

    for item in ro.json():
        print(str(item["id"]) + ' ' + item["codigo"] + ' ' + item["descripcion"])

    url_ = url_municipios_by_departamento
    print('==========================================================================================')
    print('=======================INVOCANDO API======================================================')
    print(url_)
    print('==========================================================================================')
    ro = requests.get(url_ + "1", headers=headers)

    for item in ro.json():
        print(str(item["id"]) + ' ' + item["codigo"] + ' ' + item["descripcion"])


    url_ = url_categoriaseco
    print('==========================================================================================')
    print('=======================INVOCANDO API =====================================================')
    print(url_)
    print('==========================================================================================')
    ro = requests.get(url_, headers=headers)
    for item in ro.json():
        print(str(item["id"]) + ' ' + item["descripcion"])

    url_ = url_subcategoriasecobycat
    print('==========================================================================================')
    print('=======================INVOCANDO API =====================================================')
    print(url_)
    print('==========================================================================================')
    ro = requests.get(url_ + "10", headers=headers)
    for item in ro.json():
        print(str(item["id"]) + ' ' + item["descripcion"])

    url_ = url_actividadesecobysub
    print('==========================================================================================')
    print('=======================INVOCANDO API =====================================================')
    print(url_)
    print('==========================================================================================')
    ro = requests.get(url_ + "10", headers=headers)
    for item in ro.json():
        print(str(item["id"]) + ' ' + item["descripcion"])

    url_ = url_tributos
    print('==========================================================================================')
    print('=======================INVOCANDO API =====================================================')
    print(url_)
    print('==========================================================================================')
    ro = requests.get(url_, headers=headers)
    for item in ro.json():
        print(str(item["id"]) + ' ' + item["descripcion"])
        print(ro.json())

    url_ = url_emisor
    print('==========================================================================================')
    print('=======================INVOCANDO API ENVÍO EMISOR=========================================')
    print(url_)
    print('==========================================================================================')
    data = {
        'nit': '9999-999999-999-9',
        'nrc': '999999-9',
        'dui': '99999999-9',
        'actividadeco': '161',
        'nombre': 'AMC EL SALVADOR',
        'nombrecomercial': 'AMC',
        'tipoestablecimiento': '38',
        'municipio': '110',
        'complementodir': 'C.C. GALERIAS ESCALON LOC.101',
        'telefono': '2211-3553',
        'celular': '7777-7777',
        'email': 'esc14@amc.com.sv',
        'codestable': '1845',
        'codpuntoventamh': '0223',
        'codpuntoventa': '0133',
    }

    response = requests.post(url_, headers= headers,json=data)


    if response.status_code == 201:
        print('El emisor se ha creado exitosamente.')
        print(response.text)
    else:
        print(response.text)
        print('Hubo un error al crear el emisor.')

    url_ = url_receptor
    print('==========================================================================================')
    print('=======================INVOCANDO API ENVÍO RECEPTOR=========================================')
    print(url_)
    print('==========================================================================================')
    data = {
        'tipodocumento': '132',
        'nodocumento': '06142710151050',
        'nrc': '245431-3',
        'nombre': 'IMPORTADORA MOGA, S.A DE C.V',
        'actividadeco': '412',
        'municipio': '110',
        'complementodir': 'CALLE LOS ABETOS, APTO 11 B COL SAN FRANCISCO COND. REESIDENCIAL LOS ABETOS',
        'telefono': '2222-2222',
        'celular': '7777-7777',
        'email': 'importadoramoga@gmail.com',
    }

    response = requests.post(url_, headers= headers,json=data)

    if response.status_code == 201:
        print('El receptor se ha creado exitosamente.')
        print(response.text)
    else:
        print(response.text)
        print('Hubo un error al crear el receptor.')




else:
    print(response.text)
    print('Error al consumir el API REST. Código de estado:', response.status_code)
