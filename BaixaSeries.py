import webbrowser
import requests
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime

now = datetime.now()

'''
lumendatabase.org/
http://webcache.googleusercontent.com/
'''

'''def inicio():
    os.open
'''


def magnetcerto(magnet, serie):
    padrao = ''
    pattern = re.compile(r'\s+')
    lista = pattern.split(serie)

    for i in range(len(lista)):
        if i != (len(lista)-1):
            padrao += lista[i] + '.*'

        else:
            padrao += lista[i]
    pattern = re.compile(padrao)
    lista2 = pattern.search(magnet)
    if lista2 is None:
        return False
    else:
        return True


def conferiSerie(magnet, serie, epi):

    if magnetcerto(magnet, serie) is True:
        pattern = re.compile(epi)
        if pattern.search(magnet) is not None:
            return True


def conferiFilme(magnet, filme):
    if magnetcerto(magnet, filme) is True:
        if re.search(r's\d+e\d+', magnet) is None:
            return True


def menu():
    escolha = 1
    while escolha != 0:
        print('\n\nMENU\n')
        print('1-Procurar serie')
        print('2-Procurar filme')
        print('3-Procurar qualquer coisa')
        print('4-Abrir MENU sobre urls confiaveis e nao confiaveis')
        print('5-Ver quando saiu episodios novos')
        print('0-Sair')
        escolha = input('Digite sua escolha: ')
        if escolha.isdigit():
            escolha = int(escolha)
            if escolha >= 0 and escolha <= 5:
                auxErro = 0
            else:
                auxErro = 1
        else:
            auxErro = 1
        if auxErro == 0:
            if escolha == 1:
                FindSerie()
            if escolha == 2:
                FindFilme()
            if escolha == 3:
                FindAleatorio()
            if escolha == 4:
                menuURL()
            if escolha == 5:
                AtualizaSerie()
        else:
            print('DIGITE UMA OPCAO VALIDA')


def menuURL():
    escolha = 100
    while escolha != 0:
        print('\n\nMENU URL\n')
        print('1-Inserir url nao confiavel')
        print('2-Para ver a lista de urls nao confiaveis')
        print('3-Excluir url nao confiavel')
        print('4-Inserir url confiavel')
        print('5-Para ver a lista de urls confiaveis')
        print('6-Excluir url confiavel')
        print('0-Voltar')
        escolha = input('Digite sua escolha: ')
        escolha = int(escolha)
        if escolha == 1:
            url = input('Digite a url nao confiavel: ')
            addLinkErrado(url)
        if escolha == 2:
            lerLinkErrado()
        if escolha == 3:
            excluirLinkErrado()
        if escolha == 4:
            url = input('Digite a url confiavel: ')
            addLinkConfiavel(url)
        if escolha == 5:
            lerLinkConfiavel()
        if escolha == 6:
            excluirLinkConfiavel()


def organizaURL(links):
    links2 = []
    links3 = []
    print('###Consertando links bagunçados - Parte 1', end='')
    for i in range(len(links)):
        if links[i][0:7] == '/url?q=':
            links2.append(links[i][7:])
    print('   OK')
    print('###Consertando links bagunçados - Parte 2', end='')
    for texto in links2:
        aux = 0
        for j in range(len(texto)-2):
            if texto[j:j+2] == '/&' or texto[j:j+2] == '&s':
                break
            else:
                aux += 1
        links3.append(texto[:aux])
    print('   OK')
    links = tiraLinksErrados(links3)
    return links


def tiraLinksErrados(links):
    links2 = []
    arq = open('LinksErrados.txt', 'r')
    texto = arq.readlines()
    for i in range(len(links)):
        aux = 0
        for j in range(len(texto)):
            texto2 = texto[j]
            texto2 = texto2[:(len(texto2)-1)]
            if re.search(texto2, links[i]) is not None:
                aux = 1
        if aux == 0:
            links2.append(links[i])
    arq.close()
    return links2


def linksErrados(link):
    aux = 0
    arq = open('LinksErrados.txt', 'r')
    texto = arq.readlines()
    for texto2 in texto:
        texto2 = texto2[:-1]
        if texto2 == link:
            aux = 1
    arq.close()
    if aux == 1:
        return True
    else:
        return False


def erros(res):
    lista = [' ', '\n', 'https://', 'https:/', 'http://', 'http:/']
    for erro in lista:
        if erro == res:
            return True
    return False


