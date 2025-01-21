from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_save

from arches.app.models.resource import Resource
from arches.app.models.tile import Tile
from arches.app.models.models import EditLog

import uuid

class LatestResourceEdit(models.Model):
    latestresourceeditid = models.UUIDField(primary_key=True, default=uuid.uuid1)
    relatededitlogid = models.OneToOneField(
        "models.EditLog", on_delete=models.CASCADE, blank=True, null=True)
    resourcedisplayname = models.TextField(blank=True, null=True)
    resourceinstanceid = models.TextField(blank=True, null=True)
    edittype = models.TextField(blank=True, null=True)
    graphid = models.TextField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    userid = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    @receiver(post_save, sender=EditLog)
    def update_latest_resource_edit(instance, **kwargs):
        """Update LatestResourceEdit resource row after EditLog save"""
        
        def create_new_latest_resource_edit():
            latest_edit = LatestResourceEdit()
            latest_edit.resourceinstanceid = instance.resourceinstanceid
            latest_edit.resourcedisplayname = instance.resourcedisplayname
            latest_edit.edittype = instance.edittype
            latest_edit.graphid = instance.resourceclassid
            latest_edit.userid = instance.userid
            latest_edit.username = instance.user_username
            latest_edit.timestamp = instance.timestamp
            latest_edit.relatededitlogid = instance
            latest_edit.save()

        if LatestResourceEdit.objects.filter(resourceinstanceid=instance.resourceinstanceid):
            try:
                existing_lre = LatestResourceEdit.objects.get(resourceinstanceid=instance.resourceinstanceid)
                LatestResourceEdit.objects.update_or_create(
                    latestresourceeditid=existing_lre.latestresourceeditid,
                    defaults={
                        'resourceinstanceid':instance.resourceinstanceid,
                        'resourcedisplayname':instance.resourcedisplayname,
                        'edittype':instance.edittype,
                        'graphid':instance.resourceclassid,
                        'userid':instance.userid,
                        'username':instance.user_username,
                        'timestamp':instance.timestamp,
                        'relatededitlogid':instance
                    }
                )
            except:
                # more than one row for resourceinstanceid - delete all rows
                LatestResourceEdit.objects.filter(resourceinstanceid=instance.resourceinstanceid).delete()
                create_new_latest_resource_edit()
        else:
            create_new_latest_resource_edit()

    class Meta:
        managed = True
        db_table = "latest_resource_edit"