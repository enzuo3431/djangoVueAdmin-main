<template>
  <div class="app-container tools-page">
    <div class="hero">
      <h2>批量生成昵称</h2>
      <p>支持类目 + 风格 + 强度 + 地域语感，点击单个名字即可复制</p>
    </div>
    <el-card class="panel" shadow="never">
      <div class="toolbar">
        <el-select v-model="category" popper-class="nick-dark-select-popper" style="width: 170px;">
          <el-option label="混合生成" value="mixed" />
          <el-option label="女生姓名" value="female_name" />
          <el-option label="女生昵称" value="female_nickname" />
          <el-option label="女生网名" value="female_netname" />
        </el-select>
        <el-select v-model="style" popper-class="nick-dark-select-popper" style="width: 160px;">
          <el-option label="默认风格" value="default" />
          <el-option label="可爱风" value="cute" />
          <el-option label="清冷风" value="cool" />
          <el-option label="文艺风" value="literary" />
          <el-option label="古风" value="ancient" />
          <el-option label="甜妹风" value="sweet" />
          <el-option label="风格混合" value="mixed" />
        </el-select>
        <el-select v-model="intensity" popper-class="nick-dark-select-popper" style="width: 120px;">
          <el-option label="强度弱" value="weak" />
          <el-option label="强度中" value="medium" />
          <el-option label="强度强" value="strong" />
        </el-select>
        <el-select v-model="region" popper-class="nick-dark-select-popper" style="width: 150px;">
          <el-option label="地域默认" value="default" />
          <el-option label="江南语感" value="jiangnan" />
          <el-option label="北方语感" value="beifang" />
          <el-option label="现代语感" value="modern" />
          <el-option label="地域混合" value="mixed" />
        </el-select>
        <el-input-number v-model="count" :min="1" :max="100" controls-position="right" />
        <el-button
          type="primary"
          class="generate-btn"
          :loading="loading"
          :disabled="loading || cooldownSeconds > 0"
          @click="handleGenerate"
        >
          {{ cooldownSeconds > 0 ? `${cooldownSeconds}s后可生成` : '生成' }}
        </el-button>
        <el-button type="success" plain @click="copyAll">复制全部</el-button>
      </div>
      <div class="hint">词库文件：<code>backend/apps/tools_management/nickname_vocab.py</code></div>
      <div class="name-wall">
        <div v-for="(name, idx) in list" :key="`${name}-${idx}`" class="name-pill" @click="copyOne(name)">{{ name }}</div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { generateNicknames } from '@/api/toolsManagement'

