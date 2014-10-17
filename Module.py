from core import ModuleManager

from bs4 import BeautifulSoup as bs4
from urllib.parse import quote, parse_qs, urlparse


class Module:
    def query(self, query):
        result = {
            'result': [],
        }

        http = ModuleManager.call_module_method(
            'http_lib',
            'get',
            'https://encrypted.google.com/search?q=%s&num=10000' % quote(query)
        )

        if not 'html' in http:
            result['error'] = 'No server responce'
            return result

        soup = bs4(http['html'])

        for title in soup.find_all('h3', attrs={'class': 'r'}):
            element = title.find('a')
            # parse google url
            g_url = urlparse(element['href'])
            g_args = parse_qs(g_url.query)
            url = g_args['q'][0]

            result['result'].append({
                'title': element.text,
                'url': url,
            })

        return result

