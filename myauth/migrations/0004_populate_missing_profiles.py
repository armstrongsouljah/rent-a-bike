from django.db  import migrations


def forwards_func(apps, schema_editor):
    UserProfile = apps.get_model('myauth', 'UserProfile')
    User = apps.get_model('myauth', 'User')
    users = User.objects.filter(user_profile__isnull=True)
    profiles = [UserProfile(user=user) for user in users]
    UserProfile.objects.bulk_create(profiles)

def backwards_func(apps, schema_editor):
    UserProfile = apps.get_model('myauth', 'UserProfile')
    UserProfile.objcets.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('myauth', '0003_alter_userprofile_user')
    ]
    operations = [
        migrations.RunPython(forwards_func, backwards_func)
    ]
