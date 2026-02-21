<template>
  <div class="app-container tools-page">
    <div class="split-shell">
      <div class="split-layout">
        <el-card class="panel info-panel" shadow="never">
          <h3>使用说明</h3>
          <ul class="guide-list">
            <li>仅支持上传 <strong>TXT</strong> 文本文件</li>
            <li>文件内容按行进行拆分</li>
            <li>可选择按 <strong>文件数量</strong> 或 <strong>每个文件条数</strong> 拆分</li>
            <li>提交后将 <strong>自动下载</strong></li>
            <li>拆分结果以压缩包形式返回（ZIP）</li>
          </ul>
          <p class="warn">请勿关闭页面，直到下载完成</p>
          <p class="footnote">本工具不会保存你的文件，处理完成后即释放。</p>
        </el-card>

        <el-card class="panel tool-panel" shadow="never">
          <h2 class="panel-title">文件拆分工具</h2>
          <div class="panel-divider" />

          <el-upload
            ref="uploadRef"
            class="upload-block"
            drag
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            accept=".txt"
          >
            <i class="el-icon-upload" />
            <div class="el-upload__text">点击选择文件，或拖拽到此处</div>
          </el-upload>

          <div class="file-state" :class="{ selected: !!file }">
            {{ file ? `已选择：${file.name}` : '未选择文件' }}
          </div>

          <el-select v-model="mode" class="field-control" popper-class="split-mode-popper">
            <el-option label="按文件数量平均拆分" value="count" />
            <el-option label="按每份行数拆分" value="lines" />
          </el-select>

          <el-input
            v-if="mode === 'count'"
            v-model.number="splitCount"
            class="field-control"
            placeholder="请输入拆分成多少个文件"
            type="number"
            :min="2"
            :max="500"
          />
          <el-input
            v-else
            v-model.number="linesPerFile"
            class="field-control"
            placeholder="请输入每份包含多少行"
            type="number"
            :min="1"
            :max="200000"
          />

          <el-button class="run-btn" type="primary" :loading="loading" @click="handleRun">
            开始拆分并下载
          </el-button>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import { runFileSplit } from '@/api/toolsManagement'

