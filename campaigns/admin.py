from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin
from campaigns.import_export import RecipientResource
from campaigns.models import Recipient, Campaign, EmailLog


@admin.register(Recipient)
class RecipientAdmin(ImportExportModelAdmin):
    resource_class = RecipientResource
    list_display = ("id","name", "email", "subscription_status", "is_active","created_at")
    readonly_fields = ('created_at',)
    list_filter = ("subscription_status",)


@admin.register(Campaign)
class CampaignAdmin(ImportExportModelAdmin):
    list_display = ('id','campaign_name','subject_line',"scheduled_time","status","is_active","created_at")
    readonly_fields = ['created_at']

@admin.register(EmailLog)
class EmailLogAdmin(ImportExportModelAdmin):
    list_display = ('id','campaign','recipient_email',"status","status","created_at")
    readonly_fields = ['created_at']