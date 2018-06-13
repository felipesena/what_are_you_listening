import requests, sys, threading, json
from bs4 import BeautifulSoup

#Create by Felipe Sena
#on 08/12/2017

class Recomendation(object):

    filename = "files/artists.json"
    url = "https://www.last.fm/music/%s/+listeners?page="
    user_url = "https://www.last.fm%s"
    users = []
    artists = []

    def getartistrecomendation(self, artist): #Método principal onde chama outros métodos para buscar artistas relacionados
        self.url = self.url % self.formatname(artist) + "%d"
        last_page = 10

        for i in range(1, last_page):
            t = threading.Thread(target=self.getartistlisteners, args=(i,))
            t.start()

        while threading.active_count() != 1:
            pass

        with open(self.filename, 'w') as file:
            json.dump(Recomendation.users, file)

        file = open(self.filename)
        datafile = json.load(file)
        file.close()

        for data in datafile:
            t = threading.Thread(target=self.getartists, args=(data,))
            t.start()

        while threading.active_count() != 1:
            pass

        with open(self.filename, 'w') as file:
            json.dump(Recomendation.artists, file)

    def getartists(self, user): #Busca top artistas baseadas nos usuários buscados
        url = self.user_url % user
        response = requests.get(url)
        plain_text = response.text

        soup = BeautifulSoup(plain_text, "html.parser")

        if response.status_code == 200:
            print(url)

            if len(soup.findAll('ol')) == 0:
                if len(soup.findAll('p', {'class': 'no-data-message'})) <= 2:
                    for span in soup.findAll('table')[1].findAll('span', {'class':'chartlist-ellipsis-wrap'}):
                        artistname = span.find_next('a').attrs['title']
                        Recomendation.artists.append(artistname)

    def getartistlisteners(self, page): #Busca usuários que escutam o artista em questão
        response = requests.get(self.url % page)
        plain_text = response.text
        soup = BeautifulSoup(plain_text, "html.parser")

        if response.status_code == 200:
            for h4 in soup.findAll('h4', {'class':'user-list-name'}):
                Recomendation.users.append(h4.find_next('a').get('href'))

    def formatname(self, artist): #Formata nome do artista para fazer request
        formatted = artist[0]

        if (len(artist) == 1):
            return formatted
        else:
            for name in artist[1:]:
                formatted += "+" + name

        return formatted


if __name__ == '__main__':
    artist = sys.argv[1:]
    recomendation = Recomendation()
    recomendation.formatname(artist)


