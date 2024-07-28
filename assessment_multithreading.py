import requests
from bs4 import BeautifulSoup
import json

# Global headers to be used for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

def extract_json_ld(soup):
    """Extrai e retorna o JSON-LD da página."""
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            json_ld = json.loads(script.string)
            if isinstance(json_ld, dict) and json_ld.get('@type') == 'ItemList':
                return json_ld
        except json.JSONDecodeError:
            continue
    return None

def extract_movies(soup):
    """Extrai e imprime informações dos filmes a partir dos dados JSON-LD."""
    json_ld = extract_json_ld(soup)
    if json_ld is None:
        print("Dados JSON-LD não encontrados.")
        return

    movies = json_ld.get('itemListElement', [])
    for item in movies:
        movie = item.get('item', {})
        title = movie.get('name')
        url = movie.get('url')
        description = movie.get('description')
        image = movie.get('image')
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Description: {description}")
        print(f"Image: {image}")
        print("-" * 20)

def main():
    """Função principal para buscar e processar a página de filmes populares da IMDb."""
    url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erro ao acessar {url}: Status {response.status_code}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    extract_movies(soup)

if __name__ == '__main__':
    main()
