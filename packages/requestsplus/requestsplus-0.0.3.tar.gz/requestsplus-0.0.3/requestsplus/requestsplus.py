import requests
from time import sleep
import random


class RequestsPlus:

    def __init__(self, max_retries=10, header=None,
                 p_sleep=0, sleep_time_mutiplier=10, timeout=60):
        """

        :param max_retries: Default 10 times
        :param header: Default None
        :param p_sleep: Default 0%. Probabilty of sleep for each request
        :param sleep_time_mutiplier: A multiplier that times a random number betweet [1 - p_sleep, 1] as sleeping time
        :param timeout: Default 60 secs
        """
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
        self.session.mount('https://', adapter)
        self.header = header
        self.p_sleep = p_sleep
        self.sleep_time_mutiplier = sleep_time_mutiplier
        self.timeout = timeout

    def get(self, url):
        prob = random.random()
        if prob < self.p_sleep:
            sleep(self.sleep_time_mutiplier * (1 - prob))
        return self.session.get(url, headers=self.header, timeout=self.timeout)
