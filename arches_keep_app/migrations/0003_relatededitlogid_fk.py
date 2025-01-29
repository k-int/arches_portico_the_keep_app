from django.db.migrations.recorder import MigrationRecorder
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('arches_keep_app', '0002_add_plugin'),
    ]

    def update_all_relatededitlogids(apps, schema_editor):
        """
        Function to update all existing LREs.  If many in the database, this migration could take a while.
        """
        EditLog = apps.get_model("models", "EditLog")
        LatestResourceEdit = apps.get_model("arches_keep_app", "LatestResourceEdit")

        lres = LatestResourceEdit.objects.all()
        for lre in lres:
            edit = EditLog.objects.order_by('resourceinstanceid', '-timestamp').distinct('resourceinstanceid').get(resourceinstanceid=lre.resourceinstanceid)
            lre.relatededitlogid = edit
            lre.save()

    def remove_all_relatededitlogids(apps, schema_editor):
        """
        Empty reverse function, as the reverse migration will delete the column and contents.
        """
        ...


    # NOTE: this is a very hacky method to get the reverse migration to work.  
    # Reversing migration with "models.editlog" string produces error `ValueError: Related model 'models.editlog' cannot be resolved` ...
    # ... as for some unknown reason django can't see the arches models app in reverse.  In reverse if we have the model name as ...
    # ... arches_keep_app.latestresourceedit then the migration can reverse successfully, despite not looking at the correct linked table (editlog)
    applied_migrations = MigrationRecorder.Migration.objects.filter(app="arches_keep_app").values_list('name', flat=True)
    if "0003_relatededitlogid_fk" in applied_migrations:
        model_name = "arches_keep_app.latestresourceedit"
    else:
        model_name = "models.editlog"

    operations = [
        migrations.RenameField(
            model_name='latestresourceedit',
            old_name='editlogid',
            new_name='latestresourceeditid',
        ),
        migrations.AddField(
            model_name='latestresourceedit',
            name='relatededitlogid',
        field=models.OneToOneField(blank=True, db_column='relatededitlogid', null=True, on_delete=django.db.models.deletion.PROTECT, to=model_name),
        ),
        migrations.RunPython(update_all_relatededitlogids, remove_all_relatededitlogids)
    ]
