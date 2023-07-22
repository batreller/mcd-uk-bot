from languages import BaseLanguage


class RussianLanguage(BaseLanguage):
    __name__ = 'rus'


BaseLanguage.add_language(RussianLanguage())
