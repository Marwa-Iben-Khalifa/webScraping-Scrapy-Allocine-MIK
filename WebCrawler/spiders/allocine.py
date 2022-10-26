
import scrapy
from scrapy import Request
from WebCrawler.items import ReviewsAllocineItem

class AllocineSpider(scrapy.Spider):
    name = 'allocine'
    allowed_domains = ['www.allocine.fr']
    start_urls= [f'https://www.allocine.fr/film/meilleurs/?page={n}' for n in range(1,10)]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        liste_film= response.css('li.mdl')

        # Boucle qui parcours l'ensemble des éléments de la liste des films
        for film in liste_film:
            item = ReviewsAllocineItem()

            # Nom du film
            try:
                item['title'] = film.css('a.meta-title-link::text').extract()[0]
            except:
                item['title'] = 'None'
              
            # Lien de l'image du film
            try:
                item['img'] = film.css('img').attrib['src']
            except:
                item['img'] = 'None'


            # Auteur du film
            try:
                item['author'] = film.css('a.blue-link::text').extract()
            except:
                item['author'] = 'None'
           
            # Durée du film
            try:
                item['time'] = film.css('div.meta-body-item.meta-body-info::text').extract()[0].split('\n')[1]
            except:
                item['time'] = 'None'

            # Genre cinématographique
            try:
                item['genre'] = ' '.join(film.css('div.meta-body-info').css('span::text').extract()[1:])
            except:
                 item['genre'] = 'None'

            # Score du film
            try:
                item['score'] = film.css('span.stareval-note::text').extract()[0]
            except:
                item['score'] = 'None'

            # Description du film
            try:
                item['desc'] = film.css('div.content-txt::text').extract()
            except:
                item['desc'] = 'None'

            # Date de sortie
            try:
                item['release'] = film.css('span.date::text').extract()
            except:
                item['release'] = 'None'
            
            #numéro de page
            try:
                item['page']= response.url.split('page=')[-1]
            except:
                item['page']='None'


            yield item

