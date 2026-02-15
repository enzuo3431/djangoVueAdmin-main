const fs = require('fs')
const path = require('path')

function usage() {
  console.log('Usage: node scripts/create-page.js <component_path> [title]')
  console.log('Example: node scripts/create-page.js script/santiao/index "三条配置"')
}

function toTitle(input) {
  if (!input) return '新页面'
  return String(input)
}

function normalizeComponentPath(input) {
  const raw = String(input || '').trim().replace(/\\/g, '/')
  if (!raw) return ''
  if (raw.startsWith('/')) return raw.slice(1)
  return raw
}

function ensureSafePath(componentPath) {
  if (componentPath.includes('..')) return false
  if (!/^[a-zA-Z0-9/_-]+$/.test(componentPath)) return false
  return true
}

function makeVueTemplate(title, name) {
  return `<template>
  <div class="app-container">
    <div class="page-header">
      <h2>${title}</h2>
      <p>请在这里编写页面内容</p>
    </div>

    <el-card class="box-card">
      <div class="empty-tip">
        页面已创建：${title}
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: '${name}'
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

.empty-tip {
  color: #909399;
  padding: 20px 10px;
}
</style>
`
}

function toComponentName(componentPath) {
  const parts = componentPath.split('/').filter(Boolean)
  const cleaned = parts.map(p => p.replace(/[^a-zA-Z0-9]/g, ''))
  const pascal = cleaned.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join('')
  return pascal || 'AutoPage'
}

function main() {
  const [, , componentArg, titleArg] = process.argv
  if (!componentArg) {
    usage()
    process.exit(1)
  }

  const componentPath = normalizeComponentPath(componentArg)
  if (!ensureSafePath(componentPath)) {
    console.error('Invalid component_path. Use letters, numbers, "-", "_", and "/".')
    process.exit(1)
  }

  const title = toTitle(titleArg || componentPath.split('/').slice(-1)[0])
  const componentName = toComponentName(componentPath)

  const viewsRoot = path.resolve(__dirname, '..', 'frontend', 'src', 'views')
  const targetPath = path.join(viewsRoot, `${componentPath}.vue`)
  const targetDir = path.dirname(targetPath)

  if (fs.existsSync(targetPath)) {
    console.error(`File already exists: ${targetPath}`)
    process.exit(1)
  }

  fs.mkdirSync(targetDir, { recursive: true })
  fs.writeFileSync(targetPath, makeVueTemplate(title, componentName), 'utf8')
  console.log(`Created: ${targetPath}`)
}

main()
