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