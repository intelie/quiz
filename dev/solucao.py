#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor:...: Claudio Polegato Junior
# E-mail...: junior@juniorpolegato.com.br
# Data.....: 14/Nov/2012
# Arquivo..: solucao.py
# Versão...: 0.1
# Descrição: Faz pesquisa de um termo utilizando o Google e retorna
#            quantos termos foram encontrados em cada título resultante,
#            sendo que no final totaliza os termos encontrados
# Execução.: Num teminal, tendo o Python 2.7 instalado, posiconado no
#            mesmo diretório desde arquivo, execute:
#            python solucao.py <termo de pesquisa>

import httplib
import cStringIO
import gzip
import zlib
import sys
import urllib
import re
import unicodedata

def print_matriz(m):
    ('Dada uma matriz de inteiros, na forma de vetor linhas, e cada'
     ' linha na forma de vetor de valores, imprime a mesma')
    # Maior número de dígitos dentre os valores da matriz
    max_digitos = len(str(max([max(l) for l in m])))
    # Formato para suportar e imprimir de forma alinhada
    formato = '%%%ii' % max_digitos
    # Imprimir abertura da matriz de forma alinhada
    print '--' + ' ' * ((max_digitos + 1) * len(l) - 3) + '--'
    # Imprimir valores da matriz de forma alinhada
    for i in m:
        print '|' + ' '.join([formato % j for j in i]) + '|'
    # Imprimir fechamento da matriz de forma alinhada
    print '--' + ' ' * ((max_digitos + 1) * len(l) - 3) + '--'

def levenshtein(s1, s2, mostrar_matriz = False):
    ('Dadas duas strings, a distância de Levenshtein é o somatório de'
     ' quantas inserções, remoções ou substituições são necessárias'
     ' para uma string ficar igual à outra')
    # Se forem iguais a distância é 0
    if s1 == s2:
        return 0
    # Tamanhos
    t1 = len(s1)
    t2 = len(s2)
    # Se tamanho de s1 for zero, retorna o tamanho de s2
    # No caso de que se os tamanhos de ambas forem zero, retorna zero
    if t1 == 0:
        return t2
    # Se o tamanho de s2 for zero, retorna o tamanho de s1
    if t2 == 0:
        return t1

    # Matriz baseada em http://upload.wikimedia.org/math/8/7/1/
    #                               871cba439a7684b64d12d692e96d1e83.png
    # Encontra-se em http://en.wikipedia.org/wiki/Levenshtein_distance

    # A primeira linha deve ter suas colunas com valores 0 a t2
    # A primeira coluna deve ter suas linhas com valores 0 a t1
    # A primeira linha já foi incluída acima, então deve-se adicionar
    # linhas de 1 a t1
    # Os outros valores são ignorados, mas precisam ser alocados
    m = [range(t2 + 1)] + [[i] * (t2 + 1) for i in range(1, t1 + 1)]

    # Na matriz, cada célula na linha i e coluna j, sendo i>0 e j>0,
    # é calculada como sendo o valor mínimo entre os valores da celulas:
    # - acima mais 1 => deletar
    # - à esquerda mais 1 => inserir
    # - acima e à esquerda mais o custo de substituição => substituir
    # O custo de substituição é 1 se o caracter na posição i-1 de s1 for
    # diferente do caracter na posição j-1 de s2, senão o custo é zero
    for i in range(1, t1 + 1):             # linhas de 1 a t1
        for j in range(1, t2 + 1):         # colunas de 1 a t2
            c = s1[i-1] != s2[j-1]         # custo
            m[i][j] = min(m[i-1][j]   + 1, # Deletar
                          m[i][j-1]   + 1, # Inserir
                          m[i-1][j-1] + c) # Substituir
    if mostrar_matriz:
        print_matriz(m)
    return m[t1][t2]

