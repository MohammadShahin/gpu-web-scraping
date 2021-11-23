from stem import Signal
from stem.control import Controller
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import os
from dotenv import load_dotenv


load_dotenv()
N = int(os.getenv('ALLOWED_REQUESTS'))


def new_tor_identity():
    """
    A method to change the tor identity.
    """
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=os.getenv('PASSWORD'))
        controller.signal(Signal.NEWNYM)


class ProxyMiddleware(HttpProxyMiddleware):

    num_requests = 0

    def process_response(self, request, response, spider):
        """
        This method is used to change the TOR identity when the response's status of some request is not successful.
        """
        if response.status != 200:
            new_tor_identity()
            return request
        return response

    def process_request(self, request, spider):
        """
        This method is used to change the TOR identity every N requests.
        """
        # if ProxyMiddleware.num_requests == N:
        #     new_tor_identity()
        #     ProxyMiddleware.num_requests = 1
        # else:
        #     ProxyMiddleware.num_requests += 1
        new_tor_identity()
        request.meta['proxy'] = 'http://127.0.0.1:8118'
