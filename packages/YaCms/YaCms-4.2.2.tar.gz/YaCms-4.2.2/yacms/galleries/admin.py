from __future__ import unicode_literals

from django.contrib import admin

from yacms.core.admin import TabularDynamicInlineAdmin
from yacms.pages.admin import PageAdmin
from yacms.galleries.models import Gallery, GalleryImage
from yacms.utils.static import static_lazy as static


class GalleryImageInline(TabularDynamicInlineAdmin):
    model = GalleryImage


class GalleryAdmin(PageAdmin):

    class Media:
        css = {"all": (static("yacms/css/admin/gallery.css"),)}

    inlines = (GalleryImageInline,)


admin.site.register(Gallery, GalleryAdmin)
