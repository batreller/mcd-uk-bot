import asyncio

import aiohttp


class McDonalds:
    _BASE_URL = 'https://www.mcdfoodforthoughts.com'
    _AMOUNT_SPENT_1 = 2
    _AMOUNT_SPENT_2 = 5
    _QUESTION_ANSWER = 2
    _JS_ENABLED = 1
    _FIP = True

    def __init__(self, code: str):
        self._code = code
        self._code_parts = [self._code[:4], self._code[4:8], self._code[8:]]
        self._session = None
        self._next_button = None
        self._next_url = '/'
        self._progress = None
        self._posted_fns = None
        self._ionf = None
        self._finished = False

    async def activate_code(self) -> str:
        """
        :return: mcdonalds code (e.g. H11M3DJJNKWN)
        """
        while not self._finished:
            response = await self._send_request(method='post', url=self._next_url, data=self._question_answer_payload)

        response_text = await response.text()
        print('ok')
        return response_text.split('QRCode" alt="')[1].split('"')[0]

    async def validate_code(self) -> bool:
        """
        :return: if code is valid
        """
        await self._send_request(method='get', url='/')
        await self._send_request(method='post', url=self._next_url, data=self._starter_payload)
        await self._send_request(method='post', url=self._next_url, data=self._have_receipt_payload)
        await self._send_request(method='post', url=self._next_url, data=self._input_code_payload)
        print('validated')
        if self._progress is not None:
            return True
        return False

    @property
    def _question_answer_payload(self):
        payload = {
            'IoNF': self._ionf,
            'PostedFNS': self._posted_fns,
            'OneQuestionLeftUnansweredErrorMessageTemplate': 'There is {0} error on the page.',
            'MoreQuestionsLeftUnansweredErrorMessageTemplate': 'There are {0} errors on the page.'
        }
        for fn in self._posted_fns.split('|'):
            payload[fn] = self._QUESTION_ANSWER
        return payload

    @property
    def _starter_payload(self) -> dict:
        return {
            'P': 1,
            'JavaScriptEnabled': self._JS_ENABLED,
            'FIP': self._FIP,
            'NextButton': 'Continue'
        }

    @property
    def _have_receipt_payload(self) -> dict:
        return {
            'P': 2,
            'JavaScriptEnabled': self._JS_ENABLED,
            'FIP': self._FIP,
            'Receipt': 1,
            'NextButton': 'Next',
            'RadioButtonNames': 'Receipt'
        }

    @property
    def _input_code_payload(self) -> dict:
        return {
            'JavaScriptEnabled': self._JS_ENABLED,
            'FIP': self._FIP,
            'OneQuestionLeftUnansweredErrorMessageTemplate': 'There is {0} error on the page.',
            'MoreQuestionsLeftUnansweredErrorMessageTemplate': 'There are {0} errors on the page.',
            'CN1': self._code_parts[0],
            'CN2': self._code_parts[1],
            'CN3': self._code_parts[2],
            'AmountSpent1': self._AMOUNT_SPENT_1,
            'AmountSpent2': self._AMOUNT_SPENT_2,
            'NextButton': self._next_button
        }

    async def _ensure_aiohttp_session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(base_url=self._BASE_URL)
            self._session.headers[
                'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

    async def _get_answers_to_next_question(self, response: str) -> None:
        try:
            self._posted_fns = response.split('PostedFNS" value="')[1].split('"')[0]
            self._ionf = response.split('IoNF" value="')[1].split('"')[0]
        except IndexError:
            ...

    async def _renew_variables(self, response: str) -> None:
        try:
            self._finished = self._progress == 100 or 'We appreciate your feedback' in response
            self._next_url = '/' + response.split('action="')[1].split('"')[0]
            self._next_button = response.split('NextButton" value="')[1].split('"')[0]
            self._progress = int(response.split('<div id="ProgressPercentage">')[1].split('<')[0].replace('%', ''))
        except IndexError:
            ...

        if self._progress is not None:
            await self._get_answers_to_next_question(response)

    async def _send_request(self, method: str, url: str, data: dict = None):
        await self._ensure_aiohttp_session()

        async with self._session.request(method=method, url=url, data=data, ssl=False) as response:
            response_text = await response.text()

        await self._renew_variables(response_text)
        return response
