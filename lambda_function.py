import json
import boto3
import os
from jinja2 import Environment, FileSystemLoader

def lambda_handler(event, context):
    
    # Extrai os dados do evento da API Gateway
    data = json.loads(event['body'])
    
    # Carrega os dados de um arquivo local (json)
    # with open('./dados.json', 'r') as file:
    #     data = json.load(file) 
    
    # Carrega o template localizado no S3
    s3_bucket_name = os.environ.get('s3_bucket_name')
    s3_template_file = os.environ.get('s3_template_file')
    s3 = boto3.resource("s3")
    obj = s3.Object(s3_bucket_name, s3_template_file)
    template_content = obj.get()["Body"].read().decode("utf-8")

    # Carrega ambiente com loader FileSystemLoader
    load_env = Environment(loader=FileSystemLoader('.'))

    # Obtem o conteúdo do template 
    template = load_env.from_string(template_content)

    # Renderiza o template com os dados do JSON
    rendered_template = template.render(data)

    # Envia e-mail utilizando o AWS SES
    subject = data["subject"]
    mail_sender = os.environ.get('mail_sender')
    mail_receive = data["mail_receive"]
    charset = "UTF-8"

    ses_client = boto3.client("ses")
    try:
        response = ses_client.send_email(
            Source=mail_sender,
            Destination={"ToAddresses": [mail_receive]},
            Message={
                "Subject": {"Data": subject, "Charset": charset},
                "Body": {"Html": {"Data": rendered_template, "Charset": charset}},
            },
        )
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "Erro ao enviar o e-mail: " + str(e),
        }

    # Retornar a resposta em um formato adequado para a API Gateway
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "E-mail enviado com sucesso!",
    }