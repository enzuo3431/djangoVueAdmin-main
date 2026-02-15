<template>
  <div class="app-container">
    <div class="page-header">
      <h2>数据权限规则</h2>
      <p>基于角色配置自定义过滤条件（大众化标准格式）</p>
    </div>

    <el-card class="box-card">
      <div class="filter-container">
        <el-select v-model="listQuery.role_id" placeholder="选择角色" clearable class="filter-item">
          <el-option v-for="role in roleOptions" :key="role.id" :label="role.name" :value="role.id" />
        </el-select>
        <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
          搜索
        </el-button>
        <el-button
          v-permission="'data:rule:add'"
          class="filter-item"
          type="primary"
          icon="el-icon-plus"
          @click="handleCreate"
        >
          添加规则
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
        <el-table-column label="角色" min-width="150">
          <template slot-scope="scope">
            {{ scope.row.role_name }}
          </template>
        </el-table-column>
        <el-table-column label="字段" min-width="140">
          <template slot-scope="scope">
            {{ scope.row.field }}
          </template>
        </el-table-column>
        <el-table-column label="操作符" width="120" align="center">
          <template slot-scope="scope">
            {{ operatorLabel(scope.row.operator) }}
          </template>
        </el-table-column>
        <el-table-column label="值" min-width="200">
          <template slot-scope="scope">
            {{ scope.row.value || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template slot-scope="scope">
            <el-button
              v-permission="'data:rule:edit'"
              type="primary"
              size="mini"
              @click="handleUpdate(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              v-permission="'data:rule:delete'"
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
      width="520px"
      :close-on-click-modal="false"
    >
      <el-form ref="ruleFormRef" :model="ruleForm" :rules="ruleRules" label-width="100px">
        <el-form-item label="角色" prop="role">
          <el-select v-model="ruleForm.role" placeholder="请选择角色">
            <el-option v-for="role in roleOptions" :key="role.id" :label="role.name" :value="role.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="字段" prop="field">
          <el-input v-model="ruleForm.field" placeholder="如：username / department_id" />
        </el-form-item>
        <el-form-item label="操作符" prop="operator">
          <el-select v-model="ruleForm.operator" placeholder="请选择操作符">
            <el-option v-for="op in operatorOptions" :key="op.value" :label="op.label" :value="op.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="值" prop="value">
          <el-input v-model="ruleForm.value" placeholder="如：\"admin\" 或 [1,2,3]" />
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
import { getRoles } from '@/api/user'
import request from '@/utils/request'

export default {
  name: 'DataPermissions',
  data() {
    return {
      list: [],
      listLoading: false,
      listQuery: {
        role_id: ''
      },
      roleOptions: [],
      dialogVisible: false,
      dialogTitle: '添加规则',
      dialogLoading: false,
      ruleForm: {
        id: null,
        role: '',
        field: '',
        operator: 'eq',
        value: ''
      },
      ruleRules: {
        role: [{ required: true, message: '请选择角色', trigger: 'change' }],
        field: [{ required: true, message: '请输入字段名', trigger: 'blur' }],
        operator: [{ required: true, message: '请选择操作符', trigger: 'change' }]
      },
      operatorOptions: [
        { label: '等于', value: 'eq' },
        { label: '不等于', value: 'ne' },
        { label: '小于', value: 'lt' },
        { label: '小于等于', value: 'lte' },
        { label: '大于', value: 'gt' },
        { label: '大于等于', value: 'gte' },
        { label: '包含', value: 'in' },
        { label: '包含文本', value: 'contains' },
        { label: '包含文本(忽略大小写)', value: 'icontains' },
        { label: '前缀匹配', value: 'startswith' },
        { label: '后缀匹配', value: 'endswith' },
        { label: '为空', value: 'isnull' }
      ]
    }
  },
  created() {
    this.fetchRoles()
    this.getList()
  },
  methods: {
    operatorLabel(value) {
      const item = this.operatorOptions.find(op => op.value === value)
      return item ? item.label : value
    },
    fetchRoles() {
      getRoles().then(res => {
        this.roleOptions = res.data || []
      })
    },
    getList() {
      this.listLoading = true
      request({
        url: '/data-rules/',
        method: 'get',
        params: this.listQuery
      }).then(res => {
        this.list = res.data
        this.listLoading = false
      }).catch(() => {
        this.listLoading = false
      })
    },
    handleFilter() {
      this.getList()
    },
    handleCreate() {
      this.dialogTitle = '添加规则'
      this.ruleForm = {
        id: null,
        role: '',
        field: '',
        operator: 'eq',
        value: ''
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.ruleFormRef.clearValidate()
      })
    },
    handleUpdate(row) {
      this.dialogTitle = '编辑规则'
      this.ruleForm = {
        id: row.id,
        role: row.role,
        field: row.field,
        operator: row.operator,
        value: row.value || ''
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.ruleFormRef.clearValidate()
      })
    },
    handleSave() {
      this.$refs.ruleFormRef.validate(valid => {
        if (!valid) return
        this.dialogLoading = true
        const apiCall = this.ruleForm.id
          ? request({ url: `/data-rules/${this.ruleForm.id}/update/`, method: 'put', data: this.ruleForm })
          : request({ url: '/data-rules/create/', method: 'post', data: this.ruleForm })
        apiCall.then(() => {
          this.$message.success(this.ruleForm.id ? '更新成功' : '创建成功')
          this.dialogVisible = false
          this.dialogLoading = false
          this.getList()
        }).catch(() => {
          this.dialogLoading = false
        })
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除该规则吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        request({ url: `/data-rules/${row.id}/delete/`, method: 'delete' }).then(() => {
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
  background: linear-gradient(135deg, #5b86e5 0%, #36d1dc 100%);
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
