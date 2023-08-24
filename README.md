AWS Lambda Email Sender
Código função Lambda da AWS que envia e-mails usando o serviço Amazon Simple Email Service (SES). A função é acionada por eventos da API Gateway e utiliza um template HTML armazenado no Amazon S3 para criar o conteúdo do e-mail.

Pré-requisitos
Antes de começar, certifique-se de ter:

Uma conta AWS configurada com as permissões necessárias para criar funções Lambda, acessar o SES e o S3.
O ambiente de desenvolvimento configurado com as credenciais AWS corretas.

Configuração
Faça o upload do arquivo JSON de dados para o S3:

Certifique-se de ter um arquivo JSON de dados no formato correto. Faça o upload deste arquivo para um bucket no Amazon S3. Anote o nome do bucket e o caminho para o arquivo.

Configurar variáveis de ambiente:

Defina as seguintes variáveis de ambiente para a função Lambda:

s3_bucket_name: Nome do bucket no S3 onde o template está localizado.
s3_template_file: Caminho para o arquivo de template HTML no S3.
mail_sender: Endereço de e-mail remetente.

Configurar o template HTML:

Certifique-se de ter um arquivo HTML que servirá como o template para o corpo do e-mail. Faça upload deste arquivo para o bucket S3 especificado acima.

Uso
A função Lambda será acionada por eventos da API Gateway. Quando um evento for recebido, a função seguirá os seguintes passos:

Extrai os dados JSON do corpo do evento.
Carrega o template HTML do S3 e cria um ambiente Jinja2 para renderização.
Renderiza o template com os dados JSON.
Envia um e-mail usando o SES, usando o conteúdo renderizado como corpo do e-mail.
Em caso de erro durante o processo de envio do e-mail, um erro 500 será retornado com detalhes sobre o erro. Caso contrário, um status 200 será retornado indicando o sucesso no envio do e-mail.

Notas
Certifique-se de que a função Lambda tenha as permissões adequadas para acessar o S3 e enviar e-mails usando o SES.
