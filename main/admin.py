from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from main import models
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import escape
from django.urls import reverse, NoReverseMatch, path
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.contrib.sessions.models import Session
from django.contrib.contenttypes.models import ContentType
from django.utils.crypto import get_random_string

admin.site.site_header = "GLUG Backend | Admin Panel"
admin.site.site_url = "http://nitdgplug.org/"
admin.site.index_template = "admin/custom_index.html"


#Linit Admin


class LinitImageInline(admin.TabularInline):
    model = models.LinitImage
    extra = 1


class LinitAdmin(admin.ModelAdmin):
    list_display = ('title', 'year_edition', 'document_url')
    list_filter = ('year_edition',)
    search_fields = ('title', 'description')
    ordering = ('-year_edition',)

    def clean_document_url(self, obj):
        """Validate document URL format"""
        if obj.document_url and not obj.document_url.endswith('.pdf'):
            raise ValidationError('URL must point to a PDF document')
    
    inlines = [LinitImageInline]


admin.site.register(models.Linit, LinitAdmin)


class LinitImageAdmin(admin.ModelAdmin):
    list_display = ('image', )
    list_filter = ('linit_year', )


admin.site.register(models.LinitImage, LinitImageAdmin)

#Linit Section End


class EventAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'status', 'show', 'action_show']
    readonly_fields = ['event_image_preview']
    actions = ['mark_draft', 'mark_final']

    def mark_draft(self, req, queryset):
        queryset.update(status="DRAFT")

    mark_draft.short_description = "Mark Event Data as Draft"

    def mark_final(self, req, queryset):
        queryset.update(status="FINAL")

    mark_final.short_description = "Mark Event Data as Final"

    def event_image_preview(self, obj):
        return format_html('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.event_image.url,
            width='450px',
            height='auto',
        ))

    # Overriding the get_urls() method to add custom urls
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('toggle_show/<int:event_id>',
                 self.admin_site.admin_view(self.process_toggle),
                 name='toggle-event-show'),
        ]
        return custom_urls + urls

    # Code For Toggle Button
    def process_toggle(self, request, event_id):
        event_obj = self.get_object(request, event_id)
        event_obj.show = not event_obj.show
        event_obj.save()
        ct = ContentType.objects.get_for_model(event_obj)
        return_url = reverse('admin:%s_%s_changelist' % (ct.app_label, ct.model))

        return HttpResponseRedirect(return_url, {})

    # Code to show the action button
    def action_show(self, obj):
        return format_html('<a class="button" href="{}">Toggle Show</a>',
                           reverse('admin:toggle-event-show', args=[obj.pk]))

    action_show.allow_tags = True
    action_show.short_description = "Toggle Show"


class SpecialTokenAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'used', 'max_usage', 'valid_till']
    readonly_fields = ['value', 'used']


# This Section Handels the Log Entry

action_names = {
    ADDITION: 'Addition',
    CHANGE: 'Change',
    DELETION: 'Deletion',
}


class FilterBase(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        if self.value():
            dictionary = dict(((self.parameter_name, self.value()), ))
            return queryset.filter(**dictionary)


class ActionFilter(FilterBase):
    title = 'action'
    parameter_name = 'action_flag'

    def lookups(self, request, model_admin):
        return action_names.items()


class UserFilter(FilterBase):
    """Use this filter to only show current users, who appear in the log."""
    title = 'user'
    parameter_name = 'user_id'

    def lookups(self, request, model_admin):
        return tuple(
            (u.id, u.username) for u in User.objects.filter(pk__in=LogEntry.objects.values_list('user_id').distinct()))


class AdminFilter(UserFilter):
    """Use this filter to only show current Superusers."""
    title = 'admin'

    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(is_superuser=True))


class StaffFilter(UserFilter):
    """Use this filter to only show current Staff members."""
    title = 'staff'

    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(is_staff=True))


class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

    readonly_fields = [f.name for f in LogEntry._meta.get_fields()]

    list_filter = [
        UserFilter,
        ActionFilter,
        'content_type',
        # 'user',
    ]

    search_fields = ['object_repr', 'change_message']

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_description',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        ct = obj.content_type
        repr_ = escape(obj.object_repr)
        try:
            href = reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id])
            link = '<a href="%s">%s</a>' % (href, repr_)
        except NoReverseMatch:
            link = repr_
        return format_html(link) if obj.action_flag != DELETION else repr_

    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = 'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')

    def action_description(self, obj):
        return action_names[obj.action_flag]

    action_description.short_description = 'Action'


admin.site.register(LogEntry, LogEntryAdmin)
# Logentry code Ends

# Session Admin code starts


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    def get_username(self, obj):
        session_data = obj.get_decoded()
        uid = session_data.get('_auth_user_id', None)
        try:
            user_obj = User.objects.get(pk=uid)
        except Exception:
            user_obj = None

        if user_obj:
            return user_obj
        else:
            return "Anon"

    get_username.short_description = "Username"

    def has_add_permission(self, request):
        return False

    list_display = ['session_key', 'get_username', 'expire_date']


admin.site.register(Session, SessionAdmin)
# SessionAdmin code ends


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'is_staff',
    )
    actions = ['set_random_pass']

    def set_random_pass(self, req, queryset):
        for user in queryset:
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()

    set_random_pass.short_description = "Set random password"


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'user', 'email', 'passout_year']
    actions = [
        'convert_to_alumni',
    ]

    def convert_to_alumni(modeladmin, request, queryset):
        for profile in queryset:
            profile.convert_to_alumni = True
            profile.save(commit=True)

    convert_to_alumni.short_description = 'Convert to Alumni'

class FacadAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'post', 'email','image']

class AlumniAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'passout_year']


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Project)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Facad, FacadAdmin)
admin.site.register(models.Alumni, AlumniAdmin)
admin.site.register(models.CarouselImage)
admin.site.register(models.About)
admin.site.register(models.Contact)
admin.site.register(models.Activity)
admin.site.register(models.Timeline)
admin.site.register(models.SpecialToken, SpecialTokenAdmin)
admin.site.register(models.TechBytes)
admin.site.register(models.DevPost)
admin.site.register(models.Config)
