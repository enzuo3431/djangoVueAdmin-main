from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_department_logs_sessions'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataPermissionRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('field', models.CharField(max_length=100, verbose_name='字段名')),
                ('operator', models.CharField(choices=[('eq', '等于'), ('ne', '不等于'), ('lt', '小于'), ('lte', '小于等于'), ('gt', '大于'), ('gte', '大于等于'), ('in', '包含'), ('contains', '包含文本'), ('icontains', '包含文本(忽略大小写)'), ('startswith', '前缀匹配'), ('endswith', '后缀匹配'), ('isnull', '为空')], max_length=20, verbose_name='操作符')),
                ('value', models.TextField(blank=True, null=True, verbose_name='值')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_rules', to='core.role', verbose_name='角色')),
            ],
            options={
                'verbose_name': '数据权限规则',
                'verbose_name_plural': '数据权限规则',
                'db_table': 'sys_data_permission_rule',
            },
        ),
    ]
