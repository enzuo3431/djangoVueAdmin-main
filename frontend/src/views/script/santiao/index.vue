<template>
  <div class="app-container santiao-page script-santiao-page">
    <div class="page-header">
      <h2>三条配置</h2>
      <p>脚本相关的三条配置管理页面</p>
    </div>

    <el-card class="form-card">
      <div slot="header" class="card-title">
        <div class="card-actions">
          <div class="user-id-badge">
            <span class="badge-prefix">用户ID:</span>
            <span class="badge-value">{{ quickForm.userId }}</span>
          </div>
        </div>
      </div>
      <el-form
        ref="quickFormRef"
        :model="quickForm"
        :rules="quickRules"
        label-width="80px"
        class="santiao-form"
        v-loading="quickLoading"
      >
        <div class="form-section">
          <div class="section-title">基础信息</div>
          <div class="section-grid grid-5">
            <el-form-item label="IP地址" prop="ipAddress" class="field-narrow">
              <el-input v-model="quickForm.ipAddress" placeholder="请输入IP地址" />
            </el-form-item>
            <el-form-item label="定义名称" prop="name" class="field-narrow">
              <el-input v-model="quickForm.name" placeholder="请输入名称" />
            </el-form-item>
          </div>
        </div>

        <div class="form-section">
          <div class="section-title">功能开关</div>
          <div class="section-grid grid-5">
            <el-form-item label="是否加好友">
              <el-switch v-model="quickForm.isOpenAddFriend" />
            </el-form-item>
            <el-form-item label="是否搜索">
              <el-switch v-model="quickForm.isOpenSearchAddFriend" />
            </el-form-item>
            <el-form-item label="是否通讯录">
              <el-switch v-model="quickForm.isOpenBookAddFriend" />
            </el-form-item>
            <el-form-item label="是否发媒体">
              <el-switch v-model="quickForm.isOpenSendFile" />
            </el-form-item>
            <el-form-item label="监听消息">
              <el-switch v-model="quickForm.isOpenMsgReply" />
            </el-form-item>
          </div>
        </div>

        <div class="form-section">
          <div class="section-title">参数与时间</div>
          <div class="section-grid grid-5">
            <el-form-item label="添加数量">
              <el-input-number v-model="quickForm.addNumber" :min="1" :max="100" :step="1" controls-position="right" />
            </el-form-item>
            <el-form-item label="消息间隔/s">
              <el-input-number v-model="quickForm.delayTime" :min="1" :max="3600" :step="1" controls-position="right" />
            </el-form-item>
            <el-form-item label="好友间隔/s">
              <el-input-number v-model="quickForm.timeIntervalAdd" :min="10" :max="7200" :step="1" controls-position="right" />
            </el-form-item>
            <el-form-item label="开始时间" class="field-narrow">
              <el-time-picker v-model="quickForm.startTime" placeholder="开始时间" value-format="HH:mm" format="HH:mm" @change="handleStartTimeChange" />
            </el-form-item>
            <el-form-item label="结束时间" prop="endTime" class="field-narrow">
              <el-time-picker v-model="quickForm.endTime" placeholder="结束时间" value-format="HH:mm" format="HH:mm" />
            </el-form-item>
          </div>
        </div>

        <div class="form-section">
          <div class="section-title">内容配置</div>
          <div class="section-grid grid-2">
            <el-form-item label="加入话术">
              <el-input
                v-model="quickForm.replyContent"
                type="textarea"
                :rows="4"
                placeholder="请输入内容"
              />
            </el-form-item>
            <el-form-item label="发送内容">
              <el-input
                v-model="quickForm.addPeopleContent"
                type="textarea"
                :rows="4"
                placeholder="请输入内容"
              />
            </el-form-item>
          </div>
        </div>

        <div class="form-actions">
          <el-button type="primary" :loading="submitLoading" @click="handleQuickSubmit">立即提交</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { getScriptConfigs, createScriptConfig, updateScriptConfig } from '@/api/script'
import { mapGetters } from 'vuex'

