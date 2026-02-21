from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ToolIdCardRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(default='', max_length=20, verbose_name='姓名')),
                ('idcard', models.CharField(db_index=True, max_length=18, unique=True, verbose_name='身份证号')),
                ('status', models.SmallIntegerField(db_index=True, default=0, verbose_name='状态(0未使用 1已使用)')),
            ],
            options={
                'verbose_name': '身份证记录',
                'verbose_name_plural': '身份证记录',
                'db_table': 'tools_idcard_record',
            },
        ),
    ]
