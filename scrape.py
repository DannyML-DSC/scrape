from requests import get
url = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'
response = get(url)
print(response.text[:500])

#amazing soup
from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

#getting required columns, name,year,rating and metascore
movie_containers = html_soup.find_all('div', class_ ='lister-item mode-advanced')
print(type(movie_containers))
print(len(movie_containers))
first_movie = movie_containers[0]
first_movie
first_movie.div
first_movie.h3
first_movie.h3.a
first_movie.h3.a.text
first_year = first_movie.h3.find('span', class_ = 'lister-item-year text-muted unbold')
first_year
first_year = first_year.text
first_year
first_movie.strong
first_imdb = float(first_movie.strong.text)
first_imdb
first_mscore = first_movie.find('span', class_ ='metascore favorable')
first_mscore = int(first_mscore.text)

first_mscore

find_votes = first_movie.find('span', attrs = {'name':'nv'})
find_votes
find_votes['data-value']
find_votes = int(find_votes['data-value'])
eight_movie_mscore = movie_containers[7].find('div', class_ = 'ratings-metascore')
type(eight_movie_mscore)

#creating emty containers to scrape contents into
names = []
years = []
imdb_ratings = []
metascores = []
votes = []

#looping through to get values for containers
for container in movie_containers:
    #if the movie has meascore then extract 
    if container.find('div',class_ = 'ratings-metascore') is not None:
        
        #the name 
        name = container.h3.a.text
        names.append(name)
        
        #the year
        year = container.h3.find('span', class_ = 'lister-item-year').text
        years.append(year)
        
        #the imdb rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)
        
        #the metascore
        m_score = container.find('span', class_ = 'metascore').text
        metascores.append(int(m_score))
        
        #the number of votes
        vote = container.find('span', attrs = {'name':'nv'})['data-value']
        votes.append(int(vote))
        
#getting scraped data with pandas        
import pandas as pd
test_df = pd.DataFrame({'movie': names,
                        'year':years,
                        'ratings': imdb_ratings,
                        'metascore': metascores,
                        'votes': votes})

test_df.info()
test_df        

#read to csv
movie = pd.DataFrame(test_df)
movie.to_csv('movie.csv')
mov = pd.read_csv('movie.csv')
mov
mov = mov.drop(['year'], axis=1)
mov.insert(1, 'year', 2017)
mov