import random
import string

import aiohttp


class MailTM:
    def __init__(self, password: str = '123123qweqwe!Q', session=aiohttp.ClientSession()):
        self._mail_without_domain = None
        self._mail = None
        self._domain = None
        self._token = None
        self._password = password
        self._session = session

    async def _send_request(self, method: str, url: str, payload: dict = None) -> dict:
        async with self._session.request(method=method, url=url, json=payload) as response:
            response_json = await response.json()
        return response_json

    async def _get_domains(self) -> list:
        domains = []
        response = await self._send_request(method='get', url='https://api.mail.tm/domains')
        for domain in response['hydra:member']:
            if domain['@type'] == 'Domain':
                domains.append(domain['domain'])

        return domains

    async def _get_random_email(self) -> str:
        domains = await self._get_domains()
        domain_to_use = random.choice(domains)
        self._mail_without_domain = ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase, 30))
        self._domain = domain_to_use
        self._mail = f'{self._mail_without_domain}@{self._domain}'
        return self._mail

    async def _get_token(self):
        response = await self._send_request(method='post', url='https://api.mail.tm/token', payload=self._create_email_payload)
        print(response)
        self._token = response['token']
        self._session.headers['Authorization'] = f'Bearer {self._token}'

    async def get_mail(self):
        await self._get_random_email()
        response = await self._send_request(method='post', url='https://api.mail.tm/accounts', payload=self._create_email_payload)
        await self._get_token()
        print(response)
        return self._mail

    async def get_messages(self) -> list:
        response = await self._send_request(method='get', url='https://api.mail.tm/messages')
        print(response)
        return response['hydra:member']

    async def get_full_message(self, msg_id):
        response = await self._send_request(method='get', url=f'https://api.mail.tm/messages/{msg_id}')
        print(response)
        return response


    @property
    def _create_email_payload(self):
        return {
            'address': self._mail.lower(),
            'password': self._password
        }
