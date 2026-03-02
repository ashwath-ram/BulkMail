from django.db import models

# Create your models here.
# receipient
# Name
# - Email Address
# - Subscription Status (Subscribed / Unsubscribed)

# # campaign
# Campaign Name
# - Subject Line
# - Email Content (plain text or HTML)
# - Scheduled Time for Sending

# delivery log For each email

# campaign reports

# apps/recipients/models.py


class Recipient(models.Model):
    SUBSCRIPTION = [("subscribed", "Subscribed"),("unsubscribed", "Unsubscribed")]

    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True, db_index=True)
    subscription_status = models.CharField(max_length=20,choices=SUBSCRIPTION,default="subscribed")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}"
    
    class Meta:
        db_table = 'recipient'
    

class Campaign(models.Model):

    STATUS = [("draft", "Draft"),("scheduled", "Scheduled"),("in_progress", "In Progress"),("completed", "Completed")]

    campaign_name = models.CharField(max_length=100)
    subject_line = models.CharField(max_length=100)
    email_content = models.TextField()
    scheduled_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS,default="draft")
    total_recipients = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.campaign_name
    
    class Meta:
        db_table = 'campaign'


class EmailLog(models.Model):
    STATUS_CHOICES = [("pending", "Pending"),("sent", "Sent"),("failed", "Failed")]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    recipient_email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    error_message = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'email_log'
