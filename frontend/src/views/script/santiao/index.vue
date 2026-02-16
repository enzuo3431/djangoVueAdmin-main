<template>
  <div class="app-container">
    <div class="page-header">
      <h2>三条配置</h2>
      <p>脚本相关的三条配置管理页面</p>
    </div>

    <el-card class="box-card">
      <div class="filter-container">
        <el-input
          v-model="listQuery.keyword"
          placeholder="搜索设备类型或IP"
          style="width: 220px;"
          class="filter-item"
          clearable
          @keyup.enter.native="handleFilter"
        />
        <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
          搜索
        </el-button>
        <el-button
          v-permission="'script:config:add'"
          class="filter-item"
          type="primary"
          icon="el-icon-plus"
          @click="handleCreate"
        >
          新建配置
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
        <el-table-column label="ID" width="80" align="center">
          <template slot-scope="scope">
            {{ scope.row.id }}
          </template>
        </el-table-column>
        <el-table-column label="设备类型" min-width="140">
          <template slot-scope="scope">
            {{ scope.row.name }}
          </template>
        </el-table-column>
        <el-table-column label="用户ID" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.userId }}
          </template>
        </el-table-column>
        <el-table-column label="IP地址" min-width="140">
          <template slot-scope="scope">
            {{ scope.row.ipAddress }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status ? 'success' : 'info'" size="small">
              {{ scope.row.status ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="更新时间" width="180">
          <template slot-scope="scope">
            {{ scope.row.updated_at | datetime }}
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="200">
          <template slot-scope="scope">
            <el-button
              v-permission="'script:config:edit'"
              type="primary"
              size="mini"
              @click="handleUpdate(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              v-permission="'script:config:delete'"
              type="danger"
              size="mini"
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.page_size"
        @pagination="getList"
      />
    </el-card>

    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="760px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="configForm"
        :model="configForm"
        :rules="configRules"
        label-width="160px"
      >
        <el-form-item label="设备类型" prop="name">
          <el-input v-model="configForm.name" placeholder="请输入设备类型" />
        </el-form-item>
        <el-form-item label="用户ID" prop="userId">
          <el-input-number v-model="configForm.userId" :min="0" :step="1" />
        </el-form-item>
        <el-form-item label="IP地址" prop="ipAddress">
          <el-input v-model="configForm.ipAddress" placeholder="请输入IP地址" />
        </el-form-item>
        <el-form-item label="评论" prop="remark">
          <el-input v-model="configForm.remark" placeholder="请输入评论" />
        </el-form-item>
        <el-form-item label="是否开启添加好友">
          <el-switch v-model="configForm.isOpenAddFriend" />
        </el-form-item>
        <el-form-item label="是否开启搜索好友">
          <el-switch v-model="configForm.isOpenSearchAddFriend" />
        </el-form-item>
        <el-form-item label="是否开启通讯录加好友">
          <el-switch v-model="configForm.isOpenBookAddFriend" />
        </el-form-item>
        <el-form-item label="是否开启发送文件">
          <el-switch v-model="configForm.isOpenSendFile" />
        </el-form-item>
        <el-form-item label="添加好友数量">
          <el-input-number v-model="configForm.addNumber" :min="1" :step="1" />
        </el-form-item>
        <el-form-item label="发送文件索引">
          <el-input-number v-model="configForm.openSendFileIndex" :min="1" :step="1" />
        </el-form-item>
        <el-form-item label="发消息间隔/s">
          <el-input-number v-model="configForm.delayTime" :min="1" :step="1" />
        </el-form-item>
        <el-form-item label="添加好友间隔/s">
          <el-input-number v-model="configForm.timeIntervalAdd" :min="1" :step="1" />
        </el-form-item>
        <el-form-item label="加好友话术" prop="replyContent">
          <el-input v-model="configForm.replyContent" placeholder="请输入话术" />
        </el-form-item>
        <el-form-item label="发消息内容">
          <el-input
            v-model="configForm.addPeopleContent"
            type="textarea"
            :rows="3"
            placeholder="请输入发消息内容"
          />
        </el-form-item>
        <el-form-item label="定时启动时间">
          <el-input v-model="configForm.startTime" placeholder="例如 08:00" />
        </el-form-item>
        <el-form-item label="定时结束时间">
          <el-input v-model="configForm.endTime" placeholder="例如 20:00" />
        </el-form-item>
        <el-form-item label="是否开启消息回复">
          <el-switch v-model="configForm.isOpenMsgReply" />
        </el-form-item>
        <el-form-item label="脚本状态">
          <el-switch v-model="configForm.status" active-text="启用" inactive-text="停用" />
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
import Pagination from '@/components/Pagination'
import { getScriptConfigs, createScriptConfig, updateScriptConfig, deleteScriptConfig } from '@/api/script'

export default {
  name: 'ScriptSantiao',
  components: { Pagination },
  data() {
    return {
      list: [],
      total: 0,
      listLoading: false,
      listQuery: {
        page: 1,
        page_size: 10,
        keyword: '',
        config_type: 'santiao'
      },
      dialogVisible: false,
      dialogTitle: '新建配置',
      dialogLoading: false,
      isEdit: false,
      configForm: this.buildEmptyForm(),
      configRules: {
        name: [{ required: true, message: '请输入设备类型', trigger: 'blur' }],
        userId: [{ required: true, message: '请输入用户ID', trigger: 'blur' }],
        ipAddress: [{ required: true, message: '请输入IP地址', trigger: 'blur' }]
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    buildEmptyForm() {
      return {
        id: null,
        createBy: '',
        updateBy: '',
        remark: 'remark',
        ipAddress: '',
        userId: 0,
        name: '',
        isOpenAddFriend: false,
        isOpenSearchAddFriend: false,
        isOpenBookAddFriend: false,
        isOpenSendFile: false,
        addNumber: 1,
        openSendFileIndex: 1,
        delayTime: 1,
        timeIntervalAdd: 5,
        replyContent: '',
        configType: 'santiao',
        addPeopleContent: '',
        startTime: '',
        endTime: '',
        isOpenMsgReply: false,
        status: false
      }
    },
    getList() {
      this.listLoading = true
      getScriptConfigs(this.listQuery).then(res => {
        this.list = res.data.list
        this.total = res.data.total
        this.listLoading = false
      }).catch(() => {
        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleCreate() {
      this.isEdit = false
      this.dialogTitle = '新建配置'
      this.configForm = this.buildEmptyForm()
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.configForm.clearValidate()
      })
    },
    handleUpdate(row) {
      this.isEdit = true
      this.dialogTitle = '编辑配置'
      this.configForm = { ...row }
      if (!this.configForm.configType) {
        this.configForm.configType = 'santiao'
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.configForm.clearValidate()
      })
    },
    handleSave() {
      this.$refs.configForm.validate(valid => {
        if (!valid) return
        this.dialogLoading = true
        const payload = { ...this.configForm, configType: 'santiao' }
        const request = this.isEdit
          ? updateScriptConfig(this.configForm.id, payload)
          : createScriptConfig(payload)
        request.then(() => {
          this.$message.success((this.isEdit ? '编辑' : '新建') + '成功')
          this.dialogVisible = false
          this.dialogLoading = false
          this.getList()
        }).catch(() => {
          this.dialogLoading = false
        })
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除该配置吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteScriptConfig(row.id).then(() => {
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
  background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
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

.empty-tip {
  color: #909399;
  padding: 20px 10px;
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
