# b2w-web-crawler

Code challenge for B2W hiring process.

## Instruções de Instalação

É necessário o Docker versão 18.03.0-ce. 

Teoricamente, deve funcionar na versão 17.09 ou superior, mas não testei.

### Utilizando as Imagens do Docker Hub

1. Executar os seguintes comandos

        ~$ git clone https://github.com/thiago6891/b2w-web-crawler.git
        ~$ cd b2w-web-crawler/
        ~$ docker swarm init
        ~$ docker stack deploy -c docker-compose.yml b2w

    - Caso o comando ***docker swarm init*** apresente erro, será necessário executá-lo com a opção ***--advertise-addr*** de acordo com as instruções que irão aparecer no terminal.

2. Acessar ***localhost:8000*** para ver informações sobre páginas visitadas e gerar o arquivo csv com as informações de páginas de produtos encontradas até o momento.

### Fazendo o Build das Imagens Localmente

Caso seja desejado buildar as imagens localmente, os comandos a serem executados serão os seguintes:

1. Clonar o repositório:

        ~$ git clone https://github.com/thiago6891/b2w-web-crawler.git
        ~$ cd b2w-web-crawler/

2. Buildar as imagens necessárias:

        ~$ docker build -t b2w-web -f DockerfileWebApp .
        ~$ docker build -t b2w-crawler -f DockerfileCrawler .

3. Incializar o swarm e fazer o deploy do stack:

        ~$ docker swarm init
        ~$ docker stack deploy -c docker-compose-local.yml b2w

### Derrubando a Aplicação

- Para derrubar a aplicação, execute:

        ~$ docker stack rm b2w
        ~$ docker swarm leave --force

## Banco de Dados

Todas as informações coletadas pelo crawler são armazenadas com o Redis em um volume Docker com o nome *crawler-redis*.

Logo, caso a aplicação seja levantada posteriormente, o trabalho continuará de onde parou.

Caso haja interesse em reiniciar o processo de descoberta de páginas, basta deletar o BD com o comando:

    ~$ docker volume rm crawler-redis

## Testes

Para rodar os testes, vá até o diretório raiz do repositório e execute:

    ~$ python3 -m unittest