# Frontend

Esse serviço é responsável por interagir com o usuário para criar/organizar projetos e rotular imagens/textos.

O webapp é feito utilizando o framework React.

## Requerimentos

- NodeJS
- npm
  
## Setup

### WebApp

Primeiro instale as dependências do serviço:

`$ npm install`

E para executar o serviço em modo de desenvolvimento:

`$ npm start`

## Deploy

Utilizamos o CLI da IBM Cloud para dar deploy do WebApp. Com ele, utilizamos o buildpack Static File do Cloud Foudry para armazenar os arquivos estáticos da versão de build.

Primeiramente, compile a versão de produção do webapp

`npm run build-prd`

Mova o arquivo Staticfile para a pasta de build:

`cp Staticfile build`

Após isso, se já estiver com o `ibmcloud` configurado, apenas de `push` da pasta root do projeto.

`ibmcloud cf push`

As configurações de deploy estão no arquivo `manifest.yml`.

## Guia de estilo

Todas as modificações devem estar de acordo com o [Style Guide](https://github.com/airbnb/javascript/tree/master/react) da Airbnb
