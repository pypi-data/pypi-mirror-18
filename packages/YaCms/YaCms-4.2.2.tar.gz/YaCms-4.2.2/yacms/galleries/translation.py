from modeltranslation.translator import translator, TranslationOptions
from yacms.core.translation import TranslatedRichText
from yacms.galleries.models import GalleryImage, Gallery


class TranslatedGallery(TranslatedRichText):
    fields = ()


class TranslatedGalleryImage(TranslationOptions):
    fields = ('description',)

translator.register(Gallery, TranslatedGallery)
translator.register(GalleryImage, TranslatedGalleryImage)
