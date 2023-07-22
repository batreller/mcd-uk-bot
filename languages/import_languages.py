import importlib
import os


def import_languages():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for lang in os.listdir(current_dir):
        lang_path = os.path.join(current_dir, lang)
        if os.path.isdir(lang_path):
            importlib.import_module(f'.{lang}', package=__package__)
