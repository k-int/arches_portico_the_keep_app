from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("arches_keep_app", "0001_initial")
    ]

    forward = """
        INSERT INTO plugins (
            pluginid, name, icon, component, componentname, config, slug, sortorder)
        VALUES (
            'eb53e958-9ddf-40a9-8acd-da2b27df8340',
            'Keep Integration Dashboard',
            'fa fa-link',
            'views/components/plugins/keep_integration_dashboard',
            'keep_integration_dashboard', 
            '{"show": true, "is_workflow": false, "description": ""}',
            'keep_integration_dashboard',
            '1'
        );
        """
    
    reverse = """
        DELETE FROM plugins where pluginid = 'eb53e958-9ddf-40a9-8acd-da2b27df8340';
        """

    operations = [
        migrations.RunSQL(forward, reverse),
    ]