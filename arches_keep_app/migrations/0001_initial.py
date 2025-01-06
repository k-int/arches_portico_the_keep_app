from django.db import migrations, models
import uuid
from arches.app.models.system_settings import settings


def populate_latest_resource_edits(apps, schema_editor):
    EditLogModel = apps.get_model("models", "EditLog")
    LatestResourceEditModel = apps.get_model("arches_keep_app", "LatestResourceEdit")

    edits = EditLogModel.objects.order_by('resourceinstanceid', '-timestamp').distinct('resourceinstanceid')

    for edit in edits:
        if edit.resourceinstanceid != settings.SYSTEM_SETTINGS_RESOURCE_ID:
            latest_edit = LatestResourceEditModel()
            latest_edit.resourceinstanceid = edit.resourceinstanceid
            latest_edit.resourcedisplayname = edit.resourcedisplayname
            latest_edit.edittype = edit.edittype
            latest_edit.username = edit.user_username
            latest_edit.userid = edit.userid
            latest_edit.graphid = edit.resourceclassid
            latest_edit.timestamp = edit.timestamp
            latest_edit.save()


def remove_latest_resource_edits(apps, scheme_editor):
    latest_edits = apps.get_model("arches_keep_app", "LatestResourceEdit")

    for edits in latest_edits.objects.all():
        edits.delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LatestResourceEdit',
            fields=[
                ('editlogid', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('resourcedisplayname', models.TextField(blank=True, null=True)),
                ('resourceinstanceid', models.TextField(blank=True, null=True)),
                ('edittype', models.TextField(blank=True, null=True)),
                ('graphid', models.TextField(blank=True, null=True)),
                ('username', models.TextField(blank=True, null=True)),
                ('userid', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'latest_resource_edit',
                'managed': True,
            },
        ),
        migrations.RunPython(populate_latest_resource_edits, remove_latest_resource_edits),        
    ]
