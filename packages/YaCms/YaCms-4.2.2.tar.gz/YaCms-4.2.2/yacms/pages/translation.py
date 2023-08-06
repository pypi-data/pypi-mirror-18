from modeltranslation.translator import translator, TranslationOptions
from yacms.core.translation import (TranslatedDisplayable,
                                        TranslatedRichText)
from yacms.pages.models import Page, RichTextPage, Link


class TranslatedPage(TranslatedDisplayable):
    fields = ('titles',)


class TranslatedRichTextPage(TranslatedRichText):
    fields = ()


class TranslatedLink(TranslationOptions):
    fields = ()

translator.register(Page, TranslatedPage)
translator.register(RichTextPage, TranslatedRichTextPage)
translator.register(Link, TranslatedLink)
