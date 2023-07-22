import aiohttp


class Gmailer:
    def __init__(self, session: aiohttp.ClientSession = aiohttp.ClientSession()):
        self.code = None
        self.session = session
        self.rapidapi = None
        self.key = None
        self.gmail = None
        self.timestamp = 0

    async def get_email(self) -> str:
        if not self.rapidapi:
            async with self.session.get('https://smailpro.com/js/chunks/smailpro_v2_email.js') as response:
                text = await response.text()
                self.rapidapi = text.split('rapidapi_key:"')[1].split('"')[0]

        if not self.key:
            async with self.session.post('https://smailpro.com/app/key',
                                         json={"domain": "gmail.com", "username": "random", "server": "server-1",
                                               "type": "alias"}) as response:
                data = await response.json()
                self.key = data['items']

        async with self.session.get(
                f'https://public-sonjj.p.rapidapi.com/email/gm/get?key={self.key}&rapidapi-key={self.rapidapi}&domain=gmail.com&username=random&server=server-1&type=alias') as response:
            data = await response.json()
            self.gmail = data['items']['email']
            return self.gmail

    async def get_messages(self) -> dict:
        self.key = await self._get_key()
        url = f'https://public-sonjj.p.rapidapi.com/email/gm/check?key={self.key}&rapidapi-key={self.rapidapi}&email={self.gmail}&timestamp={self.timestamp}'

        async with self.session.get(url) as response:
            data = await response.json()

        return data

    async def _get_key(self) -> str:
        async with self.session.post('https://smailpro.com/app/key',
                                     json={"email": self.gmail, "timestamp": self.timestamp}) as response:
            data = await response.json()
            return data['items']
