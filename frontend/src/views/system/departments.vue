<template>
  <div class="app-container">
    <div class="page-header">
      <h2>部门管理</h2>
      <p>管理组织部门结构与数据权限范围</p>
    </div>

    <el-card class="box-card">
      <div class="filter-container">
        <el-button
          v-permission="'department:add'"
          class="filter-item"
          type="primary"
          icon="el-icon-plus"
          @click="handleCreate"
        >
          添加部门
        </el-button>
      </div>

      <el-table
        v-loading="listLoading"
        :data="list"
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
        <el-table-column label="部门名称" min-width="200">
          <template slot-scope="scope">
            {{ scope.row.name }}
          </template>
        </el-table-column>
        <el-table-column label="上级部门" min-width="200">
          <template slot-scope="scope">
            {{ scope.row.parent_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="排序" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.sort_order }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'info'" size="small">
              {{ scope.row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="220">
          <template slot-scope="scope">
            <el-button
              v-permission="'department:edit'"
              type="primary"
              size="mini"
              @click="handleUpdate(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              v-permission="'department:delete'"
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

    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form ref="deptForm" :model="deptForm" :rules="deptRules" label-width="100px">
        <el-form-item label="部门名称" prop="name">
          <el-input v-model="deptForm.name" placeholder="请输入部门名称" />
        </el-form-item>
        <el-form-item label="上级部门" prop="parent_id">
          <el-select v-model="deptForm.parent_id" clearable placeholder="请选择上级部门">
            <el-option
              v-for="item in parentOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="deptForm.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="deptForm.is_active" active-text="启用" inactive-text="禁用" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="dialogLoading" @click="handleSave">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getDepartments, createDepartment, updateDepartment, deleteDepartment } from '@/api/department'

export default {
  name: 'Departments',
  data() {
    return {
      list: [],
      listLoading: false,
      dialogVisible: false,
      dialogTitle: '添加部门',
      dialogLoading: false,
      isEdit: false,
      deptForm: {
        id: null,
        name: '',
        parent_id: null,
        sort_order: 0,
        is_active: true
      },
      deptRules: {
        name: [{ required: true, message: '请输入部门名称', trigger: 'blur' }]
      },
      parentOptions: []
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      getDepartments().then(res => {
        this.list = res.data
        this.parentOptions = res.data || []
        this.listLoading = false
      }).catch(() => {
        this.listLoading = false
      })
    },
    handleCreate() {
      this.isEdit = false
      this.dialogTitle = '添加部门'
      this.deptForm = {
        id: null,
        name: '',
        parent_id: null,
        sort_order: 0,
        is_active: true
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.deptForm.clearValidate()
      })
    },
    handleUpdate(row) {
      this.isEdit = true
      this.dialogTitle = '编辑部门'
      this.deptForm = {
        id: row.id,
        name: row.name,
        parent_id: row.parent_id || null,
        sort_order: row.sort_order,
        is_active: row.is_active
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.deptForm.clearValidate()
      })
    },
    handleSave() {
      this.$refs.deptForm.validate(valid => {
        if (!valid) return
        this.dialogLoading = true
        const apiCall = this.isEdit
          ? updateDepartment(this.deptForm.id, this.deptForm)
          : createDepartment(this.deptForm)
        apiCall.then(() => {
          this.$message.success(this.isEdit ? '更新成功' : '创建成功')
          this.dialogVisible = false
          this.dialogLoading = false
          this.getList()
        }).catch(() => {
          this.dialogLoading = false
        })
      })
    },
    handleDelete(row) {
      this.$confirm(`确定要删除部门 ${row.name} 吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteDepartment(row.id).then(() => {
          this.$message.success('删除成功')
          this.getList()
        })
      }).catch(() => {})
    }
  }
}
</script>

<style lang="scss" scoped>
.page-header {
  margin-bottom: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
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
</style>
