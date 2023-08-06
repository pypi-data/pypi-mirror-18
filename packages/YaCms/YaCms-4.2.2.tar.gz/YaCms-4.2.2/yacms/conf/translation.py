from modeltranslation.translator import translator, TranslationOptions
from yacms.conf.models import Setting


class TranslatedSetting(TranslationOptions):
    fields = ('value',)

translator.register(Setting, TranslatedSetting)
