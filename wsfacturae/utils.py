import psycopg2
from num2words import num2words
import json, random, string, uuid, inflect
from translate import Translator
from django.core.mail import EmailMultiAlternatives, get_connection
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
from decouple import config


def generateJson():
    conexion_params = {
        "dbname": "micobroxdb",
        "user": "postgres",
        "password": "root",
        "host": "localhost",
        "port": "5432",
    }
    try:
        conn = psycopg2.connect(**conexion_params)
        cursor = conn.cursor()
        print("conexion establecida")
    except psycopg2.Error as e:
        print("error al conectar con la base de datos")

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
    data = []
    for row in cursor.fetchall():
        factura_id, fecha, codigo, producto, cantidad, monto = row
        factura_encontrada = None
        for factura in data:
            if factura["id"] == factura_id:
                factura_encontrada = factura
                break

        if factura_encontrada:
            detalle = {
                "producto": producto,
                "cantidad": cantidad,
                "monto": str(monto),
            }
            factura_encontrada["detalle"].append(detalle)
        else:
            factura = {
                "id": factura_id,
                "fecha": fecha.strftime("%Y-%m-%d"),
                "codigo": codigo,
                "detalle": [
                    {
                        "producto": producto,
                        "cantidad": cantidad,
                        "monto": str(monto),
                    }
                ],
            }
            data.append(factura)
    conn.close()
    print(data)
    with open("datos_facturas.json", "w") as json_file:
        json.dump(data, json_file, indent=2)
    print("Datos exportados a 'datos_facturas.json' en formato JSON correctamente.")

def prepareMail(subject, to_email, from_email, pdf_content, json_content, smtp_config):

    msg = EmailMultiAlternatives(subject, "Estimado cliente, se adjunta el documento electrónico tributario en formato pdf y json.", from_email, to=[to_email])
    msg.attach('factura.pdf', pdf_content, 'application/pdf')
    msg.attach('archivo_json.json', json_content, "application/json")
    
    connection = get_connection(
        host=smtp_config.host,
        port=smtp_config.port,
        username=smtp_config.username,
        password=smtp_config.password,
        use_tls=smtp_config.use_tls
    )
    msg.connection = connection
    return msg

def prepareSMS(to_tel, mensaje):
   if to_tel and to_tel != "":
       cel = to_tel.replace('-', '')
       send_sms(mensaje, cel)

def send_sms(mensaje, to_tel):
    if config('TWILIO_ACTIVATE'):
        try:
            account_sid = config('TWILIO_ACCOUNT_SID')
            auth_token = config('TWILIO_AUTH_TOKEN')
            from_tel = config('TWILIO_FROM_TEL')
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                body=mensaje,
                from_=from_tel,
                to=to_tel
            )
            #print(message.sid)
        except TwilioRestException as e:
            print("SMS a "+ to_tel +" no pudo entregarse")
def generate_random_code(length=8):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code

def generate_uuidv4():
    return str(uuid.uuid4()).upper()

def numero_a_letras(numero):
    # Verificar si es un número decimal
    if "." in str(numero):
        parte_entera, parte_decimal = str(numero).split(".")
        parte_decimal = int(parte_decimal)
        
        if parte_decimal == 0:
            numero_entero_en_letras = num2words(int(parte_entera), lang='es')
            numero_en_letras = numero_entero_en_letras
        else:
            numero_entero_en_letras = num2words(int(parte_entera), lang='es')
            numero_decimal_en_letras = num2words(parte_decimal, lang='es')
            numero_en_letras = f"{numero_entero_en_letras} punto {numero_decimal_en_letras}"
    else:
        numero_en_letras = num2words(numero, lang='es')
    
    return numero_en_letras

def quitar_guiones(cadena):
    # Reemplaza todos los guiones por una cadena vacía
    cadena_sin_guiones = cadena.replace("-", "")
    return cadena_sin_guiones



