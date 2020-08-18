from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse, NoReverseMatch, path
from blog import models


class PostAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'featured', 'show', 'action_show']
    readonly_fields = ['pub_date', 'thumbnail_image_preview']
    actions = ['toggle_featured']

    def thumbnail_image_preview(self, obj):
        return format_html(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.thumbnail_image.url,
                width='450px',
                height='auto',
            )
        )

    # Overriding the get_urls() method to add custom urls
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('toggle_show/<int:post_id>',
                 self.admin_site.admin_view(self.process_toggle),
                 name='toggle-post-show'),
        ]
        return custom_urls + urls

    # Code For Toggle Button
    def process_toggle(self, request, post_id):
        post_obj = self.get_object(request, post_id)
        post_obj.show = not post_obj.show
        post_obj.save()
        ct = ContentType.objects.get_for_model(post_obj)
        return_url = reverse('admin:%s_%s_changelist' %
                             (ct.app_label, ct.model))

        return HttpResponseRedirect(return_url, {})

    # Code to show the action button
    def action_show(self, obj):
        return format_html('<a class="button" href="{}">Toggle Show</a>',
                           reverse('admin:toggle-post-show', args=[obj.pk]))

    def toggle_featured(modeladmin, request, queryset):
        for post in queryset:
            if post.featured is True:
                post.featured = False
            else:
                post.featured = True
            post.save()

    toggle_featured.short_description = 'Toggle Featured'
    action_show.allow_tags = True
    action_show.short_description = "Toggle Show"


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'


# Register your models here.
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment)
