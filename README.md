# Desafio Finxi

Desafio do processo seletivo Finxi

##Desafio Python

Desenvolva um sistema web de aluguel de imóveis simples. O sistema deve conter um front com a listagem de imóveis que podem ser alugados que, por sua vez, são cadastrados através de um CMS. Todos os inputs do CMS devem ser feitos utilizando forms. Não utilize o admin do Django.
Essa tela de listagem precisa possuir um campo de busca por endereço e sugerir imóveis que se encontrem nas proximidades do mesmo.
É obrigatório que todos os imóveis cadastrados no sistema possuam uma imagem relacionada ao mesmo e esta deve ser subida no S3 da AWS.

##Observações

Utilizei o S3 para o armazenamento da media mas não para o static. Poderia colocar os dois no mesmo bucket em pastas diferentes ou em outro bucket, mas como isso não foi solicitado optei pelo simples e só utilizei o S3 para os arquivos de media.

Utilizei a biblioteca [python-decouple](https://github.com/henriquebastos/python-decouple) para isolar as configurações do settings.py no arquivo [.env](https://github.com/diegorocha/desafio-finxi/blob/master/aluguel/.env), isso facilita o desenvolvimento em equipe, pois com o mesmo arquivo settings.py cada desenvolvedor pode ter as suas proprias configurações (banco, secret, etc).

Nesse modo o arquivo .env não deveria ser versionado (sendo incluido no .gitignore) e cada desenvolvedor cria e mantem o seu arquivo localmente, mas optei por versionar ele para facilitar a execução do desafio (basta clonar e executar, sem precisar criar o arquivo com as configurações).

Utilizei o [dj-database-url](https://github.com/kennethreitz/dj-database-url) para facilitar o decouple da configuração de banco. Uma vez que ele possibilita passar a configuração através de uma única string.

A integração Django x S3 foi feita com o [django-storages](https://github.com/jschneier/django-storages)

A geolocalização foi feita através da [api do google maps](https://developers.google.com/maps/documentation/geocoding/intro?hl=pt-br)

Para integrar o Django com o Google Maps eu utilizei as bibliotecas [requests](http://docs.python-requests.org/en/master/) e [simplejson](http://simplejson.readthedocs.org/en/latest/), para consultar os dados e fazer o parse, respectivamente.

Buscas com latitude e longitude são complicadas, pesquisei se havia algo pronto para o django, encontrei o [GeoDjango](https://docs.djangoproject.com/en/1.9/ref/contrib/gis/), mas para poder utilizar seria necessario configurar um banco de dados de latitude e longitude e a documentação não me ajudou muito. Seria necessário algum tempo para entender como ele funciona para utilizar corretamente. Como a intenção não é um sistema completo e sim um demonstração rápida, optei por utilizar uma abordagem matemática aproximada.

A abordagem matemática mais correta seria usar a [Fórmula de Haversine](https://pt.wikipedia.org/wiki/F%C3%B3rmula_de_Haversine) para testar a distancia de cada imóvel ao endereço de busca. Mas, além de complicado de implementar numa consulta do django, seria problematico quando o banco de dados ficasse cheio de imóveis. Pois seriam realizados várias contas para cada imóvel. 

Pela simplicidade resolvi usar uma aproximação:

A função get_min_max_coordenates calcula as latitudes e longitudes mínimas e máximas com n km de distancia (aproximada). Nesse caso n=1 km

Assim, eu filtro os imoveis cujas latitude e longitude fiquem dentro desse quadrado. É claro que essa lista pode retornar imoveis que estejam a mais de 1km de distância do endereço, afinal, geramos um quadrado ao invés de um circulo.

Como o conjunto de imóveis já foi reduzido, uma solução para isso seria filtrar os imóveis retornados pelo orm novamente, dessa vez sim testando a distância entre cada um e ponto através da formula, os imóveis com distância maior que o desejado seriam removidos do conjunto, restando apenas os dentro do circulo.