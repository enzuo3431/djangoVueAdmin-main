<template>
  <div class="app-container benefits-page">
    <div class="benefits-shell">
      <el-card class="panel info-panel" shadow="never">
        <h3 class="left-title">每日签到 / 劳模活动</h3>
        <p class="left-sub">每局完成30手同号ID</p>
        <table class="rate-table">
          <thead>
            <tr>
              <th>级别/局数</th>
              <th>3局</th>
              <th>5局</th>
              <th>8局</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>1/2</td><td>38</td><td>58</td><td>88</td></tr>
            <tr><td>2/4</td><td>58</td><td>88</td><td>188</td></tr>
            <tr><td>5/10</td><td>88</td><td>188</td><td>288</td></tr>
            <tr><td>10/20</td><td>188</td><td>288</td><td>588</td></tr>
            <tr><td>20/40 (25/50)</td><td>288</td><td>588</td><td>888</td></tr>
            <tr><td>50/100</td><td>588</td><td>888</td><td>1388</td></tr>
            <tr><td>100/200</td><td>888</td><td>1588</td><td>2588</td></tr>
          </tbody>
        </table>

        <h4 class="rec-title">推荐活动</h4>
        <p class="left-sub rec-sub">推荐朋友上桌<br>即可领取推荐奖励</p>
        <table class="rate-table small">
          <thead>
            <tr>
              <th>1/2</th>
              <th>2/4</th>
              <th>5/10</th>
              <th>10/20</th>
              <th>25/50</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>58</td><td>88</td><td>188</td><td>288</td><td>588</td></tr>
          </tbody>
        </table>
        <p class="left-note">推荐奖 = 新人奖励</p>
      </el-card>

      <el-card class="panel tool-panel" shadow="never">
        <div class="panel-head">
          <h2 />
          <div class="actions">
            <el-date-picker
              v-model="queryDate"
              type="date"
              value-format="yyyy-MM-dd"
              placeholder="选择日期"
              class="date-picker"
            />
            <el-button :loading="queryLoading" @click="loadStats">查询</el-button>
            <el-date-picker
              v-model="rangeDates"
              type="daterange"
              value-format="yyyy-MM-dd"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              popper-class="benefits-range-popper"
              class="range-picker"
            />
            <el-button :loading="aggregateLoading" @click="loadAggregate">筛选合计</el-button>
            <el-button type="primary" @click="dialogVisible = true">上传文件</el-button>
          </div>
        </div>

        <div class="table-note">用户块展示：用户 + 指标标识 + 数值（支持 Ctrl+F 搜索）</div>
        <el-empty v-if="!clubBlocks.length && !queryLoading && !aggregateLoading" description="暂无统计数据" />
        <div v-else class="matrix-wrap">
          <div v-for="(club, clubIdx) in clubBlocks" :key="club.name" class="club-block">
            <div class="club-title">{{ club.name }}</div>
            <table
              v-for="(user, userIdx) in club.users"
              :key="`${club.name}-${user.name}`"
              :class="['user-matrix-table', userToneClass(clubIdx, userIdx)]"
            >
              <tbody>
                <tr v-for="(metric, idx) in user.metrics" :key="`${club.name}-${user.name}-${metric.label}`">
                  <td v-if="idx === 0" :rowspan="user.metrics.length" class="user-cell">{{ user.name }}</td>
                  <td class="metric-cell">{{ metric.label }}</td>
                  <td class="value-cell">{{ metric.value }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </el-card>
    </div>

    <el-dialog
      title="上传福利文件"
      :visible.sync="dialogVisible"
      width="760px"
      custom-class="benefits-upload-dialog"
      @close="resetUploadState"
    >
      <div class="upload-date-row">
        <span class="upload-date-label">统计日期</span>
        <el-date-picker
          v-model="uploadDate"
          type="date"
          value-format="yyyy-MM-dd"
          placeholder="不选则默认当天"
          clearable
          class="upload-date-picker"
        />
      </div>
      <el-upload
        ref="uploadRef"
        drag
        multiple
        :auto-upload="false"
        :file-list="uploadFileList"
        :on-change="handleUploadChange"
        :on-remove="handleUploadRemove"
        :before-upload="beforeUpload"
        accept=".xlsx"
      >
        <i class="el-icon-upload" />
        <div class="el-upload__text">点击上传，或拖拽到此处（仅 xlsx）</div>
      </el-upload>
      <div slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="uploadLoading" @click="submitUpload">确认上传</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getBenefitsStats, getBenefitsAggregate, uploadBenefitsFiles } from '@/api/toolsManagement'

