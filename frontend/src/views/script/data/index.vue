<template>
  <div class="app-container script-data-page">
    <div class="page-header">
      <h2>脚本数据</h2>
      <p>管理手机号队列与数据上传</p>
    </div>

    <el-card class="box-card script-data-card">
      <div class="create-row">
        <el-form ref="createFormRef" :model="createForm" :rules="createRules" inline>
          <el-form-item label="队列名称" prop="name">
            <el-input v-model="createForm.name" placeholder="英文或下划线" />
          </el-form-item>
          <el-form-item label="备注" prop="remark">
            <el-input v-model="createForm.remark" placeholder="可选" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="createLoading" @click="handleCreate">创建队列</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table
        :data="queues"
        v-loading="listLoading"
        border
        class="script-data-table"
        style="margin-top: 16px;"
      >
        <el-table-column label="队列名称" prop="name" min-width="180" />
        <el-table-column label="备注" prop="remark" min-width="220" />
        <el-table-column label="数量" prop="count" width="120" align="center" />
        <el-table-column label="创建时间" width="180">
          <template slot-scope="scope">
            {{ scope.row.created_at | datetime }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="openUpload(scope.row)">上传</el-button>
            <el-button size="mini" @click="handleClear(scope.row)">清空</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      :title="`上传数据 - ${currentQueue?.name || ''}`"
      :visible.sync="uploadVisible"
      width="520px"
      :close-on-click-modal="false"
    >
      <el-form label-width="90px">
        <el-form-item label="上传方式">
          <el-radio-group v-model="uploadMode">
            <el-radio label="append">追加</el-radio>
            <el-radio label="overwrite">覆盖</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="TXT文件">
          <el-upload
            ref="uploadRef"
            drag
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            accept=".txt"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖拽到此处，或点击选择</div>
            <div slot="tip" class="el-upload__tip">仅支持 TXT，一行一个手机号</div>
          </el-upload>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="uploadVisible = false">取消</el-button>
        <el-button type="primary" :loading="uploadLoading" @click="handleUpload">开始上传</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  getScriptQueues,
  createScriptQueue,
  clearScriptQueue,
  deleteScriptQueue,
  uploadScriptQueue
} from '@/api/script'

export default {
  name: 'ScriptData',
  data() {
    const namePattern = /^[A-Za-z_]+$/
    const validateName = (rule, value, callback) => {
      if (!value || !namePattern.test(value)) {
        callback(new Error('仅支持英文或下划线'))
      } else {
        callback()
      }
    }
    return {
      queues: [],
      listLoading: false,
      createLoading: false,
      createForm: {
        name: '',
        remark: ''
      },
      createRules: {
        name: [{ required: true, validator: validateName, trigger: 'blur' }]
      },
      uploadVisible: false,
      uploadMode: 'append',
      uploadLoading: false,
      currentQueue: null,
      currentFile: null
    }
  },
  created() {
    this.fetchQueues()
  },
  methods: {
    fetchQueues() {
      this.listLoading = true
      getScriptQueues().then(res => {
        this.queues = res.data || []
        this.listLoading = false
      }).catch(() => {
        this.listLoading = false
      })
    },
    handleCreate() {
      this.$refs.createFormRef.validate(valid => {
        if (!valid) return
        this.createLoading = true
        createScriptQueue(this.createForm).then(() => {
          this.$message.success('创建成功')
          this.createForm = { name: '', remark: '' }
          this.fetchQueues()
          this.createLoading = false
        }).catch(() => {
          this.createLoading = false
        })
      })
    },
    handleClear(row) {
      this.$confirm(`确认清空队列 ${row.name} 吗？`, '提示', {
        type: 'warning'
      }).then(() => {
        clearScriptQueue(row.id).then(() => {
          this.$message.success('清空成功')
          this.fetchQueues()
        })
      }).catch(() => {})
    },
    handleDelete(row) {
      this.$confirm(`确认删除队列 ${row.name} 吗？`, '提示', {
        type: 'warning'
      }).then(() => {
        deleteScriptQueue(row.id).then(() => {
          this.$message.success('删除成功')
          this.fetchQueues()
        })
      }).catch(() => {})
    },
    openUpload(row) {
      this.currentQueue = row
      this.uploadMode = 'append'
      this.currentFile = null
      this.uploadVisible = true
      if (this.$refs.uploadRef) {
        this.$refs.uploadRef.clearFiles()
      }
    },
    handleFileChange(file) {
      this.currentFile = file.raw
    },
    handleFileRemove() {
      this.currentFile = null
    },
    handleUpload() {
      if (!this.currentQueue) return
      if (!this.currentFile) {
        this.$message.warning('请选择TXT文件')
        return
      }
      this.uploadLoading = true
      const formData = new FormData()
      formData.append('file', this.currentFile)
      formData.append('mode', this.uploadMode)
      uploadScriptQueue(this.currentQueue.id, formData).then(() => {
        this.$message.success('上传成功')
        this.uploadVisible = false
        this.fetchQueues()
        this.uploadLoading = false
      }).catch(() => {
        this.uploadLoading = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.page-header {
  margin-bottom: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #4facfe 0%, #00c6ff 100%);
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

.create-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.script-data-table ::v-deep .el-table td .cell,
.script-data-table ::v-deep .el-table th .cell {
  padding: 5px 10px;
  font-size: 14px;
  line-height: 1;
}

.script-data-page ::v-deep .script-data-table.el-table--small {
  font-size: 14px;
}

.script-data-page ::v-deep .script-data-table.el-table--small .cell {
  font-size: 14px;
  line-height: 1;
}

.script-data-table ::v-deep .el-table__row {
  height: 52px;
}

</style>