export default {
  name: 'ToolsFileSplitIndex',
  data() {
    return {
      mode: 'count',
      splitCount: null,
      linesPerFile: null,
      file: null,
      loading: false
    }
  },
  methods: {
    handleFileChange(file) {
      this.file = file.raw
    },
    handleFileRemove() {
      this.file = null
    },
    handleRun() {
      if (!this.file) {
        this.$message.warning('请先上传文件')
        return
      }
      if (this.mode === 'count' && (!this.splitCount || this.splitCount < 2)) {
        this.$message.warning('请输入正确的拆分文件数（>=2）')
        return
      }
      if (this.mode === 'lines' && (!this.linesPerFile || this.linesPerFile < 1)) {
        this.$message.warning('请输入正确的每份行数（>=1）')
        return
      }
      this.loading = true
      const formData = new FormData()
      formData.append('file', this.file)
      formData.append('mode', this.mode)
      if (this.mode === 'count') formData.append('split_count', this.splitCount)
      if (this.mode === 'lines') formData.append('lines_per_file', this.linesPerFile)

      runFileSplit(formData).then(res => {
        const data = res.data || {}
        const base64 = data.content_base64 || ''
        if (!base64) {
          this.$message.error('拆分结果为空')
          this.loading = false
          return
        }
        const bytes = window.atob(base64)
        const len = bytes.length
        const arr = new Uint8Array(len)
        for (let i = 0; i < len; i++) arr[i] = bytes.charCodeAt(i)
        const blob = new Blob([arr], { type: data.mime_type || 'application/zip' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = data.filename || 'split_result.zip'
        link.click()
        URL.revokeObjectURL(link.href)
        this.$message.success(`拆分成功，共${data.parts || 0}个文件`)
        this.loading = false
      }).catch(() => { this.loading = false })
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

.split-shell {
  max-width: 1120px;
  margin: 0 auto;
}

.split-layout {
  display: grid;
  grid-template-columns: 320px minmax(0, 1fr);
  gap: 22px;
}

.info-panel h3 {
  margin: 0 0 14px;
  font-size: 22px;
  font-weight: 700;
}

.guide-list {
  margin: 0;
  padding-left: 0;
  list-style: none;
  line-height: 1.75;
  font-size: 15px;
  color: #3f4f5c;
}

.guide-list strong {
  color: #192a3a;
}

.warn {
  margin: 12px 0 0;
  color: #f2592f;
  font-weight: 600;
  font-size: 15px;
}

.footnote {
  margin: 150px 0 0;
  padding-top: 14px;
  border-top: 1px dashed #d8dbe2;
  color: #7f8b97;
  line-height: 1.6;
  font-size: 14px;
}

.tool-panel {
  padding-bottom: 4px;
}

.panel-title {
  margin: 2px 0 10px;
  text-align: center;
  font-size: 30px;
  font-weight: 700;
}

.panel-divider {
  border-top: 1px dashed #d2d6dd;
  margin-bottom: 14px;
}

.upload-block {
  margin-bottom: 10px;
}

.tools-page ::v-deep .upload-block .el-upload {
  width: 100%;
}

.tools-page ::v-deep .upload-block .el-upload-dragger {
  width: 100%;
  min-height: 180px;
  border-color: #cfd5dd;
}

.file-state {
  text-align: center;
  color: #ff5f43;
  font-size: 19px;
  margin-bottom: 12px;
}

.file-state.selected {
  color: #2f8f5c;
}

.field-control {
  display: block;
  width: 100%;
  margin-bottom: 10px;
}

.run-btn {
  width: 100%;
  height: 44px;
  font-size: 15px;
  font-weight: 700;
}

body.theme-dark:not([data-theme='black-gold']) .info-panel h3,
body.theme-dark:not([data-theme='black-gold']) .panel-title {
  color: #f2d7a3;
}

body.theme-dark:not([data-theme='black-gold']) .guide-list {
  color: #d5bf98;
}

body.theme-dark:not([data-theme='black-gold']) .guide-list strong {
  color: #ffe0a4;
}

body.theme-dark:not([data-theme='black-gold']) .footnote {
  border-top-color: #5b4723;
  color: #a98f65;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .panel {
  position: relative;
  border: 1px solid #594520;
  background: linear-gradient(160deg, #11100d 0%, #17130e 58%, #100d09 100%);
  box-shadow: 0 0 0 1px rgba(229, 189, 110, 0.08), 0 14px 30px rgba(0, 0, 0, 0.4);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .panel::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: 14px;
  background: repeating-linear-gradient(
    -20deg,
    rgba(226, 186, 104, 0.04) 0,
    rgba(226, 186, 104, 0.04) 1px,
    rgba(0, 0, 0, 0) 2px,
    rgba(0, 0, 0, 0) 7px
  );
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .panel-divider {
  border-top-color: #5a4521;
}

body.theme-dark:not([data-theme='black-gold']) .file-state {
  color: #ff8b76;
}

body.theme-dark:not([data-theme='black-gold']) .file-state.selected {
  color: #a7e8bb;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .panel ::v-deep .el-card__body {
  position: relative;
  background: transparent;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-input__inner,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-input-number__decrease,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-input-number__increase {
  border-color: #624c24;
  background: #18140f;
  color: #f2dfb5;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-upload-dragger {
  border-color: #6f5528;
  background: linear-gradient(180deg, rgba(33, 27, 18, 0.92) 0%, rgba(23, 19, 14, 0.96) 100%);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-upload__text,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-upload__tip,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-upload-dragger .el-icon-upload {
  color: #e2c38a;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .run-btn.el-button--primary {
  height: 44px;
  border-color: #a97c35;
  background: linear-gradient(90deg, #725325 0%, #a87c38 55%, #c89b4b 100%);
  box-shadow: 0 10px 24px rgba(150, 108, 37, 0.34);
  font-weight: 700;
  letter-spacing: 1px;
}

@media (max-width: 1100px) {
  .split-layout {
    grid-template-columns: 1fr;
  }

  .footnote {
    margin-top: 26px;
  }
}
</style>

<style lang="scss">
body.theme-dark:not([data-theme='black-gold']) .split-mode-popper {
  border: 1px solid #644c23 !important;
  background: linear-gradient(180deg, #1a150f 0%, #13100c 100%) !important;
  box-shadow: 0 12px 26px rgba(0, 0, 0, 0.48), 0 0 0 1px rgba(224, 178, 93, 0.12) !important;
}

body.theme-dark:not([data-theme='black-gold']) .split-mode-popper .el-select-dropdown__item {
  color: #ebd5a7 !important;
}

body.theme-dark:not([data-theme='black-gold']) .split-mode-popper .el-select-dropdown__item.hover,
body.theme-dark:not([data-theme='black-gold']) .split-mode-popper .el-select-dropdown__item:hover {
  background: linear-gradient(90deg, rgba(111, 83, 35, 0.34) 0%, rgba(74, 54, 24, 0.54) 100%) !important;
  color: #ffe2a4 !important;
}

body.theme-dark:not([data-theme='black-gold']) .split-mode-popper .el-select-dropdown__item.selected {
  background: linear-gradient(90deg, rgba(146, 107, 43, 0.36) 0%, rgba(100, 72, 30, 0.6) 100%) !important;
  color: #ffd98f !important;
  font-weight: 600 !important;
}
</style>
