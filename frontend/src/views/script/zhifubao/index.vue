<template>
  <div class="app-container">
    <div class="page-header">
      <h2>支付宝配置</h2>
      <p>请在这里编写页面内容</p>
    </div>

    <el-card class="box-card">
      <div class="empty-tip">
        页面已创建：支付宝配置
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'ScriptZhifubaoIndex'
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
