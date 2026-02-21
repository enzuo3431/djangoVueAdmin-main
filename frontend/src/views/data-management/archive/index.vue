<template>
  <div class="app-container archive-page">
    <div class="page-header">
      <div class="header-copy">
        <h2>归档数据</h2>
        <p>按 dataConsole 归档号码数据能力提供检索与维护</p>
      </div>
      <div class="header-badges">
        <span class="badge-chip">总量 {{ total }}</span>
        <span class="badge-chip">平台 {{ platformMeta.length }}</span>
        <span class="badge-chip">分页 {{ listQuery.page }}/{{ Math.max(1, Math.ceil((total || 0) / (listQuery.limit || 10))) }}</span>
      </div>
    </div>

    <el-card class="box-card archive-shell" shadow="never">
      <div class="filter-container toolbar">
        <el-input
          v-model="listQuery.phone"
          placeholder="手机号精确查询"
          class="filter-item"
          style="width: 180px;"
          clearable
          @keyup.enter.native="handleFilter"
        />
        <el-input
          v-model="listQuery.remark"
          placeholder="备注模糊查询"
          class="filter-item"
          style="width: 200px;"
          clearable
          @keyup.enter.native="handleFilter"
        />
        <el-input
          v-model="listQuery.source"
          placeholder="来源"
          class="filter-item"
          style="width: 140px;"
          clearable
          @keyup.enter.native="handleFilter"
        />
        <el-select
          v-model="listQuery.is_filtered"
          class="filter-item archive-dark-select"
          popper-class="archive-filter-popper"
          placeholder="过滤状态"
          clearable
          style="width: 120px;"
        >
          <el-option label="命中过滤" value="1" />
          <el-option label="未命中过滤" value="0" />
        </el-select>
        <el-select
          v-model="listQuery.platforms"
          class="filter-item archive-dark-select"
          popper-class="archive-filter-popper"
          multiple
          collapse-tags
          clearable
          placeholder="平台"
          style="width: 220px;"
        >
          <el-option
            v-for="item in platformMeta"
            :key="item.code"
            :label="item.label"
            :value="item.code"
          />
        </el-select>
        <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">搜索</el-button>
        <el-button class="filter-item" type="success" icon="el-icon-plus" @click="openCreate">新增</el-button>
        <el-button class="filter-item" type="warning" icon="el-icon-upload2" @click="openImport">批量导入</el-button>
        <el-button class="filter-item" type="info" icon="el-icon-refresh" :loading="syncLoading" @click="handleSync">队列同步</el-button>
      </div>

      <el-table
        v-loading="listLoading"
        :data="list"
        border
        fit
        highlight-current-row
        class="archive-table"
        style="margin-top: 14px;"
      >
        <el-table-column label="手机号" prop="phone" min-width="140" />
        <el-table-column label="平台" min-width="220">
          <template slot-scope="scope">
            <el-tag
              v-for="item in scope.row.platforms_list"
              :key="item"
              size="mini"
              class="platform-tag"
            >
              {{ platformLabel(item) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="来源" prop="source" width="110" />
        <el-table-column label="过滤状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.is_filtered ? 'warning' : 'success'" size="small" class="status-tag">
              {{ scope.row.is_filtered ? '命中' : '正常' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="备注" prop="remark" min-width="180" />
        <el-table-column label="更新时间" width="180">
          <template slot-scope="scope">{{ scope.row.updated_at | datetime }}</template>
        </el-table-column>
        <el-table-column label="操作" width="185" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" plain class="action-btn edit-btn" @click="openEdit(scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" plain class="action-btn delete-btn" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="getList"
      />
    </el-card>

    <el-dialog :title="isEdit ? '编辑归档数据' : '新增归档数据'" :visible.sync="dialogVisible" width="620px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" maxlength="11" />
        </el-form-item>
        <el-form-item label="来源" prop="source">
          <el-input v-model="form.source" />
        </el-form-item>
        <el-form-item label="过滤命中">
          <el-switch v-model="form.is_filtered" />
        </el-form-item>
        <el-form-item label="平台" prop="platforms">
          <el-checkbox-group v-model="form.platforms">
            <el-checkbox v-for="item in platformMeta" :key="item.code" :label="item.code">{{ item.label }}</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="submitForm">保存</el-button>
      </div>
    </el-dialog>

    <el-dialog title="批量导入归档数据" :visible.sync="importVisible" width="620px" custom-class="archive-import-dialog">
      <el-form label-width="90px">
        <el-form-item label="导入说明">
          <div class="import-hero">
            <div class="hero-title">仅支持 XLSX 模板文件，列名顺序不可变更</div>
            <div class="hero-sub">模板字段: phone / source / remark / platforms / is_filtered</div>
          </div>
          <div class="import-help">
            <p><strong>字段说明：</strong></p>
            <p><code>phone</code>：11位中国手机号（必填，唯一）</p>
            <p><code>source</code>：数据来源（示例：manual/import）</p>
            <p><code>remark</code>：备注（可空）</p>
            <p><code>platforms</code>：平台注册，多个用 <code>|</code> 分隔</p>
            <p><code>is_filtered</code>：是否过滤，<code>0</code>=否，<code>1</code>=是</p>
          </div>
          <div class="platform-map">
            <span class="map-pill">微信 = <code>wechat</code></span>
            <span class="map-pill">支付宝 = <code>alipay</code></span>
            <span class="map-pill">抖音 = <code>douyin</code></span>
            <span class="map-pill">QQ = <code>qq</code></span>
            <span class="map-pill">三条 = <code>santiao</code></span>
          </div>
        </el-form-item>
        <el-form-item label="文件">
          <el-upload
            ref="importUploadRef"
            drag
            :auto-upload="false"
            :limit="1"
            :on-change="handleImportFileChange"
            :on-remove="handleImportFileRemove"
            accept=".xlsx"
          >
            <i class="el-icon-upload" />
            <div class="el-upload__text">拖拽或点击上传 XLSX 模板文件</div>
            <div slot="tip" class="el-upload__tip">列名和顺序必须严格为: phone,source,remark,platforms,is_filtered</div>
          </el-upload>
        </el-form-item>
        <el-form-item label="模板">
          <el-button size="mini" type="primary" plain icon="el-icon-download" @click="downloadTemplate">
            下载XLSX模板
          </el-button>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="importVisible = false">取消</el-button>
        <el-button type="primary" :loading="importLoading" @click="submitImport">开始导入</el-button>
      </div>
    </el-dialog>

    <el-dialog title="导入失败明细（最多100条）" :visible.sync="importResultVisible" width="680px">
      <el-table :data="importFailedSamples" border size="mini" max-height="360">
        <el-table-column label="行号" prop="line" width="90" />
        <el-table-column label="手机号" prop="phone" min-width="180" />
        <el-table-column label="原因" prop="reason" min-width="220" />
      </el-table>
      <div slot="footer">
        <el-button type="primary" @click="importResultVisible = false">知道了</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import {
  getArchiveDataList,
  getArchivePlatformMeta,
  createArchiveData,
  updateArchiveData,
  deleteArchiveData,
  importArchiveData,
  getArchiveImportTemplate
} from '@/api/dataManagement'

export default {
  name: 'ArchiveDataIndex',
  components: { Pagination },
  data() {
    const phoneValidator = (rule, value, callback) => {
      if (!/^1[3-9]\d{9}$/.test(String(value || ''))) {
        callback(new Error('请输入 11 位中国手机号'))
      } else {
        callback()
      }
    }
    return {
      platformMeta: [],
      list: [],
      total: 0,
      listLoading: false,
      submitLoading: false,
      importLoading: false,
      syncLoading: false,
      importResultVisible: false,
      importFailedSamples: [],
      listQuery: {
        page: 1,
        limit: 10,
        phone: '',
        remark: '',
        source: '',
        is_filtered: '',
        platforms: []
      },
      dialogVisible: false,
      importVisible: false,
      importFile: null,
      isEdit: false,
      currentId: null,
      form: {
        phone: '',
        source: 'manual',
        is_filtered: false,
        platforms: [],
        remark: ''
      },
      rules: {
        phone: [{ required: true, validator: phoneValidator, trigger: 'blur' }]
      }
    }
  },
  created() {
    this.getPlatformMeta()
    this.getList()
  },
  methods: {
    getPlatformMeta() {
      getArchivePlatformMeta().then(res => {
        this.platformMeta = res.data || []
      })
    },
    getList() {
      this.listLoading = true
      const params = { ...this.listQuery }
      getArchiveDataList(params).then(res => {
        const data = res.data || {}
        this.list = data.items || []
        this.total = data.total || 0
        this.listLoading = false
      }).catch(() => {
        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    platformLabel(code) {
      const found = this.platformMeta.find(item => item.code === code)
      return found ? found.label : code
    },
    openCreate() {
      this.isEdit = false
      this.currentId = null
      this.form = { phone: '', source: 'manual', is_filtered: false, platforms: [], remark: '' }
      this.dialogVisible = true
      this.$nextTick(() => this.$refs.formRef && this.$refs.formRef.clearValidate())
    },
    openEdit(row) {
      this.isEdit = true
      this.currentId = row.id
      this.form = {
        phone: String(row.phone || ''),
        source: row.source || 'manual',
        is_filtered: !!row.is_filtered,
        platforms: row.platforms_list || [],
        remark: row.remark || ''
      }
      this.dialogVisible = true
      this.$nextTick(() => this.$refs.formRef && this.$refs.formRef.clearValidate())
    },
    submitForm() {
      this.$refs.formRef.validate(valid => {
        if (!valid) return
        this.submitLoading = true
        const payload = { ...this.form }
        const req = this.isEdit ? updateArchiveData(this.currentId, payload) : createArchiveData(payload)
        req.then(() => {
          this.$message.success(this.isEdit ? '更新成功' : '创建成功')
          this.dialogVisible = false
          this.getList()
          this.submitLoading = false
        }).catch(() => {
          this.submitLoading = false
        })
      })
    },
    handleDelete(row) {
      this.$confirm(`确认删除手机号 ${row.phone} 吗？`, '提示', { type: 'warning' })
        .then(() => {
          deleteArchiveData(row.id).then(() => {
            this.$message.success('删除成功')
            this.getList()
          })
        })
        .catch(() => {})
    },
    openImport() {
      this.importVisible = true
      this.importFile = null
      this.$nextTick(() => this.$refs.importUploadRef && this.$refs.importUploadRef.clearFiles())
    },
    handleImportFileChange(file) {
      this.importFile = file.raw
    },
    handleImportFileRemove() {
      this.importFile = null
    },
    submitImport() {
      if (!this.importFile) {
        this.$message.warning('请选择导入文件')
        return
      }
      const fileName = (this.importFile.name || '').toLowerCase()
      if (!fileName.endsWith('.xlsx')) {
        this.$message.warning('仅支持上传 .xlsx 模板文件')
        return
      }
      this.importLoading = true
      const formData = new FormData()
      formData.append('file', this.importFile)
      importArchiveData(formData).then(res => {
        const data = res.data || {}
        this.$message.success(`导入完成：新增${data.created || 0}，跳过${data.skipped || 0}，无效${data.invalid || 0}，重复${data.duplicate || 0}`)
        this.importFailedSamples = data.failed_samples || []
        this.importResultVisible = this.importFailedSamples.length > 0
        this.importVisible = false
        this.getList()
        this.importLoading = false
      }).catch(() => {
        this.importLoading = false
      })
    },
    downloadTemplate() {
      getArchiveImportTemplate().then(res => {
        const data = res.data || {}
        const contentBase64 = data.content_base64 || ''
        const filename = data.filename || 'archive_import_template.xlsx'
        const mimeType = data.mime_type || 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        if (!contentBase64) {
          this.$message.error('模板数据为空')
          return
        }
        const bytes = window.atob(contentBase64)
        const len = bytes.length
        const arr = new Uint8Array(len)
        for (let i = 0; i < len; i++) arr[i] = bytes.charCodeAt(i)
        const blob = new Blob([arr], { type: mimeType })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = filename
        link.click()
        URL.revokeObjectURL(link.href)
      })
    },
    handleSync() {
      this.$message.warning('功能未开启')
    }
  }
}
</script>

<style lang="scss" scoped>
.archive-page {
  min-height: 100%;
  background:
    radial-gradient(680px 220px at 6% -6%, rgba(29, 200, 148, 0.24), transparent 58%),
    radial-gradient(720px 260px at 96% -8%, rgba(38, 132, 255, 0.18), transparent 56%);
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 14px;
  margin-bottom: 20px;
  padding: 22px 24px;
  background:
    linear-gradient(120deg, rgba(18, 73, 55, 0.95) 0%, rgba(33, 112, 82, 0.95) 55%, rgba(41, 148, 103, 0.95) 100%);
  border-radius: 14px;
  color: #fff;
  box-shadow: 0 14px 34px rgba(19, 85, 62, 0.25);
  position: relative;
  overflow: hidden;
  animation: floatIn 420ms ease-out both;

  &::after {
    content: "";
    position: absolute;
    top: -30%;
    left: -40%;
    width: 40%;
    height: 160%;
    transform: rotate(16deg);
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.22), transparent);
    animation: headerSweep 4.2s ease-in-out infinite;
    pointer-events: none;
  }

  .header-copy {
    max-width: 640px;
    position: relative;
    z-index: 1;
  }

  h2 {
    margin: 0 0 10px 0;
    font-size: 26px;
    letter-spacing: 0.4px;
  }

  p {
    margin: 0;
    opacity: 0.92;
    font-size: 13px;
  }
}

.header-badges {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}

.badge-chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 5px 12px;
  border-radius: 999px;
  font-size: 12px;
  color: #f4fff8;
  border: 1px solid rgba(255, 255, 255, 0.32);
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(4px);
}

.archive-shell {
  border-radius: 14px;
  border: 1px solid #e8eef5;
  box-shadow: 0 10px 28px rgba(21, 68, 102, 0.08);
  animation: riseIn 520ms ease-out both;
}

.toolbar {
  position: relative;
  padding: 12px 12px 4px;
  border-radius: 12px;
  background: linear-gradient(180deg, #f8fcff 0%, #f4f9ff 100%);
  border: 1px solid #e5eff9;
}

.archive-table {
  border-radius: 12px;
  overflow: hidden;
}

.platform-tag {
  margin-right: 6px;
  margin-bottom: 4px;
  border-radius: 999px;
  border-color: #b9daf8;
  color: #1f6fb2;
  background: #edf6ff;
  transition: transform 180ms ease, box-shadow 180ms ease;
}

.platform-tag:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 12px rgba(84, 141, 195, 0.28);
}

.archive-page ::v-deep .el-table th {
  background: #f3f8ff;
  color: #3d4a5c;
  font-weight: 600;
}

.archive-page ::v-deep .el-table__row:hover > td {
  background: #f8fbff;
}

.archive-page ::v-deep .el-dialog {
  border-radius: 14px;
  overflow: hidden;
}

.archive-page ::v-deep .el-dialog__header {
  background: linear-gradient(120deg, #f4f9ff 0%, #eef6ff 100%);
  border-bottom: 1px solid #e3edf9;
}

.archive-page ::v-deep .el-upload-dragger {
  border-radius: 12px;
  border: 1px dashed #9ac7ea;
  background: #f7fbff;
}

.archive-page ::v-deep .el-upload-dragger:hover {
  border-color: #5ea7dd;
}

.archive-page ::v-deep .el-button {
  transition: transform 160ms ease, box-shadow 200ms ease;
}

.archive-page ::v-deep .el-button:hover {
  transform: translateY(-1px);
}

.archive-page ::v-deep .pagination-container {
  padding-top: 14px;
  margin-top: 4px;
  border-top: 1px dashed #e6edf6;
}

@media (max-width: 768px) {
  .page-header {
    padding: 18px 16px;
  }

  .badge-chip {
    font-size: 11px;
  }
}

.filter-container {
  .filter-item {
    display: inline-block;
    vertical-align: middle;
    margin-bottom: 10px;
    margin-right: 10px;
  }
}

.import-help {
  margin-top: 8px;
  padding: 10px 12px;
  background: linear-gradient(180deg, #f8fcff 0%, #f2f8ff 100%);
  border: 1px solid #d3e7fb;
  border-radius: 8px;
  color: #4f5f70;
  font-size: 12px;
  line-height: 1.7;

  p {
    margin: 0;
  }
}

.import-hero {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #cde4fb;
  background: linear-gradient(145deg, #f7fbff 0%, #edf6ff 100%);
}

.hero-title {
  font-size: 13px;
  font-weight: 600;
  color: #32567c;
}

.hero-sub {
  margin-top: 4px;
  font-size: 12px;
  color: #55708d;
}

.platform-map {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.map-pill {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  border: 1px solid #d2e7fb;
  background: #f4f9ff;
  color: #3f5f80;
  font-size: 12px;
  padding: 3px 10px;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page {
  background:
    radial-gradient(680px 220px at 6% -6%, rgba(83, 173, 136, 0.18), transparent 58%),
    radial-gradient(720px 260px at 96% -8%, rgba(91, 127, 212, 0.16), transparent 56%);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .page-header {
  background: linear-gradient(120deg, rgba(28, 41, 36, 0.96) 0%, rgba(36, 54, 45, 0.96) 55%, rgba(46, 72, 58, 0.96) 100%);
  box-shadow: 0 14px 34px rgba(0, 0, 0, 0.35);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .badge-chip {
  color: #e8efe9;
  border-color: rgba(225, 234, 228, 0.24);
  background: rgba(255, 255, 255, 0.08);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-shell {
  background: #20252b;
  border-color: #333a42;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .toolbar {
  background: linear-gradient(180deg, #232a31 0%, #20262d 100%);
  border-color: #353f49;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .platform-tag {
  border-color: #4f77a0;
  color: #b8dcff;
  background: linear-gradient(180deg, #2b3b4f 0%, #253446 100%);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .platform-tag:hover {
  box-shadow: 0 7px 14px rgba(88, 135, 186, 0.35);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .import-help {
  background: linear-gradient(180deg, #232a31 0%, #20262d 100%);
  border-color: #37424d;
  color: #b7c2cc;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-table {
  background: #1f242a;
  color: #d5dde6;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-table th {
  background: #252d35;
  color: #dbe4ee;
  border-bottom-color: #36404a;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-table td {
  background: #1f242a;
  color: #cad3dd;
  border-bottom-color: #313a44;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .status-tag.el-tag--success {
  color: #153a2d;
  border-color: #5dd8a8;
  background: #7cf0c2;
  box-shadow: 0 0 0 1px rgba(93, 216, 168, 0.35), 0 0 18px rgba(93, 216, 168, 0.28);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .status-tag.el-tag--warning {
  color: #4a2c08;
  border-color: #ffb95f;
  background: #ffd28e;
  box-shadow: 0 0 0 1px rgba(255, 185, 95, 0.35), 0 0 18px rgba(255, 185, 95, 0.3);
  animation: warnPulse 1.6s ease-in-out infinite;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .action-btn.edit-btn {
  color: #9fd1ff;
  border-color: #4e7ead;
  background: #273748;
  box-shadow: inset 0 0 0 1px rgba(109, 168, 222, 0.25), 0 0 16px rgba(74, 132, 189, 0.22);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .action-btn.edit-btn:hover {
  color: #edf7ff;
  border-color: #89bff2;
  background: #36506a;
  box-shadow: inset 0 0 0 1px rgba(145, 199, 248, 0.45), 0 0 18px rgba(111, 169, 223, 0.4);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .action-btn.delete-btn {
  color: #ffb3b3;
  border-color: #9e4a57;
  background: #3b252b;
  box-shadow: inset 0 0 0 1px rgba(190, 95, 109, 0.25), 0 0 16px rgba(161, 73, 88, 0.22);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .action-btn.delete-btn:hover {
  color: #ffe5e5;
  border-color: #de7d8a;
  background: #55323c;
  box-shadow: inset 0 0 0 1px rgba(230, 134, 148, 0.42), 0 0 18px rgba(206, 101, 116, 0.38);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-select .el-input__inner {
  background: #242d36;
  border-color: #40505f;
  color: #dbe5ef;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-select .el-input__inner:focus {
  border-color: #9ac7f2;
  box-shadow: 0 0 0 2px rgba(92, 156, 217, 0.22);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-table__row:hover > td {
  background: #242b33;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-dialog {
  background: #1f252b;
  border: 1px solid #343e48;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-dialog__header {
  background: linear-gradient(120deg, #242d36 0%, #202830 100%);
  border-bottom-color: #36414c;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-upload-dragger {
  background: #1f2730;
  border-color: #4a6581;
  color: #d0dae4;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-upload-dragger:hover {
  border-color: #6f91b3;
  background: #222d38;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .pagination-container {
  border-top-color: #37414b;
}

/* 黑金主题覆盖层 */
body.theme-dark:not([data-theme='black-gold']) .archive-page {
  background:
    repeating-linear-gradient(
      -18deg,
      rgba(214, 171, 92, 0.03) 0,
      rgba(214, 171, 92, 0.03) 1px,
      rgba(0, 0, 0, 0) 1px,
      rgba(0, 0, 0, 0) 7px
    ),
    #1c1c1c;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .page-header {
  border: 1px solid #5b4521;
  background: linear-gradient(120deg, #1f1910 0%, #2d2415 52%, #1a150f 100%);
  box-shadow: 0 14px 34px rgba(0, 0, 0, 0.4), inset 0 0 0 1px rgba(222, 180, 98, 0.08);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-shell {
  border-color: #5a4522;
  background: linear-gradient(160deg, #11100d 0%, #17130e 58%, #0f0d09 100%);
  box-shadow: 0 0 0 1px rgba(224, 181, 100, 0.08), 0 14px 30px rgba(0, 0, 0, 0.38);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .toolbar {
  border-color: #5d4823;
  background: linear-gradient(180deg, #1b160f 0%, #16120d 100%);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .platform-tag {
  border-color: #8f6d31;
  color: #f2d8a4;
  background: linear-gradient(180deg, #332612 0%, #2a1f10 100%);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-table,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-table td {
  background: #17130e;
  color: #ead2a0;
  border-bottom-color: #5a4522;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-table th {
  color: #f3d89f;
  border-bottom-color: #6a5228;
  background: linear-gradient(180deg, #2b2417 0%, #1f1a12 100%);
  position: relative;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-table th::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: repeating-linear-gradient(
    -18deg,
    rgba(245, 216, 146, 0.06) 0,
    rgba(245, 216, 146, 0.06) 2px,
    rgba(0, 0, 0, 0) 2px,
    rgba(0, 0, 0, 0) 7px
  );
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-table__row:hover > td {
  background: linear-gradient(90deg, rgba(109, 83, 36, 0.34) 0%, rgba(72, 53, 24, 0.52) 100%);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .action-btn.edit-btn {
  color: #f2d9a7;
  border-color: #8e6b2f;
  background: #2f2413;
  box-shadow: inset 0 0 0 1px rgba(198, 151, 72, 0.22), 0 0 16px rgba(166, 122, 46, 0.18);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .action-btn.edit-btn:hover {
  color: #fff3d4;
  border-color: #c39645;
  background: #3f2f17;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .action-btn.delete-btn {
  color: #ffd2a8;
  border-color: #9f6231;
  background: #3a2613;
  box-shadow: inset 0 0 0 1px rgba(182, 108, 50, 0.24), 0 0 16px rgba(145, 85, 40, 0.18);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .action-btn.delete-btn:hover {
  color: #ffe9d1;
  border-color: #cf8343;
  background: #4b3118;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-dialog {
  border: 1px solid #5a4522;
  background: linear-gradient(160deg, #11100d 0%, #17130e 58%, #0f0d09 100%);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-dialog__header {
  border-bottom-color: #5a4522;
  background: linear-gradient(120deg, #2b2316 0%, #221c12 100%);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-form-item__label {
  color: #d9be8c;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-input__inner,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-textarea__inner {
  border-color: #624c24;
  background: #18140f;
  color: #f2dfb5;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-input__inner:focus,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .el-textarea__inner:focus {
  border-color: #ba9042;
  box-shadow: 0 0 0 1px rgba(186, 144, 66, 0.24) inset;
}

@keyframes headerSweep {
  0% { left: -48%; opacity: 0; }
  8% { opacity: 1; }
  45% { left: 115%; opacity: 0; }
  100% { left: 115%; opacity: 0; }
}

@keyframes riseIn {
  from { opacity: 0; transform: translateY(8px) scale(0.995); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes floatIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

<style lang="scss">
body.theme-dark:not([data-theme='black-gold']) .archive-filter-popper {
  background: linear-gradient(180deg, #1a150f 0%, #13100c 100%);
  border-color: #644c23;
}

body.theme-dark:not([data-theme='black-gold']) .archive-filter-popper[x-placement^="bottom"] .popper__arrow {
  border-bottom-color: #644c23;
}

body.theme-dark:not([data-theme='black-gold']) .archive-filter-popper[x-placement^="bottom"] .popper__arrow::after {
  border-bottom-color: #1a150f;
}

body.theme-dark:not([data-theme='black-gold']) .archive-filter-popper .el-select-dropdown__item {
  color: #ebd5a7;
}

body.theme-dark:not([data-theme='black-gold']) .archive-filter-popper .el-select-dropdown__item.hover,
body.theme-dark:not([data-theme='black-gold']) .archive-filter-popper .el-select-dropdown__item:hover {
  background: linear-gradient(90deg, rgba(111, 83, 35, 0.34) 0%, rgba(74, 54, 24, 0.54) 100%);
  color: #ffe2a4;
}

body.theme-dark:not([data-theme='black-gold']) .archive-filter-popper .el-select-dropdown__item.selected {
  color: #ffd98f;
  font-weight: 600;
  text-shadow: 0 0 10px rgba(205, 154, 70, 0.38);
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-loading-mask {
  background-color: rgba(21, 27, 34, 0.72) !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-loading-spinner .path {
  stroke: #89bff2;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-loading-spinner .el-loading-text {
  color: #bcd8f2;
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog {
  background: linear-gradient(160deg, #11100d 0%, #17130e 58%, #0f0d09 100%);
  border: 1px solid #5a4522;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45);
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .el-dialog__header {
  background: linear-gradient(120deg, #2b2316 0%, #221c12 100%);
  border-bottom: 1px solid #5a4522;
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .el-dialog__title {
  color: #f0d8a5;
  letter-spacing: 0.4px;
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .el-form-item__label {
  color: #c4d1de;
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .import-hero {
  border-color: #42607d;
  background: linear-gradient(145deg, #253140 0%, #212c38 100%);
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .hero-title {
  color: #c7def7;
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .hero-sub {
  color: #9db3c9;
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .import-help {
  background: linear-gradient(180deg, #232d37 0%, #202933 100%);
  border-color: #405060;
  color: #c3ced9;
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .map-pill {
  border-color: #476283;
  background: #253445;
  color: #b8d4ef;
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .el-upload-dragger {
  background: linear-gradient(180deg, #202a34 0%, #1d2630 100%);
  border-color: #55779b;
  color: #d6e1ec;
  box-shadow: inset 0 0 0 1px rgba(92, 141, 194, 0.2);
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .el-upload-dragger:hover {
  background: linear-gradient(180deg, #23303d 0%, #202b36 100%);
  border-color: #79a5d1;
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .el-dialog__footer {
  border-top: 1px solid #34414f;
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .el-button--primary {
  box-shadow: 0 0 18px rgba(193, 145, 72, 0.3);
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .el-button--primary.is-plain {
  color: #bfe1ff;
  border-color: #5b83ad;
  background: #273a4d;
}

body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .el-button--primary.is-plain:hover,
body.theme-dark:not([data-theme='black-gold']) .archive-import-dialog .el-button--primary.is-plain:focus {
  color: #e8f4ff;
  border-color: #84b3df;
  background: #2f4660;
}

/* 高优先级覆盖：强化 hover 动态、操作按钮、下拉框黑金样式 */
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-table .el-table__body tr:hover > td {
  background: linear-gradient(90deg, rgba(67, 50, 22, 0.55) 0%, rgba(49, 37, 17, 0.72) 100%) !important;
  color: #f0ddb5 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-table .el-table__body tr.hover-row > td {
  background: linear-gradient(90deg, rgba(67, 50, 22, 0.55) 0%, rgba(49, 37, 17, 0.72) 100%) !important;
  color: #f0ddb5 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-table .el-table__body tr.current-row > td,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-table .el-table__fixed-body-wrapper tr.current-row > td,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-table .el-table__fixed-right .el-table__fixed-body-wrapper tr.current-row > td,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-table .el-table__fixed .el-table__fixed-body-wrapper tr.current-row > td,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-table .el-table__fixed-body-wrapper tr:hover > td,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-table .el-table__fixed-right .el-table__fixed-body-wrapper tr:hover > td,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-table .el-table__fixed .el-table__fixed-body-wrapper tr:hover > td {
  background: linear-gradient(90deg, rgba(67, 50, 22, 0.55) 0%, rgba(49, 37, 17, 0.72) 100%) !important;
  color: #f0ddb5 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-table .el-table__fixed,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-table .el-table__fixed-right,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-table .el-table__fixed::before,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-table .el-table__fixed-right::before {
  background-color: #17130e !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .action-btn.edit-btn {
  color: #fff1cc !important;
  border-color: #c39243 !important;
  background: linear-gradient(90deg, #6f5224 0%, #9f7533 60%, #c89a4b 100%) !important;
  box-shadow: 0 0 0 1px rgba(218, 171, 82, 0.24), 0 0 18px rgba(181, 129, 43, 0.3) !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .action-btn.edit-btn:hover {
  color: #fff8e6 !important;
  border-color: #deb368 !important;
  background: linear-gradient(90deg, #7e5c29 0%, #b5843c 60%, #d6aa5a 100%) !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .action-btn.delete-btn {
  color: #ffe3c7 !important;
  border-color: #cb7b3d !important;
  background: linear-gradient(90deg, #6a3f1d 0%, #8e5529 60%, #b26a34 100%) !important;
  box-shadow: 0 0 0 1px rgba(208, 124, 60, 0.22), 0 0 18px rgba(170, 100, 44, 0.28) !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .action-btn.delete-btn:hover {
  color: #fff1e4 !important;
  border-color: #e09a5f !important;
  background: linear-gradient(90deg, #7a4922 0%, #a36230 60%, #c37a3c 100%) !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-input__inner,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-select .el-input__inner {
  border-color: #6a5228 !important;
  background: #18140f !important;
  color: #efdcb3 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-select .el-input__inner::placeholder,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-input__inner::placeholder {
  color: #bda578 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-select .el-input__suffix-inner i,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-input__suffix-inner i {
  color: #caa96a !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-select .el-input__inner[readonly] {
  background: #18140f !important;
  color: #efdcb3 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-select .el-select__placeholder,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-select .el-select__selected-item {
  color: #efdcb3 !important;
}

/* 定点覆盖：过滤状态/平台下拉框默认态 */
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-dark-select .el-input__inner,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-dark-select .el-input__inner[readonly] {
  background: #17130f !important;
  border-color: #6a5228 !important;
  color: #efdcb3 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-dark-select .el-input__inner::placeholder {
  color: #bda578 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-dark-select .el-input__suffix-inner i {
  color: #d0b178 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-dark-select .el-select__tags .el-tag,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-dark-select .el-tag {
  background: linear-gradient(180deg, #332612 0%, #2a1f10 100%) !important;
  border-color: #8f6d31 !important;
  color: #f2d8a4 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .archive-dark-select .el-tag__close {
  background: rgba(196, 149, 71, 0.22) !important;
  color: #f8e6c2 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-input__inner:focus,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-select .el-input__inner:focus {
  border-color: #bf9245 !important;
  box-shadow: 0 0 0 1px rgba(191, 146, 69, 0.26) inset !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-filter-popper {
  border-color: #6a5228 !important;
  background: linear-gradient(180deg, #1b160f 0%, #14100c 100%) !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-filter-popper .el-select-dropdown__item {
  color: #f0dcb2 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-filter-popper .el-select-dropdown__item.hover,
body.theme-dark:not([data-theme='black-gold']) .archive-filter-popper .el-select-dropdown__item:hover {
  background: linear-gradient(90deg, rgba(118, 86, 36, 0.38) 0%, rgba(80, 58, 25, 0.58) 100%) !important;
  color: #ffe8b9 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-filter-popper .el-select-dropdown__item.selected {
  color: #ffdca0 !important;
  background: linear-gradient(90deg, rgba(126, 92, 39, 0.38) 0%, rgba(88, 63, 27, 0.58) 100%) !important;
  text-shadow: 0 0 10px rgba(205, 154, 70, 0.42) !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-select__tags .el-tag,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-select .el-tag {
  border-color: #8f6d31 !important;
  background: linear-gradient(180deg, #332612 0%, #2a1f10 100%) !important;
  color: #f2d8a4 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-select__tags .el-tag__close,
body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-select .el-tag__close {
  color: #f7e6c2 !important;
  background: rgba(196, 149, 71, 0.22) !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page ::v-deep .toolbar .el-select__tags-text {
  color: #f2d8a4 !important;
}

@keyframes warnPulse {
  0%, 100% {
    box-shadow: 0 0 0 1px rgba(255, 185, 95, 0.35), 0 0 12px rgba(255, 185, 95, 0.28);
  }
  50% {
    box-shadow: 0 0 0 1px rgba(255, 185, 95, 0.5), 0 0 22px rgba(255, 185, 95, 0.45);
  }
}

/* 全局硬覆盖（避免 scoped/旧样式冲突） */
body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-table__body tr:hover > td,
body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-table__body tr.hover-row > td,
body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-table__body tr.current-row > td,
body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-table__fixed-body-wrapper tr:hover > td,
body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-table__fixed-body-wrapper tr.hover-row > td,
body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-table__fixed-body-wrapper tr.current-row > td,
body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-table__fixed-right .el-table__fixed-body-wrapper tr:hover > td,
body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-table__fixed-right .el-table__fixed-body-wrapper tr.current-row > td {
  background: #2b2114 !important;
  color: #f0ddb5 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-table__fixed,
body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-table__fixed-right,
body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-table__fixed::before,
body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-table .el-table__fixed-right::before {
  background: #17130e !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-dark-select .el-input__inner,
body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-dark-select .el-input__inner[readonly],
body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-dark-select .el-input.is-focus .el-input__inner {
  background: #17130f !important;
  border-color: #6a5228 !important;
  color: #efdcb3 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-dark-select .el-input__inner::placeholder {
  color: #bda578 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-dark-select .el-input__suffix-inner i {
  color: #d0b178 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-dark-select .el-select__tags .el-tag,
body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-dark-select .el-tag {
  background: #2a1f10 !important;
  border-color: #8f6d31 !important;
  color: #f2d8a4 !important;
}

body.theme-dark:not([data-theme='black-gold']) .archive-page .archive-dark-select .el-select__tags input {
  color: #efdcb3 !important;
  background: transparent !important;
}

@keyframes archiveRowFlow {
  0% { background-position: 0% 0; }
  100% { background-position: 180% 0; }
}
</style>
