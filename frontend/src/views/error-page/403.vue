<template>
  <div class="error-page">
    <div class="error-code">4<span>0</span>3</div>
    <div class="error-desc">抱歉，您没有权限访问该页面</div>
    <div class="error-detail">请联系管理员获取相应权限</div>
    <div class="error-handle">
      <router-link to="/">
        <el-button type="primary" size="large">返回首页</el-button>
      </router-link>
      <el-button class="error-btn" type="info" size="large" @click="goBack">返回上一页</el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Error403',
  methods: {
    goBack() {
      this.$router.go(-1)
    }
  }
}
</script>

<style lang="scss" scoped>
.error-page {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background: #f0f0f0;

  .error-code {
    line-height: 1;
    font-size: 250px;
    font-weight: bolder;
    color: #2d8cf0;

    span {
      color: #ed4014;
    }
  }

  .error-desc {
    font-size: 30px;
    color: #777;
    margin-top: 20px;
  }

  .error-detail {
    font-size: 16px;
    color: #999;
    margin-top: 10px;
  }

  .error-handle {
    margin-top: 30px;
    padding-bottom: 200px;

    .error-btn {
      margin-left: 100px;
    }
  }
}
</style>