export default {
  name: 'ScriptSantiao',
  data() {
    const validateEndTime = (rule, value, callback) => {
      if (!value || !this.quickForm.startTime) {
        callback()
        return
      }
      const start = this.timeToMinutes(this.quickForm.startTime)
      const end = this.timeToMinutes(value)
      if (end <= start) {
        callback(new Error('结束时间必须晚于开始时间'))
      } else {
        callback()
      }
    }
    return {
      quickForm: this.buildEmptyForm(),
      quickLoading: false,
      submitLoading: false,
      configId: null,
      quickRules: {
        name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
        userId: [{ required: true, message: '请输入用户ID', trigger: 'blur' }],
        ipAddress: [{ required: true, message: '请输入IP地址', trigger: 'blur' }],
        endTime: [{ validator: validateEndTime, trigger: 'change' }]
      }
    }
  },
  computed: {
    ...mapGetters(['userId'])
  },
  created() {
    this.initConfig()
  },
  methods: {
    buildEmptyForm() {
      return {
        id: null,
        createBy: '',
        updateBy: '',
        remark: 'remark',
        ipAddress: '127.0.0.1',
        userId: this.userId || 0,
        name: 'DDPP',
        isOpenAddFriend: false,
        isOpenSearchAddFriend: false,
        isOpenBookAddFriend: false,
        isOpenSendFile: false,
        addNumber: 1,
        openSendFileIndex: 1,
        delayTime: 1,
        timeIntervalAdd: 10,
        replyContent: '',
        configType: 'santiao',
        addPeopleContent: '',
        startTime: '00:00',
        endTime: '23:59',
        isOpenMsgReply: false,
        status: false
      }
    },
    initConfig() {
      if (!this.userId) {
        this.$store.dispatch('user/getInfo').then(() => {
          if (!this.userId) {
            this.$message.error('无法获取用户ID')
            return
          }
          this.quickForm.userId = this.userId
          this.fetchOrCreateConfig()
        }).catch(() => {
          this.$message.error('无法获取用户信息')
        })
        return
      }
      this.fetchOrCreateConfig()
    },
    fetchOrCreateConfig() {
      if (!this.userId) {
        this.$message.error('无法获取用户ID')
        return
      }
      this.quickLoading = true
      const params = {
        config_type: 'santiao'
      }
      getScriptConfigs(params).then(res => {
        const current = res.data
        if (current) {
          this.configId = current.id
          this.quickForm = {
            ...this.buildEmptyForm(),
            ...current,
            startTime: this.normalizeTime(current.startTime || '00:00'),
            endTime: this.normalizeTime(current.endTime || '23:59')
          }
        } else {
          const payload = { ...this.buildEmptyForm(), userId: this.userId }
          createScriptConfig(payload).then(createRes => {
            this.configId = createRes.data.id
            this.quickForm = {
              ...this.buildEmptyForm(),
              ...createRes.data,
              startTime: this.normalizeTime(createRes.data.startTime || '00:00'),
              endTime: this.normalizeTime(createRes.data.endTime || '23:59')
            }
          }).catch(() => {
            this.$message.error('初始化配置失败')
          })
        }
        this.quickLoading = false
      }).catch(() => {
        this.quickLoading = false
      })
    },
    timeToMinutes(timeStr) {
      const [h, m] = timeStr.split(':').map(v => parseInt(v, 10))
      return h * 60 + m
    },
    normalizeTime(value) {
      if (!value) return ''
      const parts = value.split(':')
      return parts.length >= 2 ? `${parts[0].padStart(2, '0')}:${parts[1].padStart(2, '0')}` : value
    },
    handleQuickSubmit() {
      this.$refs.quickFormRef.validate(valid => {
        if (!valid) return
        this.submitLoading = true
        const payload = { ...this.quickForm, configType: 'santiao', userId: this.userId }
        const request = this.configId
          ? updateScriptConfig(this.configId, payload)
          : createScriptConfig(payload)
        request.then(res => {
          this.$message.success('提交成功')
          if (res.data && res.data.id) {
            this.configId = res.data.id
          }
          this.submitLoading = false
        }).catch(() => {
          this.submitLoading = false
        })
      })
    },
    handleQuickReset() {
      this.quickForm = { ...this.buildEmptyForm(), userId: this.userId }
      this.$nextTick(() => {
        this.$refs.quickFormRef && this.$refs.quickFormRef.clearValidate()
      })
    },
    handleStartTimeChange() {
      if (this.$refs.quickFormRef) {
        this.$refs.quickFormRef.validateField('endTime')
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.app-container {
  min-height: calc(100vh - 90px);
  background: var(--app-bg);
}

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

.form-card {
  margin-top: 20px;
  border-radius: 8px;
}

.santiao-form {
  padding: 6px 6px 4px;
}

.form-section {
  padding: 12px 12px 6px;
  border: 1px solid var(--border-light);
  border-radius: 8px;
  margin-bottom: 14px;
}

.section-title {
  font-size: 13px;
  font-weight: 700;
  color: #1f2a44;
  margin-bottom: 10px;
  letter-spacing: 0.6px;
  text-transform: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.section-title::before {
  content: '';
  width: 6px;
  height: 12px;
  border-radius: 3px;
  background: linear-gradient(180deg, #4c6ef5 0%, #9b6bff 100%);
}

.section-grid {
  display: grid;
  gap: 12px;
}

.grid-3 {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.grid-2 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.grid-5 {
  grid-template-columns: repeat(5, minmax(0, 1fr));
}

.section-grid ::v-deep .el-form-item__label {
  white-space: nowrap;
}

.section-grid ::v-deep .el-form-item__content {
  min-width: 0;
}

.section-grid ::v-deep .el-input__inner,
.section-grid ::v-deep .el-input-number__inner,
.section-grid ::v-deep .el-time-editor {
  white-space: nowrap;
}

.field-narrow ::v-deep .el-input__inner,
.field-narrow ::v-deep .el-time-editor {
  max-width: 180px;
}

@media (max-width: 1200px) {
  .field-narrow ::v-deep .el-input__inner,
  .field-narrow ::v-deep .el-time-editor {
    max-width: 100%;
  }
}

.grid-5 ::v-deep .el-form-item__label {
  width: 90px !important;
}

.grid-5 ::v-deep .el-form-item__content {
  margin-left: 90px !important;
}

.grid-5 ::v-deep .el-switch__core {
  border-color: #dcdfe6;
}

.grid-5 ::v-deep .el-switch.is-checked .el-switch__core {
  border-color: #13ce66;
  background-color: #13ce66;
}

.form-actions {
  margin-top: 12px;
  padding-left: 80px;
}

::v-deep .el-form-item__label {
  color: #6b7280;
  font-weight: 500;
  letter-spacing: 0.1px;
}

::v-deep .el-form-item {
  margin-bottom: 8px;
}

::v-deep .el-switch__label {
  font-size: 12px;
}

::v-deep .el-input__inner,
::v-deep .el-textarea__inner,
::v-deep .el-input-number__inner {
  border-radius: 8px;
  background: #fbfcff;
  border-color: #e4e7ed;
}

::v-deep .el-input__inner:focus,
::v-deep .el-textarea__inner:focus,
::v-deep .el-input-number__inner:focus {
  border-color: #4c6ef5;
  box-shadow: 0 0 0 3px rgba(76, 110, 245, 0.12);
}

::v-deep .el-textarea__inner {
  resize: none;
}

::v-deep .el-input-number__decrease,
::v-deep .el-input-number__increase {
  border-color: #e4e7ed;
}

:global(body.theme-dark:not([data-theme='black-gold'])) ::v-deep .el-form-item__label {
  color: rgba(255, 255, 255, 0.6);
}


:global(body.theme-dark:not([data-theme='black-gold'])) .section-title::before {
  background: linear-gradient(180deg, #9db0ff 0%, #6b8dff 100%);
}

:global(body.theme-dark:not([data-theme='black-gold'])) ::v-deep .el-input__inner,
:global(body.theme-dark:not([data-theme='black-gold'])) ::v-deep .el-textarea__inner,
:global(body.theme-dark:not([data-theme='black-gold'])) ::v-deep .el-input-number__inner {
  background: rgba(23, 28, 44, 0.9);
  border-color: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.9);
}

:global(body.theme-dark:not([data-theme='black-gold'])) ::v-deep .el-input__inner:focus,
:global(body.theme-dark:not([data-theme='black-gold'])) ::v-deep .el-textarea__inner:focus,
:global(body.theme-dark:not([data-theme='black-gold'])) ::v-deep .el-input-number__inner:focus {
  border-color: rgba(79, 99, 255, 0.8);
  box-shadow: 0 0 0 3px rgba(79, 99, 255, 0.25);
}

:global(body.theme-dark:not([data-theme='black-gold'])) ::v-deep .el-input-number__decrease,
:global(body.theme-dark:not([data-theme='black-gold'])) ::v-deep .el-input-number__increase {
  border-color: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.7);
}

::v-deep .el-input__inner,
::v-deep .el-textarea__inner,
::v-deep .el-input-number__inner,
::v-deep .el-time-panel {
  border-radius: 2px;
}

@media (max-width: 1200px) {
  .grid-3 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .grid-2 {
    grid-template-columns: 1fr;
  }
  .grid-5 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  .form-actions {
    padding-left: 0;
  }
}

@media (max-width: 900px) {
  .grid-3 {
    grid-template-columns: 1fr;
  }
  .grid-5 {
    grid-template-columns: 1fr;
  }
  .grid-2 {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 1400px) {
  .grid-5 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 1100px) {
  .grid-5 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

.user-id-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 18px;
  background: #f0f5ff;
  border: 1px solid #d6e4ff;
}

.user-id-badge::before {
  content: '';
  width: 6px;
  height: 22px;
  border-radius: 3px;
  background: #13ce66;
}

.badge-value {
  font-size: 16px;
  color: #1f2a44;
  font-weight: 700;
  letter-spacing: 0.4px;
}

.badge-prefix {
  font-size: 13px;
  color: #4c6ef5;
  font-weight: 600;
}

.card-title {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

:global(body.theme-dark:not([data-theme='black-gold'])) .user-id-badge {
  background: rgba(79, 99, 255, 0.18);
  border-color: rgba(79, 99, 255, 0.35);
}

:global(body.theme-dark:not([data-theme='black-gold'])) .user-id-badge::before {
  background: #26d17a;
}

:global(body.theme-dark:not([data-theme='black-gold'])) .badge-value {
  color: rgba(255, 255, 255, 0.9);
}

:global(body.theme-dark:not([data-theme='black-gold'])) .badge-prefix {
  color: #9db0ff;
}
</style>
