<template>
  <div class="app-container">
    <div class="page-header">
      <h2>用户管理</h2>
      <p>管理系统中的所有用户信息 - RBAC权限演示</p>
    </div>

    <el-card class="box-card">
      <!-- 搜索和操作栏 -->
      <div class="filter-container">
        <el-input
          v-model="listQuery.keyword"
          placeholder="搜索用户名或邮箱"
          style="width: 200px;"
          class="filter-item"
          clearable
          @keyup.enter.native="handleFilter"
        />
        <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
          搜索
        </el-button>
        <!-- 使用 v-permission 指令控制按钮显示 -->
        <el-button
          v-permission="'user:add'"
          class="filter-item"
          style="margin-left: 10px;"
          type="primary"
          icon="el-icon-edit"
          @click="handleCreate"
        >
          添加用户
        </el-button>
        <el-button
          v-permission="['user:export', 'system:admin']"
          class="filter-item"
          type="success"
          icon="el-icon-download"
          @click="handleExport"
        >
          导出
        </el-button>
      </div>

      <!-- 用户列表表格 -->
      <el-table
        v-loading="listLoading"
        :data="list"
        element-loading-text="Loading"
        border
        fit
        highlight-current-row
        style="margin-top: 20px;"
      >
        <el-table-column align="center" label="ID" width="80">
          <template slot-scope="scope">
            {{ scope.row.id }}
          </template>
        </el-table-column>
        <el-table-column label="用户名" width="150">
          <template slot-scope="scope">
            {{ scope.row.username }}
          </template>
        </el-table-column>
        <el-table-column label="昵称" width="150">
          <template slot-scope="scope">
            {{ scope.row.nickname || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="角色" width="200">
          <template slot-scope="scope">
            <el-tag
              v-for="(role, index) in scope.row.roles"
              :key="index"
              size="small"
              style="margin-right: 5px;"
              :type="role.code === 'admin' ? 'danger' : 'primary'"
            >
              {{ role.name }}
            </el-tag>
            <span v-if="!scope.row.roles || scope.row.roles.length === 0">-</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'info'" size="small">
              {{ scope.row.is_active ? '激活' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="440">
          <template slot-scope="scope">
            <div class="action-buttons">
            <!-- 权限控制：查看详情 -->
            <el-button
              v-permission="'user:detail'"
              type="info"
              size="mini"
              @click="handleDetail(scope.row)"
            >
              详情
            </el-button>
            <!-- 权限控制：编辑 -->
            <el-button
              v-permission="'user:edit'"
              type="primary"
              size="mini"
              @click="handleUpdate(scope.row)"
            >
              编辑
            </el-button>
            <!-- 权限控制：删除 -->
            <el-button
              v-permission="'user:delete'"
              type="danger"
              size="mini"
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
            <!-- 权限控制：分配角色 -->
            <el-button
              v-permission="'user:assign:role'"
              type="warning"
              size="mini"
              @click="handleAssignRoles(scope.row)"
            >
              角色
            </el-button>
            <el-button
              v-permission="'user:reset:password'"
              type="success"
              size="mini"
              @click="handleResetPassword(scope.row)"
            >
              重置密码
            </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.page_size"
        @pagination="getList"
      />
    </el-card>

    <!-- 添加/编辑用户对话框 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="userForm"
        :model="userForm"
        :rules="userRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" :disabled="isEdit" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input v-model="userForm.password" type="password" placeholder="请输入密码（至少6位）" show-password />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="userForm.nickname" placeholder="请输入昵称" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="userForm.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="部门" prop="department_id">
          <el-select v-model="userForm.department_id" placeholder="请选择部门" clearable>
            <el-option
              v-for="dept in departmentOptions"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="userForm.is_active" active-text="激活" inactive-text="禁用" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="dialogLoading" @click="handleSave">保存</el-button>
      </div>
    </el-dialog>

    <!-- 分配角色对话框 -->
    <el-dialog
      title="分配角色"
      :visible.sync="roleDialogVisible"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-checkbox-group v-model="selectedRoleIds">
        <el-checkbox
          v-for="role in allRoles"
          :key="role.id"
          :label="role.id"
        >
          {{ role.name }}
        </el-checkbox>
      </el-checkbox-group>
      <div slot="footer" class="dialog-footer">
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="roleDialogLoading" @click="handleSaveRoles">保存</el-button>
      </div>
    </el-dialog>

    <!-- 用户详情对话框 -->
    <el-dialog
      title="用户详情"
      :visible.sync="detailDialogVisible"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-descriptions :column="2" border>
        <el-descriptions-item label="用户名">{{ detailUser.username || '-' }}</el-descriptions-item>
        <el-descriptions-item label="昵称">{{ detailUser.nickname || '-' }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ detailUser.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ detailUser.phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="部门">{{ detailUser.department_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="性别">{{ detailUser.gender || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          {{ detailUser.is_active ? '激活' : '禁用' }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detailUser.date_joined | datetime }}</el-descriptions-item>
        <el-descriptions-item label="最后登录">{{ detailUser.last_login | datetime }}</el-descriptions-item>
      </el-descriptions>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { getUsers, getUserDetail, createUser, updateUser, deleteUser, getRoles, assignRoles, resetUserPassword } from '@/api/user'
import { getDepartments } from '@/api/department'

export default {
  name: 'Users',
  components: { Pagination },
  data() {
    return {
      list: [],
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        page_size: 10,
        keyword: ''
      },
      dialogVisible: false,
      dialogTitle: '添加用户',
      dialogLoading: false,
      isEdit: false,
      userForm: {
        id: null,
        username: '',
        password: '',
        nickname: '',
        email: '',
        phone: '',
        department_id: null,
        is_active: true
      },
      userRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 50, message: '长度在 3 到 50 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码不能少于6位', trigger: 'blur' }
        ],
        email: [
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        phone: [
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ]
      },
      roleDialogVisible: false,
      roleDialogLoading: false,
      allRoles: [],
      selectedRoleIds: [],
      currentUserId: null,
      departmentOptions: [],
      detailDialogVisible: false,
      detailUser: {}
    }
  },
  created() {
    this.getList()
    this.fetchRoles()
    this.fetchDepartments()
  },
  methods: {
    getList() {
      this.listLoading = true
      getUsers(this.listQuery).then(response => {
        this.list = response.data.list
        this.total = response.data.total
        this.listLoading = false
      }).catch(() => {
        this.listLoading = false
      })
    },
    fetchRoles() {
      getRoles().then(response => {
        this.allRoles = response.data
      })
    },
    fetchDepartments() {
      getDepartments().then(response => {
        this.departmentOptions = response.data || []
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleCreate() {
      this.isEdit = false
      this.dialogTitle = '添加用户'
      this.userForm = {
        id: null,
        username: '',
        password: '',
        nickname: '',
        email: '',
        phone: '',
        department_id: null,
        is_active: true
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.userForm.clearValidate()
      })
    },
    handleUpdate(row) {
      this.isEdit = true
      this.dialogTitle = '编辑用户'
      this.userForm = {
        id: row.id,
        username: row.username,
        nickname: row.nickname,
        email: row.email,
        phone: row.phone,
        department_id: row.department_id || null,
        is_active: row.is_active
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.userForm.clearValidate()
      })
    },
    handleDetail(row) {
      getUserDetail(row.id).then(res => {
        this.detailUser = res.data
        this.detailDialogVisible = true
      })
    },
    handleSave() {
      this.$refs.userForm.validate(valid => {
        if (valid) {
          this.dialogLoading = true
          const apiCall = this.isEdit
            ? updateUser(this.userForm.id, this.userForm)
            : createUser(this.userForm)

          apiCall.then(() => {
            this.$message({
              type: 'success',
              message: (this.isEdit ? '编辑' : '添加') + '成功!'
            })
            this.dialogVisible = false
            this.dialogLoading = false
            this.getList()
          }).catch(() => {
            this.dialogLoading = false
          })
        }
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除用户 ' + row.username + ' 吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteUser(row.id).then(() => {
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          this.getList()
        })
      }).catch(() => {})
    },
    handleAssignRoles(row) {
      this.currentUserId = row.id
      this.selectedRoleIds = row.roles ? row.roles.map(r => r.id) : []
      this.roleDialogVisible = true
    },
    handleResetPassword(row) {
      this.$confirm(`确定要重置用户 ${row.username} 的密码吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        resetUserPassword(row.id, {}).then(res => {
          const newPwd = res.data.new_password
          this.$alert(`新密码：${newPwd}`, '重置成功', { confirmButtonText: '确定' })
        })
      }).catch(() => {})
    },
    handleSaveRoles() {
      this.roleDialogLoading = true
      assignRoles(this.currentUserId, { role_ids: this.selectedRoleIds }).then(() => {
        this.$message({
          type: 'success',
          message: '角色分配成功!'
        })
        this.roleDialogVisible = false
        this.roleDialogLoading = false
        this.getList()
      }).catch(() => {
        this.roleDialogLoading = false
      })
    },
    handleExport() {
      this.$message.info('导出功能演示 - 权限检查通过')
    }
  }
}
</script>

<style lang="scss" scoped>
.page-header {
  margin-bottom: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  color: #fff;

  h2 {
    margin: 0 0 10px 0;
    font-size: 24px;
  }

  p {
    margin: 0;
    opacity: 0.9;
  }
}

.filter-container {
  padding-bottom: 10px;

  .filter-item {
    display: inline-block;
    vertical-align: middle;
    margin-bottom: 10px;
    margin-right: 10px;
  }
}

.action-buttons {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  flex-wrap: nowrap;
  white-space: nowrap;
}
</style>
