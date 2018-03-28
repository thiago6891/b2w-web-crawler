# Web Crawler

## Arquitetura

A idéia da arquitetura pode ser melhor explicada por essa [figura](https://www.evernote.com/shard/s133/sh/76966c02-5e3e-4359-b1c5-1d73e692ef9a/26f43401c72d5448904941c2c3c27803).

Basicamente, N *crawlers* são configurados para acessar o site em questão e usam um BD central para guardar as informações necessárias.

As informações guardadas no BD são:

- URLs que já foram visitadas.
- URLs que foram encontradas, porém ainda precisam ser visitadas.
- URLs de páginas de produtos.
- Informações das páginas de produtos (utilizando a URL como chave de acesso).

Visto que o Redis possui *Hashes* e *Sets*, me pareceu uma escolha melhor ao invés de um banco relacional.

Um pequeno aplicativo web foi feito para acessar o banco, capturar as informações desejadas, e gerar o csv pedido.

Além disso, o aplicativo mostra algumas informações sobre o processo de *crawling*.

Para a comunicação entre as diferentes partes, Docker me pareceu uma boa escolha devido à simplicidade. (*Quem eu estou querendo enganar? Só fiz com Docker para ganhar o chocolate... gosto de 70% cacau, no mínimo. ;)* )

## Instruções de Instalação

É necessário o Docker versão 18.03.0-ce.

*Teoricamente, deve funcionar na versão 17.09 ou superior, mas não testei*.

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

## Questões Discursivas

***1 - Agora você tem de capturar dados de outros 100 sites. Quais seriam suas estratégias para escalar a aplicação?***

Acredito que a utilização do Docker já facilita essa escalação ao permitir a distribuição de vários crawlers em máquinas diferentes.

Um problema em potencial que consigo enxergar na arquitetura que utilizei é o BD centralizado que pode acabar sendo um gargalo.

Uma possível solução talvez seja utilizar vários BDs. Um para cada site que se deseja capturar dados.

***2 - Alguns sites carregam o preço através de JavaScript. Como faria para capturar esse valor?***

Teria que utilizar um browser para executar o código javascript e retornar o HTML renderizado para ser tratado no código.

Parece ser possível fazer isso com Python usando o módulo Selenium.

***3 - Alguns sites podem bloquear a captura por interpretar seus acessos como um ataque DDOS. Como lidaria com essa situação?***

Algumas possíveis soluções preventivas seriam:

- Respeitar as regras no arquivo *robots.txt* se estiver presente.
- Inserir períodos aleatórios de *sleep* entre *requests*.
- Usar diferentes IPs e *User-Agents* aleatoriamente.

Como será possível notar no código, não implementei nenhuma dessas prevenções devido à inexperiência com crawling. *(Tive que fazer uma breve pesquisa para conseguir responder essa pergunta.)*

***4 - Um cliente liga reclamando que está fazendo muitos acessos ao seu site e aumentando seus custos com infra. Como resolveria esse problema?***

Uma possível solução seria simplesmente diminuir a velocidade de ação do crawler, resultando em menos acessos.

Porém, dependendo de qual informação exatamente estamos tentando extrair, talvez hajam soluções bem melhores.
