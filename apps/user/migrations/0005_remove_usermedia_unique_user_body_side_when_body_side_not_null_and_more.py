# Generated by Django 4.1.13 on 2024-05-13 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_profile_email'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='usermedia',
            name='unique_user_body_side_when_body_side_not_null',
        ),
        migrations.AlterField(
            model_name='usermedia',
            name='body_side',
            field=models.CharField(blank=True, choices=[('front', 'front'), ('back', 'back'), ('left', 'left'), ('right', 'right')], max_length=16, null=True),
        ),
        migrations.AddConstraint(
            model_name='usermedia',
            constraint=models.UniqueConstraint(condition=models.Q(('body_side__isnull', False), models.Q(('body_side__exact', ''), _negated=True)), fields=('user', 'body_side'), name='unique_user_body_side_when_body_side_not_null'),
        ),
    ]