export default {
  name: 'ToolsBenefitsIndex',
  data() {
    return {
      queryLoading: false,
      aggregateLoading: false,
      uploadLoading: false,
      dialogVisible: false,
      queryDate: '',
      rangeDates: [],
      uploadDate: '',
      rawData: {},
      clubBlocks: [],
      uploadFileList: []
    }
  },
  created() {
    this.queryDate = this.today()
    this.loadStats()
  },
  methods: {
    today() {
      const d = new Date()
      const y = d.getFullYear()
      const m = `${d.getMonth() + 1}`.padStart(2, '0')
      const day = `${d.getDate()}`.padStart(2, '0')
      return `${y}-${m}-${day}`
    },
    loadStats() {
      this.rangeDates = []
      this.queryLoading = true
      getBenefitsStats({ query_date: this.queryDate }).then(res => {
        this.rawData = res.data || {}
        this.clubBlocks = this.toClubBlocks(this.rawData)
      }).finally(() => {
        this.queryLoading = false
      })
    },
    loadAggregate() {
      if (!this.rangeDates || this.rangeDates.length !== 2) {
        this.$message.warning('请先选择开始和结束日期')
        return
      }
      this.queryDate = ''
      this.aggregateLoading = true
      getBenefitsAggregate({
        start_date: this.rangeDates[0],
        end_date: this.rangeDates[1]
      }).then(res => {
        this.rawData = res.data || {}
        this.clubBlocks = this.toClubBlocks(this.rawData)
        this.$message.success(res.message || '合计完成')
      }).finally(() => {
        this.aggregateLoading = false
      })
    },
    toClubBlocks(raw) {
      if (!raw || typeof raw !== 'object' || Object.keys(raw).length === 0) {
        return []
      }
      const blocks = []
      Object.keys(raw).forEach((club, clubIndex) => {
        const players = raw[club] || {}
        const clubNode = {
          id: `club-${clubIndex}`,
          name: club,
          users: []
        }
        Object.keys(players).forEach((player, playerIndex) => {
          const item = players[player] || {}
          const preferredOrder = ['玩家贵宾分保险总数', '牛仔战绩', '牛仔下注量汇总', '玩家打满30次数']
          const metrics = []
          preferredOrder.forEach((k) => {
            metrics.push({ label: k, value: item[k] !== undefined ? item[k] : 0 })
          })
          Object.keys(item).forEach((k) => {
            if (preferredOrder.indexOf(k) === -1) {
              metrics.push({ label: k, value: item[k] })
            }
          })
          clubNode.users.push({
            id: `player-${clubIndex}-${playerIndex}`,
            name: player,
            metrics
          })
        })
        blocks.push(clubNode)
      })
      return blocks
    },
    userToneClass(clubIdx, userIdx) {
      const tones = ['tone-a', 'tone-b', 'tone-c', 'tone-d', 'tone-e']
      return tones[(clubIdx * 7 + userIdx) % tones.length]
    },
    beforeUpload(file) {
      const ok = file.name.toLowerCase().endsWith('.xlsx')
      if (!ok) this.$message.warning('仅支持 xlsx 文件')
      return ok
    },
    handleUploadChange(file, fileList) {
      this.uploadFileList = fileList.filter(f => f.name.toLowerCase().endsWith('.xlsx'))
    },
    handleUploadRemove(file, fileList) {
      this.uploadFileList = fileList
    },
    submitUpload() {
      if (!this.uploadFileList.length) {
        this.$message.warning('请先选择 xlsx 文件')
        return
      }
      const formData = new FormData()
      this.uploadFileList.forEach(f => {
        if (f.raw) formData.append('files', f.raw)
      })
      if (this.uploadDate) {
        formData.append('query_date', this.uploadDate)
      }
      this.uploadLoading = true
      uploadBenefitsFiles(formData).then(res => {
        const data = res.data || {}
        this.rawData = data.items || {}
        this.clubBlocks = this.toClubBlocks(this.rawData)
        this.queryDate = data.date || this.queryDate
        this.$message.success(res.message || '上传成功')
        this.dialogVisible = false
        this.resetUploadState()
      }).finally(() => {
        this.uploadLoading = false
      })
    },
    resetUploadState() {
      this.uploadFileList = []
      this.uploadDate = ''
      if (this.$refs.uploadRef) this.$refs.uploadRef.clearFiles()
    }
  }
}
</script>

<style lang="scss" scoped>
.panel {
  border-radius: 14px;
  position: relative;
  overflow: hidden;
}

