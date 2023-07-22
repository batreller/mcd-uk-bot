import os
from abc import ABC

from fluent.runtime import FluentLocalization, FluentResourceLoader


class BaseLanguage(ABC):
    languages = {}

    @classmethod
    def add_language(cls, language):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        lang_dir = os.path.join(current_dir, f'{language.__name__}/{language.__name__}.ftl')
        print(f'{language.__name__} successfully added!')
        if not os.path.exists(lang_dir):
            raise ValueError(f'You did not specify language file for "{language.__name__}" language')

        loader = FluentResourceLoader(current_dir + '/{locale}')
        l10n = Languages([language.__name__], [f'{language.__name__}.ftl'], loader)
        cls.languages[language.__name__] = l10n


class Languages(FluentLocalization):
    languages = {}

    def __init__(self, locales, *args):
        self.__class__.languages[locales[0]] = self
        super().__init__(locales, *args)

    @classmethod
    def swap_language(cls, new_lang):
        return cls.languages[new_lang]
