from json import loads
from random import choice
from time import sleep

import cloudscraper
from unicaps import CaptchaSolver, CaptchaSolvingService
from bs4 import BeautifulSoup
from eth_account import Account
from requests import get
from pyuseragents import random as random_useragent


class FarmerToken:
    def __init__(self, captcha_id: str, name_captcha: str, proxy: list[str] = None) -> None:
        self.scraper = cloudscraper.create_scraper()
        self.captcha_id = captcha_id
        self.proxy = proxy
        self.name_capthca = name_captcha

    def captcha2(self):
        captcha = {'2captcha.com': CaptchaSolvingService.TWOCAPTCHA,
                   'anti-captcha.com': CaptchaSolvingService.ANTI_CAPTCHA}
        with CaptchaSolver(captcha[self.name_capthca], self.captcha_id) as solver:
            # solve CAPTCHA
            solved = solver.solve_recaptcha_v2(
                site_key="6LfmSZciAAAAADgF5jcfcwBlptwNwWyDPr762YZk",
                page_url="https://registration.vendiblelabs.tech/"
            )
            # get response token
            return solved.solution.token

    def post2(self, captcha: str, adress: str, mail: str, proxy=None) -> None:
        proxy_ = {'http': proxy,
                  'https': proxy}
        headers = {
            'authority': 'govendible.com',
            'sec-ch-ua': '"Chromium";v="98", " Not A;Brand";v="99", "Chrome";v="98"',
            'accept': 'application/json, text/plain, */*',
            # Already added when you pass json=
            # 'content-type': 'application/json',
            'sec-ch-ua-mobile': '?0',
            'user-agent': random_useragent(),
            'token': captcha,
            'sec-ch-ua-platform': '"macOS X"',
            'origin': 'https://registration.vendiblelabs.tech',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://registration.vendiblelabs.tech/',
            'accept-language': 'be-BY,be',
        }
        self.scraper.headers.update(headers)

        json_data = {
            'email': mail,
            'address': adress,
            'network': 'polygon',
        }

        if self.proxy:
            self.scraper.post('https://govendible.com/api/verify-email',
                              headers=headers, json=json_data, proxies=proxy_)
        else:
            self.scraper.post('https://govendible.com/api/verify-email',
                              headers=headers, json=json_data)

    def post3(self, mail: str, adress: str, reff: str, code: str, proxy=None) -> None:
        proxy_ = {'http': proxy,
                  'https': proxy}
        headers = {
            'authority': 'govendible.com',
            'sec-ch-ua': '"Chromium";v="98", " Not A;Brand";v="99", "Chrome";v="98"',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'user-agent': random_useragent(),
            'token': 'henl.e.ylawr.e.nce.j1.74@gmail.com',
            'sec-ch-ua-platform': '"macOS X"',
            'origin': 'https://registration.vendiblelabs.tech',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://registration.vendiblelabs.tech/',
            'accept-language': 'be-BY,be',
        }
        self.scraper.headers.update(headers)

        json_data = {
            'email': mail,
            'code': code,
            'network': 'polygon',
            'address': adress,
            'referral': reff,
        }
        if self.proxy:
            self.scraper.post('https://govendible.com/api/rewards-register',
                              headers=headers, json=json_data, proxies=proxy_)
        else:
            self.scraper.post('https://govendible.com/api/rewards-register',
                              headers=headers, json=json_data)

    @staticmethod
    def verf_mail(login: str) -> str:
        for _ in range(5):
            r = get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain=qiott.com')
            if len(loads(r.text)) >= 1:
                text = loads(r.text)[0]["id"]
                g = get(
                    f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain=qiott.com&id={text}')
                texts = loads(g.text)['htmlBody']
                soup = BeautifulSoup(texts, 'html.parser')
                text = soup.findAll(class_="pb-30")
                return str(text[0].find('span')).split('>')[1].split('<')[0]
            else:
                sleep(3)

    @staticmethod
    def get_username() -> str:
        return "".join([choice("abcdefghijklmnopqrstuvwxyz013456789") for _ in range(8)])

    def run(self, num: int, ref: str) -> None:
        for i in range(num):
            address = Account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530').address
            username = self.get_username()
            if self.proxy:
                self.post2(mail=f'{username}@qiott.com', adress=address, captcha=self.captcha2(), proxy=self.proxy[i])
                code = self.verf_mail(username)
                self.post3(mail=f'{username}@qiott.com', code=code, adress=address, reff=ref, proxy=self.proxy[i])
            else:
                self.post2(mail=f'{username}@qiott.com', adress=address, captcha=self.captcha2())
                code = self.verf_mail(username)
                self.post3(mail=f'{username}@qiott.com', code=code, adress=address, reff=ref)
            print(f'Аккаунт № {i + 1}')
        print('Работа окончена ...')


def main() -> None:
    name_captcha = int(input('1: 2captcha.com, 2: anti-captcha.com(1 / 2): '))
    if name_captcha == 1:
        name_captcha = '2captcha.com'
    else:
        name_captcha = 'anti-captcha.com'
    captcha_id = input('Captcha API: ')
    try:
        num = int(input('Колличество аккаунтов: '))
    except TypeError:
        raise TypeError('Введите целое число от 1 ...')
    reff = input('Ref id(?referral=>>>...<<<): ')
    if len(reff) != 16:
        raise 'Неверный реф код'
    proxy = input('proxy: yes / no')
    if proxy in ('yes', 'YES', 'Yes', 'y'):
        with open('proxy.txt', 'r') as file:
            token_proxy = file.read().splitlines()
            if len(token_proxy) < num:
                raise f'Прокси меньше чем повторов, прокси: {len(token_proxy)}, повторов: {num}'
        solved = FarmerToken(captcha_id=captcha_id, proxy=token_proxy, name_captcha=name_captcha)
    else:
        solved = FarmerToken(captcha_id=captcha_id, name_captcha=name_captcha)
    solved.run(num, reff)

if __name__ == '__main__':
    main()