.benefits-shell {
  max-width: 1160px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 320px minmax(0, 1fr);
  gap: 22px;
}

.left-title {
  margin: 0 0 6px;
  text-align: center;
  font-size: 30px;
  font-weight: 700;
  color: #1d45d8;
}

.left-sub {
  margin: 0 0 12px;
  text-align: center;
  color: #253442;
  line-height: 1.45;
}

.rate-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 16px;
  font-size: 13px;
}

.rate-table th,
.rate-table td {
  border: 1px solid #d6dde8;
  text-align: center;
  padding: 7px 6px;
}

.rate-table th {
  background: #e6ebf5;
  font-weight: 700;
}

.rec-title {
  margin: 12px 0 2px;
  text-align: center;
  font-size: 25px;
  color: #1f47df;
}

.rec-sub {
  margin-bottom: 10px;
}

.left-note {
  margin: 8px 0 0;
  text-align: center;
  color: #42505e;
}

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.panel-head h2 {
  margin: 0;
  font-size: 28px;
  line-height: 1.2;
}

.actions {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-end;
  padding: 8px;
  border: 1px solid #d8e0eb;
  border-radius: 10px;
  background: #f8fbff;
}

.date-picker {
  width: 140px;
}

.range-picker {
  width: 290px;
}

.actions ::v-deep .range-picker.el-date-editor.el-input__inner,
.actions ::v-deep .range-picker.el-date-editor {
  width: 330px;
}

.actions ::v-deep .range-picker .el-range-separator {
  width: 32px;
  padding: 0 2px;
  text-align: center;
}

.table-note {
  color: #6c7f92;
  font-size: 13px;
  margin: 2px 0 12px;
}

.upload-date-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.upload-date-label {
  font-size: 13px;
  color: #5e7286;
}

.upload-date-picker {
  width: 180px;
}

.matrix-wrap {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.club-block {
  border: 1px dashed #d9dfe8;
  border-radius: 10px;
  padding: 10px;
  background: #fbfcff;
}

.club-title {
  font-size: 15px;
  font-weight: 700;
  color: #3f5163;
  margin: 2px 0 10px;
}

.user-matrix-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-bottom: 10px;
  border: 2px solid #4a5767;
  border-radius: 6px;
  overflow: hidden;
}

.user-matrix-table.tone-a { background: rgba(70, 112, 190, 0.09); }
.user-matrix-table.tone-b { background: rgba(82, 160, 130, 0.09); }
.user-matrix-table.tone-c { background: rgba(176, 122, 72, 0.09); }
.user-matrix-table.tone-d { background: rgba(132, 104, 188, 0.09); }
.user-matrix-table.tone-e { background: rgba(120, 128, 138, 0.09); }

.user-matrix-table td {
  border-right: 1px dashed #8c99aa;
  border-bottom: 1px dashed #8c99aa;
  font-size: 16px;
  padding: 6px 10px;
  line-height: 1.35;
}

.user-matrix-table tr td:last-child {
  border-right: none;
}

.user-matrix-table tr:last-child td {
  border-bottom: none;
}

.user-cell {
  width: 190px;
  text-align: center;
  letter-spacing: 0.5px;
  font-weight: 700;
}

.metric-cell {
  width: 320px;
  color: #33465a;
}

