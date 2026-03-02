from django import forms
from campaigns.models import Campaign


class CampaignForm(forms.ModelForm):
    scheduled_time = forms.DateTimeField(required=False,widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))

    class Meta:
        model = Campaign
        fields = ["campaign_name","subject_line","email_content","scheduled_time","status"]