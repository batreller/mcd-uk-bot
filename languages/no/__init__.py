from languages import BaseLanguage


class NoLanguage(BaseLanguage):
    __name__ = 'no'


BaseLanguage.add_language(NoLanguage())
