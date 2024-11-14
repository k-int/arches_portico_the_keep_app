from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_save

from arches.app.models.resource import Resource
from arches.app.models.tile import Tile

import uuid

class LatestResourceEdit(models.Model):
    editlogid = models.UUIDField(primary_key=True, default=uuid.uuid1)
    resourcedisplayname = models.TextField(blank=True, null=True)
    resourceinstanceid = models.TextField(blank=True, null=True)
    edittype = models.TextField(blank=True, null=True)
    graphid = models.TextField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    userid = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "latest_resource_edit"