def addLinkErrado(url):
    if erros(url) is False:
        if url is not None:
            if linksErrados(url) is False:
                arq = open('LinksErrados.txt', 'r')
                texto = arq.readlines()
                url = url + '\n'
                texto.append(url)
                arq = open('LinksErrados.txt', 'w')
                arq.writelines(texto)
                arq.close()


def lerLinkErrado():
    arq = open("LinksErrados.txt", "r")
    links = arq.readlines()
    for i in range(len(links)):
        link = links[i]
        print(str(i+1) + ' - ' + link[:-1])
    arq.close()
    input()


def excluirLinkErrado():
    texto = []
    arq = open('LinksErrados.txt', 'r')
    urls = arq.readlines()
    print(urls)
    exc = input('Digite a url para excluir: ')
    pattern = re.compile(exc)
    for url in urls:
        if pattern.search(url) is None:
            texto.append(url)
    arq = open('LinksErrados.txt', 'w')
    arq.writelines(texto)
    arq.close()


def FindMagnet(links):
    magnets = []
    i = 0
    for linknovo in links:
            print('\n\n' + linknovo)
            print('###Encontrando links magneticos ' + str(i+1) + '/' + str(len(links)), end=' ')
            try:
                i += 1
                codebasenovo = requests.get(linknovo)
                soup2 = BeautifulSoup(codebasenovo.content, 'html.parser')
                for a in soup2.find_all('a'):
                    link = a.get('href')
                    if link is not None:
                        if len(link) > 6:
                            if link[0:6] == 'magnet':
                                addLinkConfiavel(linknovo)
                                magnets.append(link)
                                print('|', end='')
                print('  OK', end='')
            except:
                print('  NAO OK', end='')
                if linksConfiaveis(linknovo) is False:
                    addLinkErrado(linknovo)
    return magnets


def mostraClass(lista):
    i = 0
    print('\n\nAchamos as seguintes classificações para os torrents:')
    for link in lista:
        i += 1
        print("\n" + str(i), end='')
        aux = re.search(r'\d+mb', link)
        if aux is not None:
            print(link[aux.start():(aux.end()-2)], end='')
        print(' - ', end='')
        link = link.lower()
        if re.search(r'hdtv', link) is not None:
            print('HDTV,', end=' ')
        if re.search(r'720p', link) is not None:
            print('720p,', end=' ')
        if re.search(r'1080p', link) is not None:
            print('1080p,', end=' ')
        if re.search(r'bluray', link) is not None:
            print('BLURAY,', end=' ')
        if re.search(r'web-dl', link) is not None:
            print('WEB-DL,', end=' ')
        if re.search(r'dual', link) is not None:
            print('DUAL-AUDIO,', end=' ')
        if re.search(r'dublado', link) is not None:
            print('DUBLADO,', end=' ')
        if re.search(r'legendado', link) is not None:
            print('LEGENDADO,', end=' ')


def linksConfiaveis(link):
    aux = 0
    aux2 = re.search(r'(https://)?(http://)?(\w*\:?\.*)*\/', link)
    if aux2 is not None:
        link1 = link[aux2.start():aux2.end()]
        arq = open('LinksConfiaveis.txt', 'r')
        texto = arq.readlines()
        for texto2 in texto:
            texto2 = texto2[:-1]
            if texto2 == link1:
                aux = 1
        arq.close()
    if aux == 1:
        return True
    else:
        return False


def addLinkConfiavel(url):
    aux = re.search(r'(https://)?(http://)?(\w*\:?\.*)*\/', url)
    if aux is not None:
        if erros(aux) is False:
            if linksConfiaveis(url) is False:
                link = url[aux.start():aux.end()]
                arq = open('LinksConfiaveis.txt', 'r')
                texto = arq.readlines()
                link = link + '\n'
                texto.append(link)
                arq.close()
                arq = open('LinksConfiaveis.txt', 'w')
                arq.writelines(texto)
                arq.close()


def lerLinkConfiavel():
    arq = open("LinksConfiaveis.txt", "r")
    links = arq.readlines()
    for i in range(len(links)):
        link = links[i]
        print(str(i+1) + ' - ' + link[:-1])
    arq.close()
    input()


def excluirLinkConfiavel():
    texto = []
    arq = open('LinksConfiaveis.txt', 'r')
    urls = arq.readlines()
    print(urls)
    exc = input('Digite a url para excluir: ')
    pattern = re.compile(exc)
    for url in urls:
        if pattern.search(url) is None:
            texto.append(url)
    arq = open('LinksConfiaveis.txt', 'w')
    arq.writelines(texto)
    arq.close()


