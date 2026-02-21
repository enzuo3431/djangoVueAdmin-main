<template>
  <div class="app-container tools-page">
    <div class="hero content-shell">
      <h2>六扇门ID提取</h2>
      <p>粘贴六扇门文本，自动提取姓名和身份证并入库管理</p>
    </div>
    <el-card class="panel content-shell" shadow="never">
      <el-form inline>
        <el-form-item label="身份证">
          <el-input v-model="query.idcard" placeholder="模糊查询" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="query.status" clearable placeholder="全部" style="width: 120px;">
            <el-option label="未使用" value="0" />
            <el-option label="已使用" value="1" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">查询</el-button>
          <el-button type="success" @click="dialogVisible = true">粘贴解析</el-button>
        </el-form-item>
      </el-form>

      <el-table
        :data="list"
        v-loading="loading"
        border
        element-loading-background="rgba(11, 10, 8, 0.84)"
        style="margin-top: 8px;"
      >
        <el-table-column label="姓名" width="100" align="center">
          <template slot-scope="scope">
            <span class="copy-text" @click="copyText(scope.row.name)">{{ scope.row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="身份证" min-width="200">
          <template slot-scope="scope">
            <span class="copy-text idcard-text" @click="copyText(scope.row.idcard)">{{ scope.row.idcard }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="320" align="center">
          <template slot-scope="scope">
            <el-switch
              :value="scope.row.status === 1"
              active-text="已使用"
              inactive-text="未使用"
              @change="val => handleStatusChange(scope.row, val)"
            />
          </template>
        </el-table-column>
      </el-table>

      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="query.page"
        :limit.sync="query.limit"
        @pagination="getList"
      />
    </el-card>

    <el-dialog
      title="粘贴六扇门文本"
      :visible.sync="dialogVisible"
      width="860px"
      custom-class="liushan-parse-dialog"
      @close="resetParseState"
    >
      <div class="parse-tip-row">
        <el-tooltip placement="top" effect="dark">
          <div slot="content">
            <div>可解析格式示例：</div>
            <div>第[1]条，数据来源：xxx</div>
            <div>同户人：张三，身份证：110101199001011234</div>
            <div>同户人：李四，身份证：32031119951212345X</div>
            <div style="margin-top: 6px;">要求包含：第[x]条，数据来源： + 同户人：</div>
          </div>
          <span class="parse-tip-icon">
            <i class="el-icon-question" />
            解析格式说明
          </span>
        </el-tooltip>
      </div>
      <el-input
        v-model="liushanContent"
        type="textarea"
        :rows="10"
        placeholder="请粘贴原始文本..."
      />
      <div class="preview-summary" v-if="previewDone">
        <el-tag size="mini" class="tag-parsed">解析：{{ previewSummary.parsed }}</el-tag>
        <el-tag size="mini" class="tag-batch" type="warning">批内重复：{{ previewSummary.batch_duplicate }}</el-tag>
        <el-tag size="mini" class="tag-db" type="info">库内重复：{{ previewSummary.db_duplicate }}</el-tag>
        <el-tag size="mini" class="tag-insert" type="success">待入库：{{ previewSummary.to_insert }}</el-tag>
      </div>
      <el-table
        v-if="previewDone"
        :data="previewItems"
        border
        height="240"
        size="mini"
        element-loading-background="rgba(11, 10, 8, 0.84)"
        style="margin-top: 10px;"
      >
        <el-table-column label="姓名" prop="name" width="120" />
        <el-table-column label="身份证" prop="idcard" min-width="220" />
      </el-table>
      <div slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="warning" :loading="previewLoading" @click="handlePreviewText">预览解析</el-button>
        <el-button type="primary" :loading="submitLoading" :disabled="!previewItems.length" @click="handleCommitItems">确认入库</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { previewLiushanText, commitLiushanItems, getLiushanList, updateLiushanStatus } from '@/api/toolsManagement'

export default {
  name: 'ToolsLiushanIndex',
  components: { Pagination },
  data() {
    return {
      loading: false,
      previewLoading: false,
      submitLoading: false,
      dialogVisible: false,
      liushanContent: '',
      previewDone: false,
      previewItems: [],
      previewSummary: {
        parsed: 0,
        batch_duplicate: 0,
        db_duplicate: 0,
        to_insert: 0
      },
      list: [],
      total: 0,
      query: {
        page: 1,
        limit: 10,
        status: '',
        idcard: ''
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.loading = true
      getLiushanList(this.query).then(res => {
        const data = res.data || {}
        this.list = data.items || []
        this.total = data.total || 0
        this.loading = false
      }).catch(() => { this.loading = false })
    },
    handleFilter() {
      this.query.page = 1
      this.getList()
    },
    handlePreviewText() {
      if (!this.liushanContent || this.liushanContent.length < 20) {
        this.$message.warning('内容太短，无法解析')
        return
      }
      this.previewLoading = true
      previewLiushanText({ liushan_content: this.liushanContent }).then(res => {
        const data = res.data || {}
        this.previewDone = true
        this.previewItems = data.items || []
        this.previewSummary = {
          parsed: data.parsed || 0,
          batch_duplicate: data.batch_duplicate || 0,
          db_duplicate: data.db_duplicate || 0,
          to_insert: data.to_insert || 0
        }
        this.$message.success(res.message || '预览完成')
        this.previewLoading = false
      }).catch(() => { this.previewLoading = false })
    },
    handleCommitItems() {
      if (!this.previewItems.length) {
        this.$message.warning('没有可入库数据，请先预览解析')
        return
      }
      this.submitLoading = true
      commitLiushanItems({ items: this.previewItems }).then(res => {
        this.$message.success(res.message || '入库完成')
        this.dialogVisible = false
        this.resetParseState()
        this.getList()
        this.submitLoading = false
      }).catch(() => { this.submitLoading = false })
    },
    handleStatusChange(row, val) {
      updateLiushanStatus({ id: row.id, status: val ? 1 : 0 }).then(() => {
        this.$message.success('状态已更新')
        this.getList()
      })
    },
    copyText(text) {
      if (!text) return
      navigator.clipboard.writeText(String(text)).then(() => {
        this.$message.success(`已复制：${text}`)
      })
    },
    resetParseState() {
      this.liushanContent = ''
      this.previewDone = false
      this.previewItems = []
      this.previewSummary = {
        parsed: 0,
        batch_duplicate: 0,
        db_duplicate: 0,
        to_insert: 0
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.tools-page .hero {
  margin-bottom: 16px;
  padding: 20px;
  border-radius: 14px;
  color: #fff;
  background: linear-gradient(120deg, #4a284f 0%, #7b3a87 100%);
}
.panel { border-radius: 14px; }
.content-shell {
  max-width: 1040px;
  margin-left: auto;
  margin-right: auto;
}
body.theme-dark:not([data-theme='black-gold']) .tools-page {
  position: relative;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background: #1c1c1c;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page > * {
  position: relative;
  z-index: 1;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .hero {
  border: 1px solid #5e4823;
  background: linear-gradient(120deg, #1f1910 0%, #2d2415 52%, #1a150f 100%);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.35), inset 0 0 0 1px rgba(222, 180, 98, 0.08);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .hero::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 14px;
  pointer-events: none;
  background: repeating-linear-gradient(
    -16deg,
    rgba(229, 188, 108, 0.055) 0,
    rgba(229, 188, 108, 0.055) 1px,
    rgba(0, 0, 0, 0) 1px,
    rgba(0, 0, 0, 0) 8px
  );
}

.tools-page ::v-deep .el-switch__label {
  width: 44px;
  text-align: center;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-switch__label {
  color: #8a7752;
  opacity: 0.2;
  filter: grayscale(1);
  transition: color 0.2s ease;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-switch__label.is-active {
  color: #f3d289;
  opacity: 1;
  filter: grayscale(0);
  text-shadow: 0 0 8px rgba(243, 210, 137, 0.2);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-switch .el-switch__core {
  border-color: #5f4a25;
  background-color: #2a2115;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-switch.is-checked .el-switch__core {
  border-color: #a07933;
  background: linear-gradient(90deg, #7d5c24 0%, #b3863a 100%);
}

.parse-tip-row {
  margin-bottom: 10px;
}

.preview-summary {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.copy-text {
  cursor: pointer;
  color: #2f75b6;
  font-size: 18px;
  line-height: 1.35;
}

.copy-text:hover {
  color: #1b5f9b;
  text-decoration: underline;
}

.idcard-text {
  font-family: Menlo, Consolas, monospace;
}

.tools-page ::v-deep .liushan-parse-dialog .el-table .cell {
  font-size: 18px;
  line-height: 1.35;
}

.parse-tip-icon {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #4a6b8c;
  cursor: pointer;
}

body.theme-dark:not([data-theme='black-gold']) .parse-tip-icon {
  color: #d8bc85;
}

body.theme-dark:not([data-theme='black-gold']) .copy-text {
  color: #f2d18b;
}

body.theme-dark:not([data-theme='black-gold']) .copy-text:hover {
  color: #ffe4ae;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .liushan-parse-dialog {
  border: 1px solid #2a3a57;
  border-radius: 12px;
  background: linear-gradient(160deg, #14100a 0%, #1b150d 56%, #120f0a 100%);
  box-shadow: 0 18px 45px rgba(7, 14, 27, 0.65), inset 0 0 0 1px rgba(214, 171, 92, 0.08);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .liushan-parse-dialog .el-dialog__header {
  border-bottom: 1px solid rgba(203, 160, 81, 0.26);
  background: linear-gradient(90deg, rgba(98, 72, 31, 0.3) 0%, rgba(71, 52, 24, 0.12) 100%);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .liushan-parse-dialog .el-dialog__title {
  color: #f0d8a5;
  letter-spacing: 0.5px;
  font-weight: 600;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .liushan-parse-dialog .el-dialog__body {
  color: #e7cf9f;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .panel {
  border: 1px solid #5a4522;
  background: linear-gradient(160deg, #11100d 0%, #17130e 58%, #0f0d09 100%);
  box-shadow: 0 0 0 1px rgba(224, 181, 100, 0.08), 0 14px 30px rgba(0, 0, 0, 0.38);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .panel::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: 14px;
  background: repeating-linear-gradient(
    -20deg,
    rgba(220, 176, 95, 0.045) 0,
    rgba(220, 176, 95, 0.045) 1px,
    rgba(0, 0, 0, 0) 1px,
    rgba(0, 0, 0, 0) 7px
  );
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .panel ::v-deep .el-card__body {
  position: relative;
  z-index: 1;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-form-item__label {
  color: #d8be8e;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-input__inner,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-select .el-input__inner {
  border-color: #624c24;
  background: #18140f;
  color: #f2dfb5;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-input__inner:focus,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-select .el-input__inner:focus {
  border-color: #ba9042;
  box-shadow: 0 0 0 1px rgba(186, 144, 66, 0.24) inset;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-button--success {
  border-color: #8e6c2e;
  background: linear-gradient(90deg, #6c4f22 0%, #9b7131 58%, #be9247 100%);
  color: #f9e6be;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .liushan-parse-dialog .el-textarea__inner {
  border: 1px solid #6d5428;
  color: #efdcb3;
  background: linear-gradient(180deg, rgba(33, 27, 18, 0.9) 0%, rgba(24, 19, 13, 0.96) 100%);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .liushan-parse-dialog .el-textarea__inner:focus {
  border-color: #bf9245;
  box-shadow: 0 0 0 1px rgba(191, 146, 69, 0.28) inset;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-table,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-table th,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-table tr,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-table td {
  border-color: #4e3c1e;
  background: #11100d;
  color: #f1e3c0;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-table {
  border: 1px solid #6a5228;
  box-shadow: 0 0 0 1px rgba(233, 191, 104, 0.14), 0 10px 28px rgba(0, 0, 0, 0.35);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-table th {
  background: linear-gradient(180deg, #2b2417 0%, #1f1a12 100%);
  color: #f5d892;
  letter-spacing: 0.5px;
  position: relative;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-table th::after {
  content: '';
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

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-table .el-table__body tr td {
  background: rgba(18, 16, 12, 0.95);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-table .el-table__body tr:nth-child(even) td {
  background: rgba(23, 19, 14, 0.96);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-table__body-wrapper,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-table__fixed-body-wrapper,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-table__empty-block {
  background: linear-gradient(180deg, #11100d 0%, #17130e 100%);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-table::before {
  background-color: #6b5328;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-table--enable-row-hover .el-table__body tr:hover > td {
  background: linear-gradient(90deg, rgba(109, 83, 36, 0.34) 0%, rgba(72, 53, 24, 0.52) 100%);
  box-shadow: inset 0 0 0 1px rgba(233, 191, 104, 0.36), inset 0 0 22px rgba(233, 191, 104, 0.08);
  transition: background 0.2s ease;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-loading-mask {
  background-color: rgba(11, 10, 8, 0.84) !important;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .liushan-parse-dialog .el-dialog__footer {
  border-top: 1px solid rgba(203, 160, 81, 0.2);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .preview-summary .el-tag {
  border-width: 1px;
  font-weight: 600;
  transition: all 0.25s ease;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .preview-summary .tag-parsed {
  color: #f4dca7;
  border-color: #8f6e32;
  background: rgba(116, 85, 34, 0.3);
  box-shadow: 0 0 12px rgba(219, 172, 84, 0.16);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .preview-summary .tag-batch {
  color: #ffdb9b;
  border-color: #9e6f22;
  background: rgba(131, 89, 18, 0.3);
  box-shadow: 0 0 12px rgba(224, 156, 55, 0.2);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .preview-summary .tag-db {
  color: #ebd6a6;
  border-color: #7f642f;
  background: rgba(95, 74, 34, 0.3);
  box-shadow: 0 0 12px rgba(200, 152, 73, 0.16);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .preview-summary .tag-insert {
  color: #f6dfad;
  border-color: #936f32;
  background: rgba(110, 84, 36, 0.32);
  box-shadow: 0 0 12px rgba(207, 159, 74, 0.2);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .preview-summary .el-tag:hover {
  transform: translateY(-1px);
  filter: brightness(1.08);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .liushan-parse-dialog .el-button--primary {
  border-color: #ac7d35;
  background: linear-gradient(90deg, #7a5926 0%, #b7893e 52%, #d3a859 100%);
  box-shadow: 0 10px 24px rgba(149, 108, 39, 0.35);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .liushan-parse-dialog .el-button--primary:hover,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .liushan-parse-dialog .el-button--primary:focus {
  border-color: #c79a4b;
  background: linear-gradient(90deg, #886229 0%, #c29242 55%, #ddb364 100%);
  box-shadow: 0 12px 26px rgba(177, 128, 44, 0.36);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .liushan-parse-dialog .el-button--primary.is-disabled,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .liushan-parse-dialog .el-button--primary.is-disabled:hover {
  border-color: #5d4a24;
  background: linear-gradient(90deg, #3b3020 0%, #4a3a24 100%);
  box-shadow: none;
}
</style>
