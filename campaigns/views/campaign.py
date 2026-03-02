from django.shortcuts import render, redirect
from campaigns.forms import CampaignForm
from campaigns.models import Campaign


def create_campaign(request):
    if request.method == "POST":
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)

            if campaign.scheduled_time and campaign.status == "draft":
                campaign.status = "scheduled"

            campaign.save()
            return redirect("campaign_list")
    else:
        form = CampaignForm()

    return render(request, "create_campaign.html", {"form": form})


def campaign_list(request):
    campaigns = Campaign.objects.filter(is_active=1).order_by("-created_at")
    return render(request, "campaign_list.html", {"campaigns": campaigns})