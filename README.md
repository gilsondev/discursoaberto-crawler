# Discurso Aberto Crawler

Projeto de raspagem de dados dos discursos dos deputados disponibilizados no site da Camara dos Deputados.

**Licença:** MIT

## Requisitos Minimos

 - Python 2.7, 3,4 ou 3.5
 - MongoDB

## Instalação

1 - Faça o checkout do projeto

```bash
git clone https://github.com/gilsondev/discursoaberto-crawler.git discursoaberto_crawler
```

2 - Crie o ambiente virtual

```bash
cd discursoaberto_crawler
virtualenv venv
```

3 - Ative o ambiente e instale as dependências

```bash
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
```

4 - Inicie a execução do spider `discurso` para raspar os discursos e salvar no banco de dados:

```bash
(venv)$ scrapy crawl discurso
```

Caso queria passar valores diferentes para a pesquisa de discursos, use o parametro `-a`:

 - `data_inicial`: Data de inicio para compor periodo de tempo na pesquisa
 - `data_final`: Data final para compor periodo de tempo na pesquisa

```bash
(venv)$ scrapy crawl discurso -a data_inicio="01/05/2016" -a data_final="01/05/2016"
```
