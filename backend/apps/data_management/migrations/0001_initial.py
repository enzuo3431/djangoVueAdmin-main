from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ArchivePhoneData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('phone', models.BigIntegerField(db_index=True, unique=True, verbose_name='手机号')),
                ('is_filtered', models.BooleanField(db_index=True, default=False, verbose_name='是否命中过滤')),
                ('status', models.SmallIntegerField(db_index=True, default=1, verbose_name='状态(1正常 0禁用)')),
                ('source', models.CharField(db_index=True, default='manual', max_length=32, verbose_name='数据来源')),
                ('register_flags', models.PositiveIntegerField(default=0, verbose_name='平台注册标识(bitmask)')),
                ('platforms', models.CharField(db_index=True, default='', max_length=64, verbose_name='平台注册平台(逗号分隔)')),
                ('remark', models.CharField(blank=True, db_index=True, default='', max_length=255, verbose_name='备注')),
                ('extra', models.JSONField(blank=True, default=dict, verbose_name='扩展字段')),
            ],
            options={
                'verbose_name': '归档数据',
                'verbose_name_plural': '归档数据',
                'db_table': 'data_archive_phone',
            },
        ),
    ]
