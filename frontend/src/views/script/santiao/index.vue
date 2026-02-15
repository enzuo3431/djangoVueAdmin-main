<template>
  <div class="app-container">
    <div class="page-header">
      <h2>三条配置</h2>
      <p>脚本相关的三条配置管理页面</p>
    </div>

    <el-card class="box-card">
      <div class="empty-tip">
        在这里编写“三条配置”的管理内容。
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'ScriptSantiao'
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
</style>
