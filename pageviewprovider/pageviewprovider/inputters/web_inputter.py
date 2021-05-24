from contextlib import closing
from interface import implements
from requests import Session
from requests.adapters import HTTPAdapter
# pylint: disable=import-error
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import RequestException
from .inputter import Inputter


class WebInputter(implements(Inputter)):
    ENDPOINT = 'https://dumps.wikimedia.org/other/pageviews'
    BROWSERS_USER_AGENT = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                           'AppleWebKit/537.36 (KHTML, like Gecko)',
                           'Chrome/90.0.4430.212', 'Safari/537.36',
                           'Edg/90.0.818.62']

    def __init__(self):
        # retry strategy in case of failed request
        self.__retry_strategy = Retry(
            total=6,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )
        self.__adapter = HTTPAdapter(max_retries=self.__retry_strategy)
        self.__http = Session()
        self.__http.mount("https://", self.__adapter)
        self.__http.mount("http://", self.__adapter)

    def parse_input(self, date_time):
        try:
            # formats url from datetime
            url = self.__format_url(date_time)
            # sets headers for the request
            headers = {'User-Agent': ' '.join(WebInputter.BROWSERS_USER_AGENT)}
            # perform a GET operation to the url, gets response
            web_response = self.__http.get(url, headers=headers, stream=True)

            with closing(web_response):
                # checks if status code is OK (200)
                if (self.__is_good_response(web_response)):
                    return web_response.content
                else:
                    print(f'\nBad response in: {url}')
                    print(f'Status code: {web_response.status_code}')
                    print(f'Status reason: {web_response.reason}')
                    return None
        except RequestException as e:
            print('\nError in WebInputter during' +
                  f'requests to {url} : {str(e)}')
            return None
        except Exception as e:
            print(f'\nError in WebInputter due to: {e}')
            return None

    def __format_url(self, date_time):
        # formats date_time properties to match url pattern
        year = date_time.year
        format_month_year = date_time.strftime('%Y-%m')
        format_datetime_code = date_time.strftime('%Y%m%d')
        format_hours = date_time.strftime('%H')

        return (f'{self.ENDPOINT}/{year}/{format_month_year}/' +
                f'pageviews-{format_datetime_code}-{format_hours}0000.gz')

    def __is_good_response(self, response):
        # returns if status code is 200 and content-type is not None
        return (response.status_code == 200 and
                response.headers['Content-Type'] is not None)
