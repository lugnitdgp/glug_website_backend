from django.contrib import admin
from django.utils.html import format_html 
# from main.models import Event, Profile, ImageCard
from main import models

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import escape
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

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
            width='450px',
            height='auto',
            )
        )

    def action_show(self, obj):
        print(obj.pk)
        return format_html('<a class="button" href="#">Toggle Show</a>', pk=obj.pk)
    
    action_show.allow_tags = True
    action_show.short_description = "Show On Site"

### This Section Handels the Log Entry

action_names = {
    ADDITION: 'Addition',
    CHANGE:   'Change',
    DELETION: 'Deletion',
}

class FilterBase(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        if self.value():
            dictionary = dict(((self.parameter_name, self.value()),))
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
        return tuple((u.id, u.username)
            for u in User.objects.filter(pk__in =
                LogEntry.objects.values_list('user_id').distinct())
        )

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

    readonly_fields = [ f.name for f in LogEntry._meta.get_fields()]

    list_filter = [
        UserFilter,
        ActionFilter,
        'content_type',
        # 'user',
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]


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
## Logentry code Ends

## Session Admin code starts
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

    list_display = ['session_key', 'get_username', 'expire_date']


admin.site.register(Session, SessionAdmin)
## SessionAdmin code ends

admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Profile)
admin.site.register(models.ImageCard)
admin.site.register(models.About)
admin.site.register(models.Contact)
