import json
import boto3
from botocore.exceptions import ClientError

# Crear un objeto DynamoDB usando el SDK de AWS
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

# Seleccionar nuestra tabla DynamoDB
table = dynamodb.Table('studentData')

# Definir la función handler que el servicio Lambda usará como punto de entrada
def lambda_handler(event, context):
    # Extraer valores del objeto event que recibimos del servicio Lambda
    student_id = event.get('studentid')
    name = event.get('name')
    student_class = event.get('class')
    age = event.get('age')

    # Validar que todos los campos requeridos están presentes
    if not student_id or not name or not student_class or not age:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Faltan datos del estudiante.')
        }

    # Escribir los datos del estudiante en la tabla DynamoDB
    try:
        response = table.put_item(
            Item={
                'studentid': student_id,
                'name': name,
                'class': student_class,
                'age': age
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('¡Datos del estudiante guardados exitosamente!')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al guardar los datos del estudiante: {e.response["Error"]["Message"]}')
        }