.value-cell {
  width: 140px;
  text-align: center;
  font-family: Menlo, Consolas, monospace;
  font-weight: 600;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .panel {
  border: 1px solid #594520;
  background: linear-gradient(160deg, #11100d 0%, #17130e 58%, #100d09 100%);
  box-shadow: 0 0 0 1px rgba(229, 189, 110, 0.08), 0 14px 30px rgba(0, 0, 0, 0.4);
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .panel::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: 14px;
  background: repeating-linear-gradient(
    -20deg,
    rgba(226, 186, 104, 0.04) 0,
    rgba(226, 186, 104, 0.04) 1px,
    rgba(0, 0, 0, 0) 1px,
    rgba(0, 0, 0, 0) 7px
  );
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .panel-head h2 {
  color: #f2d7a3;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .actions {
  border-color: #5f4924;
  background: rgba(29, 22, 14, 0.72);
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .left-title,
body.theme-dark:not([data-theme='black-gold']) .benefits-page .rec-title {
  color: #f0c97c;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .left-sub,
body.theme-dark:not([data-theme='black-gold']) .benefits-page .left-note {
  color: #dbc69e;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .rate-table th,
body.theme-dark:not([data-theme='black-gold']) .benefits-page .rate-table td {
  border-color: #5c4723;
  color: #edd8ad;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .rate-table th {
  background: #2c2317;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .rate-table td {
  background: rgba(28, 22, 14, 0.66);
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .table-note {
  color: #ac9367;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .upload-date-label {
  color: #c8ad78;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .club-block {
  border-color: #5c4723;
  background: rgba(20, 16, 11, 0.58);
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .club-title {
  color: #e8c98e;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .user-matrix-table td {
  border-right-color: #8c6f38;
  border-bottom-color: #8c6f38;
  background: rgba(24, 20, 14, 0.86);
  color: #ead2a0;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .metric-cell {
  color: #e4ca97;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .user-matrix-table {
  border-color: #c59a4a;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .user-matrix-table.tone-a { background: rgba(206, 165, 79, 0.085); }
body.theme-dark:not([data-theme='black-gold']) .benefits-page .user-matrix-table.tone-b { background: rgba(173, 138, 70, 0.075); }
body.theme-dark:not([data-theme='black-gold']) .benefits-page .user-matrix-table.tone-c { background: rgba(148, 116, 62, 0.075); }
body.theme-dark:not([data-theme='black-gold']) .benefits-page .user-matrix-table.tone-d { background: rgba(188, 152, 84, 0.08); }
body.theme-dark:not([data-theme='black-gold']) .benefits-page .user-matrix-table.tone-e { background: rgba(156, 126, 66, 0.075); }

body.theme-dark:not([data-theme='black-gold']) .benefits-page ::v-deep .el-input__inner,
body.theme-dark:not([data-theme='black-gold']) .benefits-page ::v-deep .el-button {
  border-color: #674f24;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page ::v-deep .el-input__inner {
  background: #18140f;
  color: #f0ddb5;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .actions ::v-deep .range-picker.el-date-editor {
  border-color: #674f24;
  background: #18140f;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .actions ::v-deep .range-picker .el-range-input {
  background: #18140f;
  color: #f0ddb5;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page .actions ::v-deep .range-picker .el-range-separator,
body.theme-dark:not([data-theme='black-gold']) .benefits-page .actions ::v-deep .range-picker .el-range__icon,
body.theme-dark:not([data-theme='black-gold']) .benefits-page .actions ::v-deep .range-picker .el-range__close-icon {
  color: #c8ad78;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-page ::v-deep .el-button--primary {
  border-color: #a97c35;
  background: linear-gradient(90deg, #725325 0%, #a87c38 55%, #c89b4b 100%);
}

@media (max-width: 1100px) {
  .benefits-shell {
    grid-template-columns: 1fr;
  }

  .panel-head {
    flex-direction: column;
  }

  .actions {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>

<style lang="scss">
body.theme-dark:not([data-theme='black-gold']) .benefits-upload-dialog {
  border: 1px solid #594520;
  border-radius: 12px;
  background: linear-gradient(160deg, #11100d 0%, #17130e 58%, #100d09 100%);
}

body.theme-dark:not([data-theme='black-gold']) .benefits-upload-dialog .el-dialog__title,
body.theme-dark:not([data-theme='black-gold']) .benefits-upload-dialog .el-upload__text {
  color: #f0d8a5;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-upload-dialog .el-upload-dragger {
  border-color: #6f5528;
  background: linear-gradient(180deg, rgba(33, 27, 18, 0.92) 0%, rgba(23, 19, 14, 0.96) 100%);
}

body.theme-dark:not([data-theme='black-gold']) .benefits-range-popper {
  border: 1px solid #5e4823 !important;
  background: linear-gradient(180deg, #1a150f 0%, #13100c 100%) !important;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-range-popper .el-picker-panel__body,
body.theme-dark:not([data-theme='black-gold']) .benefits-range-popper .el-date-range-picker__content,
body.theme-dark:not([data-theme='black-gold']) .benefits-range-popper .el-date-table td.in-range div,
body.theme-dark:not([data-theme='black-gold']) .benefits-range-popper .el-date-table td.start-date div,
body.theme-dark:not([data-theme='black-gold']) .benefits-range-popper .el-date-table td.end-date div {
  background: transparent;
  color: #e9d2a3;
}

body.theme-dark:not([data-theme='black-gold']) .benefits-range-popper .el-picker-panel__icon-btn,
body.theme-dark:not([data-theme='black-gold']) .benefits-range-popper .el-date-range-picker__header div,
body.theme-dark:not([data-theme='black-gold']) .benefits-range-popper .el-date-table th {
  color: #d9bc83;
}
</style>
