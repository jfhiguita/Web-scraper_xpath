import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'


XPATH_LINK_TO_ARTICLE = '//h2/a/@href'
XPATH_TITLE = '//h1[@class="headline"]/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="articleWrapper  "]/p[not(@class)]/text()'


# extrae los links de las noticias
def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home) # aca convierte el contenido html  para poder hacer xpath
            links_to_notice = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_notice)
            today = datetime.date.today().strftime('%d-%m-%Y')
            # crea la carpeta today sino existe
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notice:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            article = response.content.decode('utf-8')
            parsed = html.fromstring(article)

            # este try, except lo creo por si alguna noticia no tiene titulo o resumen no la incluya
            try:
                title_for_link = parsed.xpath(XPATH_TITLE)[0]
                title_for_link = title_for_link.replace('\"', '')
                summary_for_link = parsed.xpath(XPATH_SUMMARY)[0]
                body_for_link = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/{title_for_link}.txt', 'w', encoding='utf-8') as f:
                f.write(title_for_link)
                f.write('\n\n')
                f.write(summary_for_link)
                f.write('\n\n')
                for p in body_for_link:
                    f.write(p)
                    f.write('\n')


        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)




#ejecuta el archivo
def run():
    parse_home()


if __name__ == "__main__":
    run()
