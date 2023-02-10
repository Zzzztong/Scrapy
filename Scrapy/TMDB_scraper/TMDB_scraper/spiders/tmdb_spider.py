# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/67915']

    def parse(self, response):
        
        cast_page_link = response.css("p.new_button a::attr(href)").get()
        yield scrapy.Request(url = "https://www.themoviedb.org" + cast_page_link,
                            callback=self.parse_full_credits)
        
    def parse_full_credits(self, response):

        actors_links = response.css("ol[class='people credits '] p[class!='character'] a::attr(href)").getall()
        for actor_link in actors_links:  
            yield scrapy.Request(url = "https://www.themoviedb.org" + actor_link,
                                callback=self.parse_actor_page)
    def parse_actor_page(self, response):
        

        name = response.css("h2.title a::text").get()
        
        movies = response.css("table.credit_group a.tooltip bdi::text").getall()
        
        for movie in movies:
            yield{"actor name":name,
                  "movie name":movie}


'''
    def parse(self, response):
        """
        This method starts on a movie page and navigates to the Cast & Crew page.

        It doesn't return any data, but instead yields a scrapy.Request for the Cast & Crew page. The parse_full_credits method is specified as the callback for this request.
        """
        # Hardcode the Cast & Crew page URL
        cast_and_crew_url = response.url + "cast"
    
        # Yield a request for the Cast & Crew page
        yield scrapy.Request(cast_and_crew_url, callback=self.parse_full_credits)
    
    def parse_full_credits(self, response):
        """
        This method starts on the Cast & Crew page.

        It yields a scrapy.Request for each actor's page. The parse_actor_page method is specified as the callback for these requests.
        """
        # Extract the URLs for each actor's page
        actor_urls = response.css("td.name a::attr(href)").getall()

        # Yield a request for each actor's page
        for url in actor_urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_actor_page)

    def parse_actor_page(self, response):
        """
        This method starts on an actor's page.

        It yields a dictionary with two key-value pairs:
        {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}.
        """
        # Extract the actor's name
        actor_name = response.css("h1.header::text").get()

        # Extract the names of the movies or TV shows on which the actor has worked
        movie_or_TV_names = response.css("div.knownfor-title-role a::text").getall()

        # Yield a dictionary for each movie or TV show
        for movie_or_TV_name in movie_or_TV_names:
            yield {"actor": actor_name, "movie_or_TV_name": movie_or_TV_name}



'''

    