def excluiRepeticao(lista):
    lista1 = []
    for i in range(len(lista)):
        aux = 0
        for j in range(len(lista1)):
            if lista[i] == lista1[j]:
                aux = 1
        if aux == 0:
            lista1.append(lista[i])
    return lista1


def FindSerie():
    aux = 0
    sair = 0
    serien = input('Digite o nome da serie: ')
    seriet = input('Digite a temporada: ')
    seriet = int(seriet)
    serieep = input('Digite o episodio: ')
    serieep = int(serieep)
    while sair == 0 and aux < 5:
        links = []
        magnets3 = []
        qntd_links = aux*10
        qntd_links = int(qntd_links)
        if serieep < 10 and seriet < 10:
            epi = 's0' + str(seriet) + 'e0' + str(serieep)
        if serieep >= 10 and seriet < 10:
            epi = 's0' + str(seriet) + 'e' + str(serieep)
        if serieep < 10 and seriet >= 10:
            epi = 's' + str(seriet) + 'e0' + str(serieep)
        if serieep >= 10 and seriet >= 10:
            epi = 's' + str(seriet) + 'e' + str(serieep)
        serie = serien + ' ' + epi + ' legendado torrent'
        print('\n\n\n###Criando url do google - ' + str(aux+1), end='')
        for i in range(len(serie)):
            if serie[i] == ' ':
                serie = serie[:i] + '+' + serie[(i+1):]
        print('   OK')
        print('###Baixando codigo base ', end='')
        url = 'http://www.google.com.br/search?q=' + serie + '&start=' + str(qntd_links)
        codebase = requests.get(url)
        print('   OK')
        print('###Encontrando links bagunçados', end='')
        soup = BeautifulSoup(codebase.content, 'html.parser')
        for a in soup.find_all('a', href=True):
            links.append(a.get('href'))
        print('   OK')
        serie = serien + ' ' + epi + ' torrent english'
        print('###Criando url do google - ' + str(aux+1), end='')
        for i in range(len(serie)):
            if serie[i] == ' ':
                serie = serie[:i] + '+' + serie[(i+1):]
        print('   OK')
        print('###Baixando codigo base ', end='')
        url = 'http://www.google.com.br/search?q=' + serie + '&start=' + str(qntd_links)
        codebase = requests.get(url)
        print('   OK')
        print('###Encontrando links bagunçados', end='')
        soup = BeautifulSoup(codebase.content, 'html.parser')
        for a in soup.find_all('a', href=True):
            links.append(a.get('href'))
        print('   OK')
        links = organizaURL(links)
        magnets = FindMagnet(links)
        for i in range(len(magnets)):
            if conferiSerie(magnets[i].lower(), serien, epi) is True:
                magnets3.append(magnets[i])
        aux += 1
        magnets3 = excluiRepeticao(magnets3)
        if magnets3 != []:
            mostraClass(magnets3)
            escolha = 1
            while escolha != 0:
                escolha = input('\nDigite o numero da sua escolha(0-para de escolher): ')
                escolha = int(escolha)
                if escolha <= len(magnets3) and escolha > 0:
                    webbrowser.open(magnets3[escolha-1])
            if input('\n\nDigite 0, se esta satisfeito, digite 1 se quiser outras opçoes de torrent: ') is '0':
                sair = 1