# Header para identificar melhor a requisição de páginas se passando por
# Firefox 10.0.10
header = {
    'User-Agent': ('Mozilla/5.0 (X11; Linux i686; rv:10.0.10)'
                   ' Gecko/20100101 Firefox/10.0.10'),
    'Accept': ('text/html,application/xhtml+xml,application/xml;'
               'q=0.9,*/*;q=0.8'),
    'Accept-Language': 'pt-br,pt;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}

def descomprimir(dados, encoding):
    ('Retorna a descompressão de dados em gzip ou deflate, senão'
     ' retorna os dados tal como passados')
    if encoding == 'gzip':
        io = cStringIO.StringIO(dados)
        g = gzip.GzipFile(fileobj = io, mode = 'rb')
        ungziped = g.read()
        g.close()
        return ungziped
    if encoding == 'deflate':
        return zlib.decompress(dados)
    return dados

def obter_pagina(url):
    'Retorna o conteúdo de uma url inciada com http:// ou https://'
    # Separar protocolo e endereço na url
    if '://' not in url:
        print 'Protocolo não identificado!'
        return None
    protocolo, endereco = url.split('://', 1)
    protocolo = protocolo.lower()
    # Aceitar apenas protocolos http e https
    if protocolo not in ('http', 'https'):
        print 'Apenas aceitos os protocolos http e https!'
        return None
    # Separar servidor e uri no endereço
    if '/' in endereco:
        servidor_porta, uri = endereco.split('/', 1)
    else:
        servidor_porta = endereco
        uri = ''
    # Separar servidor e porta no servidor_porta
    if ':' in servidor_porta:
        serivdor, porta = servidor_porta.split(':')
    else:
        servidor = servidor_porta
        porta = 80 if protocolo == 'http' else 443
    # Conectar ao servidor
    if protocolo == 'https':
        con = httplib.HTTPSConnection(servidor, porta)
    else:
        con = httplib.HTTPConnection(servidor, porta)
    # Enviar o pedido para obeter a uri, método GET
    con.request('GET',  '/' + uri, None, header)
    # Ler resposta
    resp = con.getresponse()
    # Redirecionamento
    if 299 < resp.status < 400 and resp.getheader('location'):
        return obter_pagina(resp.getheader('location'))
    # Leitura e descompressão dos dados
    dados = descomprimir(resp.read(), resp.getheader(
                                                    'content-encoding'))
    # Passar para unicode
    charset = 'UTF-8'
    for c in resp.getheader('content-type').split(';'):
        if '=' in c:
            x, y = c.strip().split('=', 1)
            if x.lower() == 'charset':
                charset = y
                break
    dados = dados.decode(charset)
    # Fechar conexão
    con.close()
    # Se não retornou com status 200, mostra os detalhes
    if resp.status != 200:
        print '-' * 100
        print resp.status, resp.reason
        headers = resp.getheaders()
        for h, c in headers:
            print '%s: %s' % (h, c)
        print re.sub('<[^>]+>', ' ', dados)
        print '-' * 100
    # Retornar os dados lidos
    return dados

def filtrar_titulos_pesquisa_google(html):
    ('Assume que cada título no resultado da pesquisa no Google'
     ' esteja na forma: <h3 class="r"><a href="...>título</a>\n'
     'Então retorna a lista de tíltulos encontrados.')
    ts = re.findall('<h3 class="r"><a href="[^>]*>.*?(?:</a>)', html)
    ts = [re.sub('<[^>]*>', '', t) for t in ts]
    return ts

def contar_frases(frase, texto, distancia_levenshtein):
    ('Conta as frases encontradas em texto com distância de Levenshtein'
     ' máxima passada')
    contador = 0
    l_frase = len(frase)
    l_texto = len(texto)
    i = 0
    # Verificar no texto desde o primeiro até o útlimo caracter cuja
    # posição ainda possibilite estar dentro da distancia_levenshtein
    while i < l_texto - l_frase + distancia_levenshtein:
        # Verificar as possíveis palavras que estejam dentro da
        # distancia_levenshtein a partir da posição i em texto
        distancias = []
        for l in range(i + l_frase - distancia_levenshtein,
                       i + l_frase + distancia_levenshtein + 1):
            distancias.append(levenshtein(frase, texto[i:l]))
        if min(distancias) <= distancia_levenshtein:
            i += l_frase
            contador += 1
        else:
            i += 1
    return contador

def normalize(string, encoding = 'UTF-8'):
    'Normaliza uma string em determinado encoding para ASCII'
    if type(string) != unicode:
        string = string.decode(encoding)
    string = string.replace(u'Æ', u'AE').replace(u'æ', u'ae').\
                                replace(u'ª', u'a.').replace(u'º', u'.')
    return unicodedata.normalize('NFKD', string).encode('ascii',
                                                               'ignore')

def pesquisa_google_completa(string_procura, mostrar_detalhes = True):
    'Retorna a união de todas as páginas que da pesquisa no Google'
    if type(string_procura) == unicode:
        string_procura = string_procura.encode('utf-8')
    procura = urllib.quote_plus(string_procura)
    paginas = ['0']
    completa = ''
    contador = 0
    if mostrar_detalhes:
        print ('    Contando `%s´ nos títulos encontrados,'
               ' normalizados e com distância de'
               ' Levenshtein 2...') % pesquisa
        print '    Formato: <encontrados> em `<título>´'
    for pagina in paginas:
        print 'Lendo página %3i de % 3i...' % (paginas.index(pagina) +
                                                        1, len(paginas))
        resultado = obter_pagina('http://www.google.com/search?q=' +
                                           procura + '&start=' + pagina)
        novas = re.findall('start=([0-9]+)&', resultado)
        for nova in novas:
            if nova not in paginas:
                paginas.append(nova)
        titulos = filtrar_titulos_pesquisa_google(resultado)
        contador2 = 0
        for titulo in titulos:
            # Utiliza pesquisa e titulos normalizados para contagem
            encontrados = contar_frases(pesquisa_normalizada,
                                           normalize(titulo).lower(), 2)
            if mostrar_detalhes:
                print '    %3i em `%s´' % (encontrados,
                                                 titulo.encode('utf-8'))
            contador2 += encontrados
        contador += contador2
        print "Total encontrado até o momento:", contador
    return contador

if __name__ == '__main__':
    if len(sys.argv) > 1:
        pesquisa = ' '.join(sys.argv[1:])
    else:
        print 'Uso:', sys.argv[0], '<termo de pesquisa>'
        sys.exit(1)
    print 'Pequisando `%s´ via Google...' % pesquisa
    # Normaliza a pesquisa para melhorar os resultados
    pesquisa_normalizada = normalize(pesquisa).lower()
    contador = pesquisa_google_completa(pesquisa_normalizada)
    print 'Total encontrado:', contador
