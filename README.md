# b2w-web-crawler
Code challenge for B2W hiring process.

#### Instruções

Docker precisa estar instalado, e o swarm inicializado.

    docker swarm init

Caso esse comando apresente erro será necessário executá-lo com a opção *--advertise-addr*:

    docker swarm init --advertise-addr <address>
    
E em seguida:

    git clone https://github.com/thiago6891/b2w-web-crawler.git
    cd b2w-web-crawler/
    docker stack deploy -c docker-compose.yml b2w-crawler

O crawler começará a trabalhar, e o arquivo .csv poderá ser baixado em localhost:8000
    
-----

No momento da entrega as imagens necessárias estarão no Docker Hub. Porém, caso necessite buildar as imagens do crawler e da aplicação web, os comandos são:

    docker build -t crawler-web-app web_app/
    docker build -t crawler crawler/