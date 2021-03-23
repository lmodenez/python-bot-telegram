# StarTeleBot
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python 3.9](https://img.shields.io/badge/python-_>=_3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

Bot para o telegram focado em disponibilizar recursos aos representantes da Starplast.

## Motivação

Esse projeto foi criado como forma de alavancar o conhecimento do time de T.I na linguagem python.

## Desenvolvimento

Para iniciar o desenvolvimento, é necessário clonar o projeto do GitHub num diretório de sua preferência:

```shell
cd "diretorio de sua preferencia"
git clone https://github.com/starplast/startelebot.git
```

Após a clonagem do projeto se recomenda a criação de um virual enviroment a fim de isolar as dependências do projeto:

```shell
cd "diretorio do projeto"
python -m venv venv
```
> Para ativar o enviroment basta acessar via bash o  diretório ``"diretoriodoprojeto/venv/Scripts"`` e executar o arquivo ``activate``. 

Após a criação do ambiente se faz necessária a instalação do projeto em modo de edição, com isso as dependências serão automaticamente intaladas.  
Para isso ative o seu virtual enviroment e execute:

```shell
cd "diretorio do projeto"
pip install -e .[dev]
```
Para que seja possível a utilização do projeto em um bot de testes basta criar um arquivo chamado .secrets.toml com o token do seu bot.  
>Um arquivo de exemplo é disponibilizado com o nome [exemple.secrets.toml](./exemple.secrets.toml).

Se for necessário trocar o enviroment para algo além de ``development`` é necessário passar o env desejado através da váriável de sistema ``STARTELEBOT_ENV``.  
Há 2 formas simples de fazer isso:  
1. Criar o arquivo ``.env`` com o conteúdo ``STARTELEBOT_ENV = "aqui_vai_o_enviroment_(ex:PRODUCTION)"``.  
2. Exportar a variável de ambiente através do comando ``export STARTELEBOT_ENV=AQUI_VAI_O_ENVIROMENT`` para Linux, ou  ``set STARTELEBOT_ENV=AQUI_VAI_O_ENVIROMENT`` para Windows.
