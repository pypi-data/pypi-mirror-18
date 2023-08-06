
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AgileUserMixin(models.Model):

    customer_id     = models.CharField(_('Agile Customer ID'), max_length=70, null=True, blank=True)
    customer_name   = models.CharField(_('Agile Customer Name'), max_length=254, null=True, blank=True)

    member_id       = models.CharField(_('Agile Member ID'), max_length=70, null=True, blank=True)
    member_number   = models.CharField(_('Agile Member Number'), max_length=70, null=True, blank=True)
    membership_id   = models.CharField(_('Agile Membership ID'), max_length=70, null=True, blank=True)

    agile_only      = models.BooleanField(default=False)

    class Meta:
        abstract = True

