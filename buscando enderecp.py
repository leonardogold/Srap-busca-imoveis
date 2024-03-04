import json
import cloudscraper
from parsel import Selector
from models import Imoveis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CONN = 'sqlite:///banco1.db'
engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

scraper = cloudscraper.create_scraper()

# Buscar todas as URLs no banco de dados
registros = session.query(Imoveis).all()

for registro in registros:
    # Verificar se o campo endereco está vazio
    if registro.url and not registro.endereco:
        url2 = registro.url
        print(f"URL encontrada no banco de dados: {url2}")

        # Tentar acessar a URL até 10 vezes em caso de erro
        for tentativa in range(1, 11):
            try:
                r = scraper.get(url2)
                response = Selector(text=r.text)
                html = response.xpath(f'//script[@id="initial-data"]')
                html2 = html.get()
                html_selector = Selector(text=html2)

                endereco = json.loads(html_selector.css('::attr(data-json)').get()).get('ad', {}).get('locationProperties', [])

                # Lista para armazenar todos os endereços
                lista_enderecos = []

                for house in endereco:
                    endereco_completo = house.get('label') + ': ' + house.get('value')

                    # Adicionar o endereço à lista
                    lista_enderecos.append(endereco_completo)

                # Unir todos os endereços em uma string e adicionar ao registro
                registro.endereco = '\n'.join(lista_enderecos)

                # Commit da sessão para atualizar o banco de dados
                session.commit()

                print(f'Endereços atualizados no banco de dados:\n{registro.endereco}')
                print(f'Sucesso na tentativa {tentativa}')
                break  # Se bem-sucedido, sair do loop de tentativas
            except Exception as e:
                print(f'Tentativa {tentativa} falhou. Erro: {str(e)}')

        else:
            print(f"Erro: Não foi possível acessar a URL após 10 tentativas.")

# Adicione qualquer código adicional fora do loop, se necessário