def FindFilme():
    sair = 0
    aux = 0

    filmen = input('Digite o nome do filme: ')
    while sair == 0 and aux < 7:
        links = []
        magnets3 = []

        qntd_links = aux*10
        qntd_links = int(qntd_links)

        filme = filmen + ' legendado torrent'
        print('\n\n\n###Criando url do google - ' + str(aux+1), end='')
        for i in range(len(filme)):
            if filme[i] == ' ':
                filme = filme[:i] + '+' + filme[(i+1):]
        print('   OK')
        print('###Baixando codigo base ', end='')
        url = 'http://www.google.com.br/search?q=' + filme + '&start=' + str(qntd_links)
        codebase = requests.get(url)
        print('   OK')
        print('###Encontrando links bagunçados ', end='')
        soup = BeautifulSoup(codebase.content, 'html.parser')
        for a in soup.find_all('a'):
            links.append(a.get('href'))
        print('   OK')
        filme = filmen + ' dual audio torrent'
        print('###Criando url do google - ' + str(aux+1), end='')
        for i in range(len(filme)):
            if filme[i] == ' ':
                filme = filme[:i] + '+' + filme[(i+1):]
        print('   OK')
        print('###Baixando codigo base ', end='')
        url = 'http://www.google.com.br/search?q=' + filme + '&start=' + str(qntd_links)
        codebase = requests.get(url)
        print('   OK')
        print('###Encontrando links bagunçados ', end='')
        soup = BeautifulSoup(codebase.content, 'html.parser')
        for a in soup.find_all('a'):
            links.append(a.get('href'))
        print('   OK')
        links = organizaURL(links)
        magnets = FindMagnet(links)
        for i in range(len(magnets)):
            if conferiFilme(magnets[i].lower(), filmen) is True:
                magnets3.append(magnets[i])
        aux += 1
        magnets3 = excluiRepeticao(magnets3)
        if magnets3 != []:
            mostraClass(magnets3)
            escolha = 1
            while escolha != 0:
                escolha = input('\nDigite o numero da sua escolha(0-para de escolher): ')
                escolha = int(escolha)
                if escolha <= len(magnets3) and escolha > 0:
                    webbrowser.open(magnets3[escolha-1])
            if input('\n\nDigite 0, se esta satisfeito, digite 1 se quiser outras opçoes de torrent: ') is '0':
                sair = 1


def FindAleatorio():
    sair = 0
    aux = 0

    filmen = input('Digite o que quer procurar: ')
    while sair == 0 and aux < 7:
        links = []
        magnets3 = []
        qntd_links = aux*10
        qntd_links = int(qntd_links)
        filme = filmen + ' torrent'
        print('\n\n\n###Criando url do google - ' + str(aux+1), end='')
        for i in range(len(filme)):
            if filme[i] == ' ':
                filme = filme[:i] + '+' + filme[(i+1):]
        print('   OK')
        print('###Baixando codigo base ', end='')
        url = 'http://www.google.com.br/search?q=' + filme + '&start=' + str(qntd_links)
        codebase = requests.get(url)
        print('   OK')
        print('###Encontrando links bagunçados ', end='')
        soup = BeautifulSoup(codebase.content, 'html.parser')
        for a in soup.find_all('a'):
            links.append(a.get('href'))
        print('   OK')
        links = organizaURL(links)
        magnets = FindMagnet(links)
        for i in range(len(magnets)):
            if conferiFilme(magnets[i].lower(), filmen) is True:
                magnets3.append(magnets[i])
        aux += 1
        magnets3 = excluiRepeticao(magnets3)
        if magnets3 != []:
            mostraClass(magnets3)
            escolha = 1
            while escolha != 0:
                escolha = input('\nDigite o numero da sua escolha(0-para de escolher): ')
                escolha = int(escolha)
                if escolha <= len(magnets3) and escolha > 0:
                    webbrowser.open(magnets3[escolha-1])
            if input('\n\nDigite 0, se esta satisfeito, digite 1 se quiser outras opçoes de torrent: ') is '0':
                sair = 1


