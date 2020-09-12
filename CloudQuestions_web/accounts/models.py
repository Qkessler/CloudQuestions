from django.db import models
from datetime import datetime
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Group(models.Model):
    created = models.DateField(default=datetime.now)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, db_index=True
    )
    max_users = models.IntegerField(default=10)

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")


class GroupConnection(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True
    )

    class Meta:
        verbose_name = _("group connection")
        verbose_name_plural = _("group connections")

