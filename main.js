
var request = require('request');
var cheerio = require('cheerio');
var distanciaLevenshtein = require('levenshtein');
var googleapis = require('googleapis');

var APIKEY = 'AIzaSyA1VgFZ1dG7DLAMjdwRHlyd_wsOoNgLVms';
var CX = '005902665988631214965:9rgui3wxquo'
var frequencia=0;
var frequenciaGlobal=0;

var args = process.argv.slice(2);
var palavraBuscada = args[0];


frequenciaTitulosAPIGoogle(palavraBuscada);

function frequenciaTitulos(palavraBuscada){

	palavraBuscada = palavraBuscada.toLowerCase();
	var paginaVisitada = "https://www.google.com.br/search?q="+palavraBuscada;
	console.log("\n\nVisitando a página " + paginaVisitada+"\n\n");

	request(paginaVisitada,function(error, response, body){

			var $ = cheerio.load(body);

			$(".r").each(function(){
				frequencia=0;
				
				var titulo = $(this).text();
				console.log(titulo+"\n");
				var palavras = titulo.toLowerCase().split(" ");

				for(i=0; i<palavras.length; i++){
					if(distanciaLevenshtein(palavras[i], palavraBuscada)<=2){
						frequencia++;
					}
				}
				console.log("Palavras encontradas nesse Título: "+frequencia+"\n\n");
				frequenciaGlobal += frequencia;
	    		
	     	});
	     	console.log("Total de vezes que a palavra "+palavraBuscada+" apareceu na página: "+ frequenciaGlobal);
		});
}
	
function frequenciaTitulosAPIGoogle(palavraBuscada){
	
	palavraBuscada = palavraBuscada.toLowerCase();
	var paginaVisitada = "https://www.googleapis.com/customsearch/v1?key="+APIKEY+"&cx="+CX+"&q="+palavraBuscada;
	console.log("\n\nVisitando a página " + paginaVisitada+"\n\n");

	request(paginaVisitada,function(error, response, body){
	var request = JSON.parse(body);
	request.items.forEach(function(item){
		frequencia=0;
		console.log(item.title+"\n");
		var palavras = item.title.toLowerCase().split(" ");
		for(i=0; i<palavras.length; i++){
			if(distanciaLevenshtein(palavras[i], palavraBuscada)<=2)
				frequencia++;
		}

		console.log("Palavras encontradas nesse Título: "+frequencia+"\n\n");
		frequenciaGlobal +=frequencia;
		});
	console.log("Total de vezes que a palavra "+palavraBuscada+" apareceu na página: "+ frequenciaGlobal);
	});
}


