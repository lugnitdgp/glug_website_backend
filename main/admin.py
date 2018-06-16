from django.contrib import admin
from django.utils.html import format_html 
from main.models import Event, Profile, ImageCard

class EventAdmin(admin.ModelAdmin):
    list_display = ['identifier','status','show','action_show']
    readonly_fields = ['event_image_preview']
    actions = ['mark_draft','mark_final']


    def mark_draft(self, req, queryset):
        queryset.update(status="DRAFT")
    
    mark_draft.short_description = "Mark Event Data as Draft"

    def mark_final(self, req, queryset):
        queryset.update(status="FINAL")
    
    mark_final.short_description = "Mark Event Data as Final"

    def event_image_preview(self, obj):
        return format_html(
            '<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.event_image.url,
            width='400px',
            height='400px',
            )
        )

    def action_show(self, obj):
        print(obj.pk)
        return format_html('<a class="button" href="#">Toggle Show</a>', pk=obj.pk)
    
    action_show.allow_tags = True
    action_show.short_description = "Show On Site"

admin.site.register(Event, EventAdmin)
admin.site.register(Profile)
admin.site.register(ImageCard)