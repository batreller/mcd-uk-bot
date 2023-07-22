import aiohttp

from .proxy import Proxy


class Subway:
    _BASE_URL = 'https://rewards.subway.co.uk'
    is_free = True

    def __init__(self, mail: str,
                 proxy: Proxy,
                 password: str = '123123qweqwe!Q',
                 name: str = 'Jeremy',
                 surname: str = 'Wonka',
                 promocode: str = ''):
        self._proxy = proxy
        self._mail = mail
        self._password = password
        self._name = name
        self._surname = surname
        self._promocode = promocode
        self._session = None
        self._token = None
        self.__class__.is_free = False

    async def register(self) -> dict:
        response = await self._send_request('post', '/tx-sub/registration',
                                            payload=self._registration_payload)
        return response

    async def validate_code(self, code: str) -> dict:
        response = await self._send_request('put',
                                            f'/tx-sub/registration/activation/{code}')
        if response.get('login') is not None:
            self._token = response['login'].get('token')
            self._session.headers['Authorization'] = f'Bearer {self._token}'
        return response

    async def get_me(self) -> dict:
        response = await self._send_request(method='get', url='/tx-sub/members')
        self.__class__.is_free = True
        return response

    async def _ensure_aiohttp_session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(base_url=self._BASE_URL)
            self._session.headers[
                'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            self._session.headers['Modulecode'] = 'SUB_STORMBORN'
            self._session.headers['Authorization'] = '[object Object]'
            self._session.headers['Content-Type'] = 'application/json'
            self._session.headers['Sec-Ch-Ua'] = '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"'

    async def _send_request(self, method: str, url: str, payload: dict = None) -> dict:
        await self._ensure_aiohttp_session()

        async with self._session.request(method=method, url=url, json=payload, proxy=self._proxy.proxy) as response:
            print(await response.text())
            response_json = await response.json()
            print(response_json)

        return response_json

    @property
    def _registration_payload(self) -> dict:
        return {
            'channelApp': 0,
            'channelSMS': 0,
            'channelEmail': 0,
            'typeOffer': 0,
            'typeCompetitions': 0,
            'typeNews': 0,
            'mobile': '',
            'postcode': '',
            'email': self._mail,
            'firstName': self._name,
            'lastName': self._surname,
            'accessCode': '',
            'card': '',
            'promoCode': self._promocode,
            'countryId': 5,
            'birthDate': '21-07-1988',
            'password': self._password
        }

    @property
    def _validation_payload(self) -> dict:
        return {
            'email': self._mail,
            'card': '',
            'accessCode': '',
            'promoCode': self._promocode
        }
