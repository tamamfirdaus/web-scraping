# Library
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

# Link of IMDb web containing popular movies
url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'

# Initialize dict
popular_movies = {}

# Create MySpider inherit from scrapy.Spider
class MySpider(scrapy.Spider):
  name = 'myspider'
  
  # Start request
  def start_requests(self): 
    yield scrapy.Request(
      url = url,
      callback = self.parse
    )

  # Parsing function
  def parse(self, response):
    # Write out to a html file
    html_file = 'popular_movies.html'
    with open(html_file, 'wb') as fout:
      fout.write(response.body)

    # Parse the information using Xpath or CSS Locator
    movie_titles = response.xpath('//td[@class="titleColumn"]/a/text()').extract()
    movie_links = response.xpath('//td[@class="titleColumn"]/a/@href').extract()
    movie_dir_player = response.css('td.titleColumn > a::attr(title)').extract()

    # Save them to popular_movies dict
    popular_movies['Movie Title'] = movie_titles
    popular_movies['Link'] = movie_links
    popular_movies["Director and Player"] = movie_dir_player


# Run spider
process = CrawlerProcess()
process.crawl(MySpider)
process.start()

# Convert to dataframe
popular_movies_df = pd.DataFrame(popular_movies)

# Add 'https://www.imdb.com' into movie link 
popular_movies_df['Link'] = 'https://www.imdb.com' + popular_movies_df['Link']

# Print popular_movies and save it to csv file
print(popular_movies_df)
popular_movies_df.to_csv('popular_movies.csv')
