from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_permission_component_permission_icon_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='部门名称')),
                ('sort_order', models.IntegerField(default=0, verbose_name='排序')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否启用')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='core.department', verbose_name='上级部门')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门',
                'db_table': 'sys_department',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='core.department', verbose_name='部门'),
        ),
        migrations.AddField(
            model_name='role',
            name='data_scope',
            field=models.CharField(choices=[('all', '全部数据权限'), ('dept', '本部门数据权限'), ('dept_and_child', '本部门及下级数据权限'), ('self', '仅本人数据权限'), ('custom', '自定义数据权限')], default='all', max_length=20, verbose_name='数据权限范围'),
        ),
        migrations.CreateModel(
            name='RoleDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.department', verbose_name='部门')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.role', verbose_name='角色')),
            ],
            options={
                'verbose_name': '角色-部门关联',
                'verbose_name_plural': '角色-部门关联',
                'db_table': 'sys_role_department',
                'unique_together': {('role', 'department')},
            },
        ),
        migrations.AddField(
            model_name='role',
            name='departments',
            field=models.ManyToManyField(blank=True, through='core.RoleDepartment', to='core.department', verbose_name='自定义部门权限'),
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('jti', models.CharField(max_length=64, unique=True, verbose_name='JWT ID')),
                ('token_type', models.CharField(default='access', max_length=10, verbose_name='令牌类型')),
                ('ip_address', models.CharField(blank=True, max_length=64, null=True, verbose_name='IP地址')),
                ('user_agent', models.TextField(blank=True, null=True, verbose_name='User-Agent')),
                ('last_activity', models.DateTimeField(auto_now=True, verbose_name='最后活跃时间')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否有效')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户会话',
                'verbose_name_plural': '用户会话',
                'db_table': 'sys_user_session',
            },
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('username', models.CharField(blank=True, max_length=150, null=True, verbose_name='用户名')),
                ('status', models.CharField(choices=[('success', '成功'), ('failed', '失败')], max_length=10, verbose_name='状态')),
                ('ip_address', models.CharField(blank=True, max_length=64, null=True, verbose_name='IP地址')),
                ('user_agent', models.TextField(blank=True, null=True, verbose_name='User-Agent')),
                ('message', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
                ('login_time', models.DateTimeField(auto_now_add=True, verbose_name='登录时间')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '登录日志',
                'verbose_name_plural': '登录日志',
                'db_table': 'sys_login_log',
            },
        ),
        migrations.CreateModel(
            name='OperationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('username', models.CharField(blank=True, max_length=150, null=True, verbose_name='用户名')),
                ('method', models.CharField(max_length=10, verbose_name='请求方法')),
                ('path', models.CharField(max_length=255, verbose_name='请求路径')),
                ('params', models.TextField(blank=True, null=True, verbose_name='请求参数')),
                ('response', models.TextField(blank=True, null=True, verbose_name='响应结果')),
                ('status_code', models.IntegerField(default=200, verbose_name='响应状态码')),
                ('ip_address', models.CharField(blank=True, max_length=64, null=True, verbose_name='IP地址')),
                ('user_agent', models.TextField(blank=True, null=True, verbose_name='User-Agent')),
                ('duration_ms', models.IntegerField(default=0, verbose_name='耗时(毫秒)')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '操作日志',
                'verbose_name_plural': '操作日志',
                'db_table': 'sys_operation_log',
            },
        ),
        migrations.CreateModel(
            name='PasswordResetToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('token', models.CharField(max_length=64, unique=True, verbose_name='重置令牌')),
                ('expires_at', models.DateTimeField(verbose_name='过期时间')),
                ('used_at', models.DateTimeField(blank=True, null=True, verbose_name='使用时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '密码重置令牌',
                'verbose_name_plural': '密码重置令牌',
                'db_table': 'sys_password_reset_token',
            },
        ),
    ]
