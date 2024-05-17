from django.contrib import admin
from .models import AccessKey
# Register your models here.


class AccessKeyAdmin(admin.ModelAdmin):
    list_display = ('name','key', 'user', 'created_at', 'updated_at','status')
    search_fields = ('key', 'user__email')
    list_filter = ('created_at', 'updated_at','status','user')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    actions = ["revoke_key"]

    @admin.action(description="Revoked Access Key")
    def revoke_key(self, request, queryset):
        queryset.update(status="revoked")


admin.site.register(AccessKey)