from languages import BaseLanguage


class EnglishLanguage(BaseLanguage):
    __name__ = 'eng'


BaseLanguage.add_language(EnglishLanguage())
