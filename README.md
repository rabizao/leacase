# API CRUD de controle de estoque

Esta aplicação foi desenvolvida utilizando Python com o Framework [Flask](https://flask.palletsprojects.com). Para conexão com o banco de dados, utilizei o ORM [SQLALchemy](https://www.sqlalchemy.org/), que facilita a escrita de *queries* e portabilidade para diferentes tipos de banco de dados, já que as *queries* são escritas utilizando sintaxe Python, e a "tradução" para linguagem de banco de dados é realizada pelo SQLALchemy. Com isso, podemos plugar diversos bancos de dados sem precisar alterar o código da aplicação. Por padrão, para facilitar testes e desenvolvimento, utilizei o SQLite, que persiste os dados no disco e não precisa de nenhuma configuração específica no sistema para rodar a aplicação. Para alterar para um banco de dados mais robusto em produção, o arquivo [config.py](backend/config.py) já prevê uma variável de ambiente no formato do SQLAlchemy para realizar a conexão com outros bancos chamada DATABASE_URL.

Essa aplicação já está pronta para rodar como um serviço *serverless* em qualquer provedor de serviços em nuvem. Recomendo a utilização do serviço ***Cloud Run*** da ***Google Cloud Platform***, que é capaz de escalar a aplicação em momentos de pico e inclusive diminuir o número de instâncias para 0 quando não estivar sendo utilizada (acarretando custo também 0 nesses períodos). Trata-se de uma excelente alternativa tanto em escalabilidade, facilidade de implementação e custo. Para mais informações sobre o ***Cloud Run*** e um tutorial de como subir esse tipo de aplicação lá, deixo um [post](https://www.rafaelbizao.com/deploy-api-serverless-escalavel-utilizando-google-cloud-run) que publiquei recentemente em minha página pessoal. Ao final desse documento, também adicionei os comandos necessários para colocar essa aplicação no ar utilizando o ***Cloud Run***.

## Principais features

- Criar clientes, discos e pedidos
- Listar discos, filtrando por estilo, ano de lançamento, artista e nome
- Listar pedidos por cliente e período
- Já preparado para controle de estoque em picos de acesso, tratando *race conditions* adequadamente e impossibilitando a venda de mais discos do que os disponíveis em estoque

## Execução

**Pré-requisitos:**

- [Docker](https://www.docker.com/)

**Executar aplicação**

Navegue até a pasta *backend* e crie o container utilizando:

```sh
docker build -t leacase .
```

Para rodar o container em modo interativo na porta 5000, utilize:

```sh
docker run -e PORT=5000 -p 5000:5000 leacase
```

Pronto! Acesse a documentação (com possibilidade de realizar chamadas através do próprio navegador) em [http://localhost:5000/](http://localhost:5000/)

## Desenvolvimento

**Pré-requisitos:**

- Python 3.8+ com ferramentas de desenvolvimento

Para instalar em um sistema operacional baseado em Debian, utilize:

```sh
sudo apt install python3.8-venv python3.8-dev python3.8-distutils
```

Para preparar o ambiente de desenvolvimento, utilize:

```sh
git clone https://github.com/rabizao/leacase
cd leacase/
python3.8 -m venv venv
source venv/bin/activate
cd backend/
pip install -r requirements.txt
flask db upgrade
```

**Executar aplicação**

```sh
source venv/bin/activate
cd backend/
python3.8 start.py
```

**Executar testes unitários e de stress**

```sh
source venv/bin/activate
cd backend/
python3.8 tests.py
```

## Deploy na *Google Cloud Platform (GCP)*

Para subir o serviço na GCP, é necessário ter a [CLI gcloud](https://cloud.google.com/sdk/docs/install) instalada e autenticada e rodar os seguintes comandos na pasta backend:

```sh
gcloud builds submit --tag=gcr.io/project/leacase
gcloud run deploy leacase --image=gcr.io/project/leacase
```

em que project é o nome do seu projeto na GCP. Vale lembrar que o serviço será *serverless* e os dados não podem ser persistidos em disco. Por isso, é necessário também uma instância de banco de dados externa com a conexão já configurada através da variável de ambiente DATABASE_URL.
