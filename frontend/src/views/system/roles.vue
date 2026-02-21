<template>
  <div class="app-container system-roles-page">
    <div class="page-header">
      <div class="header-left">
        <h2>角色管理</h2>
        <p>管理系统中的所有角色信息 - 分配权限给角色</p>
      </div>
      <div class="header-actions">
        <el-button icon="el-icon-refresh" @click="getList" size="mini">刷新</el-button>
      </div>
    </div>

    <el-card class="box-card">
      <!-- 搜索和操作栏 -->
      <div class="filter-container">
        <el-input
          v-model="listQuery.keyword"
          placeholder="搜索角色名称或代码"
          style="width: 200px;"
          class="filter-item"
          clearable
          @keyup.enter.native="handleFilter"
        />
        <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
          搜索
        </el-button>
        <el-button
          v-permission="'role:add'"
          class="filter-item"
          style="margin-left: 10px;"
          type="primary"
          icon="el-icon-plus"
          @click="handleCreate"
        >
          添加角色
        </el-button>
      </div>

      <!-- 角色列表表格 -->
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
        <el-table-column label="角色名称" width="150">
          <template slot-scope="scope">
            {{ scope.row.name }}
          </template>
        </el-table-column>
        <el-table-column label="角色代码" width="150">
          <template slot-scope="scope">
            <el-tag type="primary" size="small">{{ scope.row.code }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="描述" width="250">
          <template slot-scope="scope">
            {{ scope.row.description || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="权限数量" width="100" align="center">
          <template slot-scope="scope">
            <el-tag type="success" size="small">{{ scope.row.permissions ? scope.row.permissions.length : 0 }} 个</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="180">
          <template slot-scope="scope">
            {{ scope.row.created_at | datetime }}
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="280">
          <template slot-scope="scope">
            <!-- 权限设置 -->
            <el-button
              v-permission="'role:assign:permission'"
              type="warning"
              size="mini"
              @click="handlePermission(scope.row)"
            >
              权限设置
            </el-button>
            <!-- 编辑 -->
            <el-button
              v-permission="'role:edit'"
              type="primary"
              size="mini"
              @click="handleUpdate(scope.row)"
            >
              编辑
            </el-button>
            <!-- 删除 -->
            <el-button
              v-permission="'role:delete'"
              type="danger"
              size="mini"
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑角色对话框 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="roleForm"
        :model="roleForm"
        :rules="roleRules"
        label-width="100px"
      >
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="roleForm.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色代码" prop="code">
          <el-input
            v-model="roleForm.code"
            placeholder="请输入角色代码（英文）"
            :disabled="isEdit"
          />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="roleForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入角色描述"
          />
        </el-form-item>
        <el-form-item label="数据权限" prop="data_scope">
          <el-select v-model="roleForm.data_scope" placeholder="请选择数据权限范围">
            <el-option label="全部数据" value="all" />
            <el-option label="本部门数据" value="dept" />
            <el-option label="本部门及下级" value="dept_and_child" />
            <el-option label="仅本人" value="self" />
            <el-option label="自定义部门" value="custom" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="roleForm.data_scope === 'custom'" label="自定义部门">
          <el-select v-model="roleForm.department_ids" multiple placeholder="请选择部门">
            <el-option
              v-for="dept in departmentOptions"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="dialogLoading" @click="handleSave">保存</el-button>
      </div>
    </el-dialog>

    <!-- 权限设置对话框 -->
    <el-dialog
      title="权限设置"
      :visible.sync="permissionDialogVisible"
      width="1400px"
      :close-on-click-modal="false"
    >
      <div class="permission-dialog">
        <div class="role-info">
          <span>角色：<strong>{{ currentRole ? currentRole.name : '' }}</strong></span>
          <span>代码：<el-tag type="info" size="mini">{{ currentRole ? currentRole.code : '' }}</el-tag></span>
        </div>
        <el-divider />
        <el-transfer
          v-model="targetPermissions"
          :data="allPermissions"
          :props="{
            key: 'id',
            label: 'name'
          }"
          :titles="['可选权限', '已选权限']"
          filterable
          filter-placeholder="搜索权限"
          class="permission-transfer"
        >
          <span slot-scope="{ option }">{{ option.name }}</span>
        </el-transfer>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="permissionDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="permissionDialogLoading" @click="handleSavePermissions">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getRoles, createRole, updateRole, deleteRole, getAllPermissions, assignPermissions } from '@/api/user'
import { getDepartments } from '@/api/department'

export default {
  name: 'Roles',
  data() {
    return {
      list: [],
      listLoading: true,
      listQuery: {
        keyword: ''
      },
      dialogVisible: false,
      dialogTitle: '添加角色',
      dialogLoading: false,
      isEdit: false,
      roleForm: {
        id: null,
        name: '',
        code: '',
        description: '',
        data_scope: 'all',
        department_ids: []
      },
      roleRules: {
        name: [
          { required: true, message: '请输入角色名称', trigger: 'blur' }
        ],
        code: [
          { required: true, message: '请输入角色代码', trigger: 'blur' },
          { pattern: /^[a-z]+$/, message: '角色代码只能包含小写英文字母', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入角色描述', trigger: 'blur' }
        ]
      },
      permissionDialogVisible: false,
      permissionDialogLoading: false,
      currentRole: null,
      allPermissions: [],
      targetPermissions: [],
      departmentOptions: []
    }
  },
  created() {
    this.getList()
    this.fetchAllPermissions()
    this.fetchDepartments()
  },
  methods: {
    getList() {
      this.listLoading = true
      getRoles().then(response => {
        this.list = response.data
        this.listLoading = false
      }).catch(() => {
        this.listLoading = false
      })
    },
    fetchAllPermissions() {
      getAllPermissions().then(response => {
        this.allPermissions = response.data.map(p => ({
          id: p.id,
          name: `${p.name} (${p.code})`,
          code: p.code
        }))
      })
    },
    fetchDepartments() {
      getDepartments().then(response => {
        this.departmentOptions = response.data || []
      })
    },
    handleFilter() {
      this.getList()
    },
    handleCreate() {
      this.isEdit = false
      this.dialogTitle = '添加角色'
      this.roleForm = {
        id: null,
        name: '',
        code: '',
        description: '',
        data_scope: 'all',
        department_ids: []
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.roleForm.clearValidate()
      })
    },
    handleUpdate(row) {
      this.isEdit = true
      this.dialogTitle = '编辑角色'
      this.roleForm = {
        id: row.id,
        name: row.name,
        code: row.code,
        description: row.description,
        data_scope: row.data_scope || 'all',
        department_ids: row.departments ? row.departments.map(d => d.id) : []
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.roleForm.clearValidate()
      })
    },
    handleSave() {
      this.$refs.roleForm.validate(valid => {
        if (valid) {
          this.dialogLoading = true
          const apiCall = this.isEdit
            ? updateRole(this.roleForm.id, this.roleForm)
            : createRole(this.roleForm)

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
      this.$confirm('确定要删除角色 ' + row.name + ' 吗？删除后该角色的用户将失去相应权限。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteRole(row.id).then(() => {
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          this.getList()
        })
      }).catch(() => {})
    },
    handlePermission(row) {
      this.currentRole = row
      // 设置已选中的权限
      this.targetPermissions = row.permissions ? row.permissions.map(p => p.id) : []
      this.permissionDialogVisible = true
    },
    handleSavePermissions() {
      this.permissionDialogLoading = true
      assignPermissions(this.currentRole.id, { permission_ids: this.targetPermissions }).then(() => {
        this.$message({
          type: 'success',
          message: '权限设置成功!'
        })
        this.permissionDialogVisible = false
        this.permissionDialogLoading = false
        this.getList()
      }).catch(() => {
        this.permissionDialogLoading = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px 24px;
  background:
    radial-gradient(1200px 400px at 10% -10%, rgba(125, 143, 255, 0.18), transparent 50%),
    radial-gradient(900px 300px at 90% -10%, rgba(0, 201, 255, 0.18), transparent 50%);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 18px 20px;
  background: linear-gradient(135deg, #1f2a44 0%, #2d3a66 100%);
  border-radius: 14px;
  color: #fff;
  box-shadow: 0 12px 30px rgba(31, 42, 68, 0.2);

  h2 {
    margin: 0;
    font-size: 22px;
    letter-spacing: 0.5px;
  }

  p {
    margin: 6px 0 0 0;
    opacity: 0.8;
    font-size: 13px;
  }
}

.header-left {
  display: flex;
  flex-direction: column;
}

.header-actions {
  display: flex;
  gap: 8px;
  align-items: center;
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

.permission-dialog {
  .role-info {
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 15px;

    span {
      font-size: 14px;
    }
  }

  ::v-deep .el-divider {
    margin: 10px 0 20px 0;
  }
}

.dialog-footer {
  text-align: right;
}

// 穿梭框列宽样式
.permission-transfer {
  ::v-deep .el-transfer-panel {
    width: 45%;
  }

  ::v-deep .el-transfer__buttons {
    width: 10%;
  }

  ::v-deep .el-transfer__item {
    width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  ::v-deep .el-transfer__item + .el-checkbox__label {
    font-size: 13px;
  }
}
</style>
