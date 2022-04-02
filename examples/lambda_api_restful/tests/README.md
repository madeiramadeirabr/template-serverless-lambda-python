# Tests
Descrição da estrutura da pasta e conceitos

## Testes de unidade
* Testes que se utiliza de mocks para evitar conexões reais a componetes externos;
* Testes focados na funcionalidade e não nos dados em si;
* Testes para serem executados em pipelines de CI;
* A duração destes testes devem ser de no máximo 1s por arquivo, sendo o ideal rodar em milisegundos;

## Testes de integração
* Testes que não devem executar fixtures ou alterações de recursos para evitar problemas;
* Testes focados na integração de componentes externos com a aplicação em questão;
* Testes para serem executados em pipelines de CD;
* A duração destes vai depender dos cenários desenvolvidos, porém recomendado criar testes objetivos para não demorar muito o pipeline;

## Testes de componentes
* Testes bases para o processo de TDD;
* Testes focados no comportamento, cenários e dados dos processo do projeto;
* Testes para serem executados localmente em conjunto do docker que irá prover o acesso local a recursos como banco de dados e afins;
* A duração destes vai depender dos cenários desenvolvidos, mas a ideia destes testes é explorar diversos cenários possíveis;

## Referências 
* https://martinfowler.com/articles/microservice-testing/