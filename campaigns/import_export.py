from import_export import resources, fields
from import_export.widgets import CharWidget
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from campaigns.models import Recipient

import logging
logger = logging.getLogger(__name__)


class RecipientResource(resources.ModelResource):
    name = fields.Field(attribute="name", column_name="name")
    email = fields.Field(attribute="email", column_name="email")
    subscription_status = fields.Field(attribute="subscription_status",column_name="subscription_status",widget=CharWidget())

    class Meta:
        model = Recipient
        import_id_fields = ("email",)
        fields = ("name", "email", "subscription_status")
        skip_unchanged = True
        report_skipped = True
        use_bulk = True

    def before_import_row(self, row, **kwargs):
        email = row.get("email")
        if not email:
            raise ValidationError("Email is required")
        email = email.strip().lower()
        row["email"] = email
        try:
            validate_email(email)
        except ValidationError as v:
            logger.exception("Exception {}".format(v.args))
            raise ValidationError(f"Invalid email: {email}")

        if not row.get("subscription_status"):
            row["subscription_status"] = "subscribed"