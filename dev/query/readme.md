
#Ainda não tenho muita experiência em ruby ... , mas considerando as opções em unix, deve ser mais fácil usar ruby do que c++ ou java.

Instalar as gems 'nokogiri' e 'levenshtein-ffi' e rodar o programa. 
O programa recebe como entrada uma palavra, que sera buscada no google, depois retorna o número de vezes em que a palavra foi encontrada nos títulos do resultado da busca, considerando distância de Levenshtein <= 2.
ex:
	#ruby query.rb
	#teste

Programa testado com a seguinte configuração:
versão ruby:
	2.0.0.p0 
versão gems:
	levenshtein-ffi (1.0.3)
	nokogiri (1.5.9)