export default {
  name: 'ToolsNicknameIndex',
  data() {
    return {
      category: 'mixed',
      style: 'mixed',
      intensity: 'medium',
      region: 'default',
      count: 100,
      list: [],
      loading: false,
      cooldownSeconds: 0,
      cooldownTimer: null
    }
  },
  created() {
    this.handleGenerate()
  },
  beforeDestroy() {
    this.clearCooldownTimer()
  },
  methods: {
    handleGenerate() {
      if (this.loading || this.cooldownSeconds > 0) return
      this.loading = true
      generateNicknames({
        count: this.count,
        category: this.category,
        style: this.style,
        intensity: this.intensity,
        region: this.region
      }).then(res => {
        const payload = res.data || {}
        this.list = payload.items || []
      }).catch(() => {
      }).finally(() => {
        this.loading = false
        this.startCooldown(3)
      })
    },
    startCooldown(seconds) {
      this.clearCooldownTimer()
      this.cooldownSeconds = seconds
      this.cooldownTimer = setInterval(() => {
        if (this.cooldownSeconds <= 1) {
          this.clearCooldownTimer()
          this.cooldownSeconds = 0
          return
        }
        this.cooldownSeconds -= 1
      }, 1000)
    },
    clearCooldownTimer() {
      if (this.cooldownTimer) {
        clearInterval(this.cooldownTimer)
        this.cooldownTimer = null
      }
    },
    copyAll() {
      if (!this.list.length) {
        this.$message.warning('暂无可复制内容')
        return
      }
      navigator.clipboard.writeText(this.list.join('\n')).then(() => {
        this.$message.success('复制成功')
      })
    },
    copyOne(name) {
      navigator.clipboard.writeText(name).then(() => {
        this.$message.success(`已复制：${name}`)
      })
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
  background: linear-gradient(120deg, #1f5a85 0%, #2c8cbc 100%);
}
.panel {
  position: relative;
  overflow: hidden;
  border-radius: 14px;
}
.toolbar { display: flex; gap: 10px; align-items: center; margin-bottom: 12px; flex-wrap: wrap; }
.generate-btn {
  min-width: 132px;
  height: 40px;
  padding: 0 22px;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 1px;
}
.hint {
  margin: 4px 0 8px;
  color: #6a7e92;
  font-size: 12px;
}
.name-wall {
  margin-top: 8px;
  display: grid;
  grid-template-columns: repeat(10, minmax(0, 1fr));
  gap: 7px 8px;
}
.name-pill {
  padding: 5px 8px;
  border-radius: 8px;
  background: #f1f8ff;
  border: 1px solid #d6e8fb;
  text-align: center;
  color: #2d4e6f;
  cursor: pointer;
  font-size: 15px;
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: all 0.16s ease;
}
.name-pill:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(74, 133, 190, 0.22);
  border-color: #b7d5f2;
}
body.theme-dark:not([data-theme='black-gold']) .tools-page .hero {
  position: relative;
  border: 1px solid #624a22;
  background: linear-gradient(120deg, #1c1710 0%, #2b2215 48%, #1a150f 100%);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35), inset 0 0 0 1px rgba(229, 189, 110, 0.08);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .hero::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 14px;
  pointer-events: none;
  background: repeating-linear-gradient(
    -18deg,
    rgba(230, 192, 118, 0.06) 0,
    rgba(230, 192, 118, 0.06) 2px,
    rgba(0, 0, 0, 0) 2px,
    rgba(0, 0, 0, 0) 8px
  );
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .panel {
  border: 1px solid #5a4622;
  background: linear-gradient(160deg, #11100d 0%, #17130e 60%, #100e0b 100%);
  box-shadow: 0 0 0 1px rgba(229, 189, 110, 0.08), 0 14px 30px rgba(0, 0, 0, 0.38);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .panel ::v-deep .el-card__body {
  position: relative;
  background: transparent;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .panel::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 14px;
  pointer-events: none;
  background: repeating-linear-gradient(
    -20deg,
    rgba(226, 186, 104, 0.045) 0,
    rgba(226, 186, 104, 0.045) 1px,
    rgba(0, 0, 0, 0) 1px,
    rgba(0, 0, 0, 0) 7px
  );
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .toolbar {
  position: relative;
  z-index: 1;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page .hint {
  position: relative;
  z-index: 1;
  color: #bfa47a;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-input__inner,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-select .el-input__inner,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-input-number__decrease,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-input-number__increase {
  border-color: #604a22;
  background: #18140f;
  color: #f0ddb5;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-input__inner:focus,
body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-select .el-input__inner:focus {
  border-color: #ba9042;
  box-shadow: 0 0 0 1px rgba(186, 144, 66, 0.24) inset;
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-button--primary {
  border-color: #89662e;
  background: linear-gradient(90deg, #715224 0%, #9f7532 55%, #c09348 100%);
  box-shadow: 0 8px 20px rgba(148, 104, 36, 0.28);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .generate-btn.el-button--primary {
  min-width: 148px;
  height: 42px;
  border-color: #ac7d35;
  background: linear-gradient(90deg, #7a5926 0%, #b7893e 52%, #d3a859 100%);
  box-shadow: 0 10px 24px rgba(149, 108, 39, 0.35), 0 0 0 1px rgba(233, 191, 104, 0.22);
}

body.theme-dark:not([data-theme='black-gold']) .tools-page ::v-deep .el-button--success.is-plain {
  border-color: #6d5428;
  background: rgba(42, 33, 19, 0.84);
  color: #e3c587;
}

body.theme-dark:not([data-theme='black-gold']) .name-pill {
  position: relative;
  z-index: 1;
  background: linear-gradient(180deg, rgba(33, 27, 18, 0.96) 0%, rgba(24, 20, 15, 0.96) 100%);
  border-color: #5c4722;
  color: #f2deb1;
  box-shadow: inset 0 0 0 1px rgba(232, 194, 116, 0.06);
}

body.theme-dark:not([data-theme='black-gold']) .name-pill::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 8px;
  pointer-events: none;
  background: repeating-linear-gradient(
    -16deg,
    rgba(240, 204, 131, 0.05) 0,
    rgba(240, 204, 131, 0.05) 1px,
    rgba(0, 0, 0, 0) 1px,
    rgba(0, 0, 0, 0) 6px
  );
}

body.theme-dark:not([data-theme='black-gold']) .name-pill:hover {
  border-color: #c79a4b;
  color: #ffe6b8;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(226, 182, 94, 0.22);
}

@media (max-width: 1200px) {
  .name-wall {
    grid-template-columns: repeat(8, minmax(0, 1fr));
  }
}

@media (max-width: 992px) {
  .name-wall {
    grid-template-columns: repeat(6, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .name-wall {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
  .name-pill {
    font-size: 14px;
    padding: 4px 6px;
  }
}
</style>

<style lang="scss">
body.theme-dark:not([data-theme='black-gold']) .nick-dark-select-popper.el-popper[x-placement^='bottom'] .popper__arrow::after {
  border-bottom-color: #19150f !important;
}

body.theme-dark:not([data-theme='black-gold']) .nick-dark-select-popper.el-popper[x-placement^='top'] .popper__arrow::after {
  border-top-color: #19150f !important;
}

body.theme-dark:not([data-theme='black-gold']) .nick-dark-select-popper {
  border: 1px solid #644c23 !important;
  background: linear-gradient(180deg, #1a150f 0%, #13100c 100%) !important;
  box-shadow: 0 12px 26px rgba(0, 0, 0, 0.48), 0 0 0 1px rgba(224, 178, 93, 0.12) !important;
}

body.theme-dark:not([data-theme='black-gold']) .nick-dark-select-popper .el-select-dropdown__item {
  color: #ebd5a7 !important;
}

body.theme-dark:not([data-theme='black-gold']) .nick-dark-select-popper .el-select-dropdown__item.hover,
body.theme-dark:not([data-theme='black-gold']) .nick-dark-select-popper .el-select-dropdown__item:hover {
  background: linear-gradient(90deg, rgba(111, 83, 35, 0.34) 0%, rgba(74, 54, 24, 0.54) 100%) !important;
  color: #ffe2a4 !important;
}

body.theme-dark:not([data-theme='black-gold']) .nick-dark-select-popper .el-select-dropdown__item.selected {
  background: linear-gradient(90deg, rgba(146, 107, 43, 0.36) 0%, rgba(100, 72, 30, 0.6) 100%) !important;
  color: #ffd98f !important;
  font-weight: 600 !important;
}

body.theme-dark:not([data-theme='black-gold']) .nick-dark-select-popper .el-scrollbar__thumb {
  background: rgba(191, 147, 68, 0.6) !important;
}
</style>
