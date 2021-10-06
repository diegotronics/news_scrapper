import requests
import lxml.html as html
from requests import status_codes
import datetime
import os

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.37'
HOME_URL = 'https://www.xataka.com/'

XPATH_LINK_TO_ARTICLE = '//article//h2[@class="abstract-title"]/a/@href'
XPATH_TITLE = '//article/div/header/h1/span/text()'
XPATH_BODY = '//div[@class="article-content"]//p/text()'



def parse_notice(link, today, index):
    try:
        response = requests.get(link, headers={'User-Agent': USER_AGENT})
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/article-{index}.txt', 'w', encoding='utf-8') as f:
                
                f.write(title)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error {response.status_code} en link: {link}')
    except ValueError as ve:
        print(ve)



def parse_home():
    try:
        response = requests.get(HOME_URL, headers={'User-Agent': USER_AGENT})
        if response.status_code == 200:
            home = response.content.decode('utf-8')

            parsed = html.fromstring(home)

            links = parsed.xpath(XPATH_LINK_TO_ARTICLE)

            # Crear archivo
            today  = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            index = 1
            for link in links:
                parse_notice(link, today, index)
                index += 1
            

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def main():
    parse_home()


if __name__ == '__main__':
    main()
    