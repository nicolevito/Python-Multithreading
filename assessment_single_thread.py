import requests
import time
import csv
import random
from bs4 import BeautifulSoup
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

def extract_json_ld(soup):
    """Extrai o JSON-LD da página."""
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            json_ld = json.loads(script.string)
            if isinstance(json_ld, dict) and json_ld.get('@type') == 'ItemList':
                return json_ld
        except json.JSONDecodeError:
            continue
    return None

def extract_movie_details(movie):
    """Extrai detalhes dos filmes e salva em um CSV."""
    title = movie.get('name')
    url = movie.get('url')
    description = movie.get('description')
    image = movie.get('image')
    
    # Opcional: Para um link válido, é necessário fazer scraping da página do filme
    # Isto pode ser feito com uma função adicional, se necessário
    
    with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:
        movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        movie_writer.writerow([title, url, description, image])
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Description: {description}")
        print(f"Image: {image}")
        print("-" * 1)

def extract_movies(soup):
    """Extrai e processa os filmes da página usando JSON-LD."""
    json_ld = extract_json_ld(soup)
    if json_ld is None:
        print("Dados JSON-LD não encontrados.")
        return

    movies = json_ld.get('itemListElement', [])
    for item in movies:
        movie = item.get('item', {})
        extract_movie_details(movie)

def main():
    start_time = time.time()

    # IMDB Most Popular Movies - 100 movies
    popular_movies_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    response = requests.get(popular_movies_url, headers=headers)
    if response.status_code != 200:
        print(f"Erro ao acessar {popular_movies_url}: Status {response.status_code}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Main function to extract the 100 movies from IMDB Most Popular Movies
    extract_movies(soup)

    end_time = time.time()
    print("Total time taken: ", end_time - start_time)

if __name__ == '__main__':
    main()
