from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from campaigns.models import Campaign, EmailLog

import logging
logger = logging.getLogger(__name__)


def campaign_dashboard(request):
    try:
        campaigns = Campaign.objects.filter(is_active=True).order_by("-created_at")
        return render(request, "dashboard.html", {"campaigns": campaigns})
    
    except Exception as e:
        logger.exception("Exception {}".format(e.args))
        return render(request, "error.html", {"error": e.args})


def campaign_detail(request, campaign_id):
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        logs = EmailLog.objects.filter(campaign=campaign).order_by("-created_at")

        return render(request, "campaign_detail.html", {"campaign": campaign,"logs": logs})

    except Exception as e:
        logger.exception("Exception {}".format(e.args))
        return render(request, "error.html", {"error": e.args})