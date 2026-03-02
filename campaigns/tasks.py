from celery import shared_task
from campaigns.models import Campaign
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from datetime import datetime
from django.db import transaction
from campaigns.models import Recipient,Campaign, EmailLog
from django.core.mail import send_mail
from django.db.models import Count, Q, F
from django.template import Template, Context
from django.conf import settings

import logging
logger = logging.getLogger(__name__)


@shared_task
def execute_campaign(campaign_id):
    try:
        recipient_list = list(Recipient.objects.filter(subscription_status="subscribed",is_active=1).values_list("email", flat=True))

        campaign = Campaign.objects.get(id=campaign_id)
        campaign.status = "in_progress"
        campaign.total_recipients = len(recipient_list)
        campaign.save(update_fields=["status","total_recipients"])

        logs = []
        for email in recipient_list:
            logs.append(EmailLog(
                campaign=campaign,
                recipient_email=email,
                status="pending"
            ))
        
        EmailLog.objects.bulk_create(logs, batch_size=1000)

        BATCH_SIZE = 100 # can be moved to setings
        for i in range(0, len(recipient_list), BATCH_SIZE):
            batch = recipient_list[i:i + BATCH_SIZE]
            send_email_batch.delay(campaign.id, batch)
    
    except Exception as e:
        logger.exception("Exception {}".format(e.args))
        raise


@shared_task
def send_email_batch(campaign_id, email_batch):
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        for email in email_batch:
            log = EmailLog.objects.get(campaign=campaign,status='pending',recipient_email=email)

            try:
                send_mail(
                    subject=campaign.subject_line,
                    message=campaign.email_content,
                    from_email="no-reply@example.com",
                    recipient_list=[email],
                    fail_silently=False,
                )
                msg = EmailMultiAlternatives(
                    subject=campaign.subject_line,
                    body="This email requires HTML support.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )

                msg.attach_alternative(campaign.email_content, "text/html")
                msg.send()

                log.status = "sent"
                log.save(update_fields=["status"])
                Campaign.objects.filter(id=campaign_id).update(sent_count=F("sent_count") + 1)

            except Exception as e:
                log.status = "failed"
                log.error_message = str(e)
                log.save(update_fields=["status", "error_message"])

                Campaign.objects.filter(id=campaign_id).update(failed_count=F("failed_count") + 1)
        update_campaign_status.delay(campaign_id)

    except Exception as e:
        logger.exception("Exception {}".format(e.args))
        raise


@shared_task
def update_campaign_status(campaign_id):
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        # stats = campaign.aggregate(total=Count("total_recipients"),sent=Count("sent_count"),
        #     failed=Count("failed_count") )

        if campaign.sent_count + campaign.failed_count == campaign.total_recipients:
            campaign.status = "completed"
            campaign.save(update_fields=["status"])
    
    except Exception as e:
        logger.exception("Exception {}".format(e.args))
        raise


@shared_task
def check_scheduled_campaigns():
    campaigns = Campaign.objects.filter(status="scheduled",is_active=True,scheduled_time__lte=timezone.now())

    for campaign in campaigns:
        execute_campaign.delay(campaign.id)
