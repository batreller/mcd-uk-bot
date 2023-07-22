from languages import BaseLanguage


class UkrainianLanguage(BaseLanguage):
    __name__ = 'ukr'


BaseLanguage.add_language(UkrainianLanguage())
