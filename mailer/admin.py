from django.contrib import admin
from mailer.models import MailSent

class MailSentAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in MailSent._meta.get_fields()]

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

admin.site.register(MailSent, MailSentAdmin)