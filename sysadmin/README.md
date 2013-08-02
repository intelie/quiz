# Desafios de operação e serviços

Escolha um dos desafios abaixo e envie a solução para o e-mail `trabalhe@intelie.com.br` especificando no assunto a vaga e o desafio escolhido.

## Desafio 1:
* crie na sua máquina uma VM do VirtualBox com sistema operacional CentOS
* use o [módulo do puppet que gerencia o MySQL](https://github.com/puppetlabs/puppetlabs-mysql) para:
  * instalar e rodar o MySQL server na sua VM
  * configurar um usuário de backup (com senha)
  * ativar uma rotina de backup diário às 01:00AM de todas as bases do MySQL
* envie por e-mail as evidências de que tudo foi realizado com sucesso

## Desafio 2:
* crie na sua máquina uma VM do VirtualBox com sistema operacional CentOS 
* use o [módulo do puppet que gerencia o ActiveMQ](https://github.com/intelie/puppetlabs-activemq) para:
  * instalar e rodar o ActiveMQ na sua VM
  * configurar o ActiveMQ para ativar a interface de administração web
  * configurar o ActiveMQ para receber dados via conector STOMP
* faça um shell script na sua máquina que envie, usando o [stomp_sender](https://github.com/intelie/stomp_sender), uma mensagem via STOMP para o ActiveMQ rodando na VM 
* visualize a mensagem na interface de administração web
* envie por email as evidências de que tudo foi realizado com sucesso

## Desafio 3:
* você tem 3 servidores no Rackspace:
  * servidor A possui IP 10.34.0.1 e está na sub-rede 10.34.0.0/16
  * servidor B possui IP 10.34.0.2 e está na sub-rede 10.34.0.0/16
  * servidor C possui IP 10.35.0.3 e está na sub-rede 10.35.0.0/16
  * os 3 servidores se pingam
  * o traceroute de A para C mostra:

```
    traceroute to 10.35.0.3 (10.35.0.3), 30 hops max, 40 byte packets
    1  10.34.64.1  (10.34.64.1)   1.847 ms  1.630 ms  1.642 ms
    2  10.35.2.104 (10.35.2.104)  0.992 ms  1.002 ms  1.094 ms
    3  10.35.0.3   (10.35.0.3)    1.267 ms  1.273 ms  1.323 ms
```

* o servidor C é o único que tem instalado um cliente VPN para acessar uma rede externa de um cliente da Intelie
* os sistemas da Intelie rodam nos servidores A e B, que precisam receber tráfego HTTP vindo da rede externa do cliente (encapsulado na VPN)
* responda: é possível adicionar uma rota nos servidores A e B apontando o servidor C como gateway para a rede externa do cliente?
* proponha duas possíveis soluções para que os servidores A e B recebam o tráfego HTTP (e, claro, a resposta chegue de volta ao cliente)
* discuta as vantagens e desvantagens de cada solução levando em consideração aspectos práticos como estabilidade da solução e facilidade de configuração/manutenção.

## Desafio 4:
* Leia rapidamente a documentação da [linguagem de processamento de eventos EPL](http://esper.codehaus.org/esper-4.9.0/doc/reference/en-US/html_single/index.html)
* Responda: para que servem as propriedades dinâmicas de um evento da linguagem EPL?
* Cite um exemplo de caso de uso.
