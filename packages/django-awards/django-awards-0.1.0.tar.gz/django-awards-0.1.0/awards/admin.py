from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import BadgeAward


@admin.register(BadgeAward)
class BadgeAwardAdmin(admin.ModelAdmin):
    THUMB_SIZE = 40

    list_display = ('user', 'slug', 'name', 'level', 'points', 'awarded_on', 'image')
    raw_id_fields = ('user', )
    list_filter = ('slug', 'level', 'points', )
    search_fields = ('slug', 'level')

    def image(self, obj):
        return '<img src="{path}" width="{size}" height="{size}">'.format(
            path=obj.image_url, size=self.THUMB_SIZE)
    image.allow_tags = True
    image.short_description = _('image')
