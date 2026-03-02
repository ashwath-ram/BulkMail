from django.urls import path
from campaigns.views.campaign import create_campaign, campaign_list
from campaigns.views.dashboard import campaign_dashboard, campaign_detail

urlpatterns = [
    path("", campaign_dashboard, name="campaign_dashboard"),
    path("<int:campaign_id>/", campaign_detail, name="campaign_detail"),

    path("campaign/create/", create_campaign, name="create_campaign"),
    path("campaign/list/", campaign_list, name="campaign_list"),
]