def FindSerieAtualiza(serien,epi):
    aux = 0
    sair = 0
    while sair == 0 and aux < 5:
        links = []
        magnets3 = []
        qntd_links = aux*10
        qntd_links = int(qntd_links)
        aux5 = re.search(r's\d+', epi)
        seriet = int(epi[1:aux5.end()])
        serieep = int(epi[(aux5.end()+1):])
        if serieep < 10 and seriet < 10:
            epi = 's0' + str(seriet) + 'e0' + str(serieep)
        if serieep >= 10 and seriet < 10:
            epi = 's0' + str(seriet) + 'e' + str(serieep)
        if serieep < 10 and seriet >= 10:
            epi = 's' + str(seriet) + 'e0' + str(serieep)
        if serieep >= 10 and seriet >= 10:
            epi = 's' + str(seriet) + 'e' + str(serieep)
        serie = serien + ' ' + epi + ' legendado torrent'
        print('\n###Criando url do google - ' + str(aux+1), end='')
        for i in range(len(serie)):
            if serie[i] == ' ':
                serie = serie[:i] + '+' + serie[(i+1):]
        print('   OK')
        print('###Baixando codigo base ', end='')
        url = 'http://www.google.com.br/search?q=' + serie + '&start=' + str(qntd_links)
        codebase = requests.get(url)
        print('   OK')
        print('###Encontrando links bagunçados', end='')
        soup = BeautifulSoup(codebase.content, 'html.parser')
        for a in soup.find_all('a', href=True):
            links.append(a.get('href'))
        print('   OK')
        serie = serien + ' ' + epi + ' torrent english'
        print('###Criando url do google - ' + str(aux+1), end='')
        for i in range(len(serie)):
            if serie[i] == ' ':
                serie = serie[:i] + '+' + serie[(i+1):]
        print('   OK')
        print('###Baixando codigo base ', end='')
        url = 'http://www.google.com.br/search?q=' + serie + '&start=' + str(qntd_links)
        codebase = requests.get(url)
        print('   OK')
        print('###Encontrando links bagunçados', end='')
        soup = BeautifulSoup(codebase.content, 'html.parser')
        for a in soup.find_all('a', href=True):
            links.append(a.get('href'))
        print('   OK')
        links = organizaURL(links)
        magnets = FindMagnet(links)
        for i in range(len(magnets)):
            if conferiSerie(magnets[i].lower(), serien, epi) is True:
                magnets3.append(magnets[i])
        aux += 1
        magnets3 = excluiRepeticao(magnets3)
        if magnets3 != []:
            mostraClass(magnets3)
            escolha = 1
            while escolha != 0:
                escolha = input('\nDigite o numero da sua escolha(0-para de escolher): ')
                escolha = int(escolha)
                if escolha <= len(magnets3) and escolha > 0:
                    webbrowser.open(magnets3[escolha-1])
            if input('\n\nDigite 0, se esta satisfeito, digite 1 se quiser outras opçoes de torrent: ') is '0':
                sair = 1


def AtualizaSerie():
    arq = open('UltimosEpisodios.txt', 'r')
    texto = arq.readlines()
    arq.close()
    for serieaux in texto:
        aux1 = re.search(r's\d+e\d+', serieaux)
        nome = serieaux[(aux1.end()+1):-1]
        episodio = serieaux[aux1.start():(aux1.end())]
        while True:
            time.sleep(1)
            aux2 = re.search(r's\d+e', episodio)
            episodiop = episodio[:aux2.end()] + str(int(episodio[aux2.end():])+1)
            # print(episodio)
            # print(episodiop)
            links = []
            url = 'http://www.minhaserie.com.br/serie/' + nome + '/episodios/' + episodiop
            # print(url)
            codebase = requests.get(url)
            soup = BeautifulSoup(codebase.content, 'html.parser')
            auxlist1 = soup.find_all("li", class_="info-post")
            if auxlist1 != []:
                # print(auxlist1)
                for a in auxlist1:
                    if re.search(r'Publicad', a.text) is None:
                        links.append(a.text)
                if links == []:
                    parar(episodio, nome)
                    break
                else:
                    # print(links[0][-11:-1])
                    aux5 = re.search(r'\d+\-', nome)
                    nomeSerie = nome[aux5.end():]
                    for i in range(len(nomeSerie)):
                        if nomeSerie[i] == '-':
                            nomeSerie = nomeSerie[:i] + ' ' + nomeSerie[(i + 1):]
                    if passou(links[0][-11:-1]) == 1:
                        print('\nO episodio ' + episodiop.upper() + ' de ' + nomeSerie.upper() + ' ainda NAO FOI BAIXADO')
                        input('\nTecle ENTER para baixa-lo')
                        FindSerieAtualiza(nomeSerie, episodiop)
                        parar(episodiop, nome)
                        episodio = episodiop
                        continue
                    else:
                        print('\nO episodio ' + episodiop.upper() + ' de ' + nomeSerie.upper() + ' sera LANCADO em ' + links[0][-11:-1])
                        parar(episodio, nome)
                        break
            else:
                parar(episodio, nome)
                break


def parar(episodio, nome):
    texto2 = []
    arq = open('UltimosEpisodios.txt', 'r')
    texto = arq.readlines()
    arq.close()
    for i in texto:
        # print(i)
        aux = re.search(nome, i)
        if aux is None:
            texto2.append(i)
        else:
            texto2.append(episodio + ' ' + i[aux.start():])
    arq = open('UltimosEpisodios.txt', 'w')
    arq.writelines(texto2)
    arq.close()


def passou(dat):
    dia = int(dat[:2])
    mes = int(dat[3:5])
    ano = int(dat[6:])
    if ano > now.year or (ano == now.year and mes > now.month) or (ano == now.year and mes == now.month and dia >= now.day):
        return 0
    else:
        return 1


menu()
