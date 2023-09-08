#Projeto de ETL

- Para iniciarmos esse projeto, usei a Estrutura abaixo:
- Cloud Functions
- Cloud Storage
- Big Query
Usei toda a estrutura do Google Cloud Platform (GCP)

![My Image](src/gcp_etl.png)

Os dados sao extraídos de algumas ferramentas de segurança, pois o objetivo é entender qual a quantidade e os tipos de vulnerabilidades são encontradas nas ferramentas de segurança. Assim, foram utilizadas as ferramentas:
- SCA (WhiteSource)
- SAST (Bandit e Snyk)
- DAST (OWASP ZAP)
Essas ferramentas foram coletas através dos repositórios do Github, Snyk e Gitlab conforme arquivos `project_id_gitlab`,`repository` e `project_id_snyk`

## Cloud Functions

Foram desenvolvidas duas cloud functions.
- A primeira para realizar toda a parte de extraçao das ferramentas de segurança para armazenar em arquivo json final. Antes disso, todos os arquivos gerados são enviados em formato csv para um bucket temporário e após isso, são concatenados e é gerado um json com arquivo final desses dados. Para a geraçao desse trigger, pode ser feito através de um request, onde será possível ter esse output:
![My Image](src/request.png)

- A segunda function foi usada com um trigger, onde se o arquivo json fosse enviado para o bucket, seria adicionada no Cloud Storage

Imagens:

### Functions
![My Image](src/functions_gcp.png)

### Extraçao de dados de segurança
![My Image](src/sec_functions.png)

### Bucket temporário
![My Image](src/bucket-temp.png)

### Upload do json
![My Image](src/log2.png)

### Carregamento do arquivo json
![My Image](src/json_function.png)

### Envio do json para Cloud Storage
![My Image](src/log1.png)

## Cloud Storage

Foi possível observar o upload e os dados armezados no banco de dados do GCP
![My Image](src/cloud-storage.png)

## Análise de dados usando Jupyter-lab
No próprio gcp, foi possível criar uma instância com jupyterlab
![My Image](src/jupyter-lab.png)

Observação sobre a ferramenta SAST obtém mais vulnerabilidades
![My Image](src/jupyter-lab-gcp.png)

Espero que tenham gostado 👩‍💻