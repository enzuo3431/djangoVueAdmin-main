<template>
  <div class="login-page">
    <div class="split-left">
      <div class="grid-bg"></div>
      <div class="neon-glow neon-glow-1"></div>
      <div class="neon-glow neon-glow-2"></div>

      <div class="split-left-content">
        <h1 class="main-title">
          <span class="line line-1">让工作</span><br>
          <span class="line line-2"><span class="highlight">更高效</span></span><br>
          <span class="line line-3">更有成就感</span>
        </h1>

        <p class="subtitle">
          告别繁琐重复的工作，<strong>每天节省3小时</strong>，专注于真正重要的事情。
        </p>

        <div class="quote-section">
          <div class="quote-text">
            "成功不是终点，<strong>持续成长</strong>才是人生的意义。<br>
            每一天都比昨天更好，这就是进步。"
          </div>
          <div class="quote-author">— 致每一位奋斗者</div>
        </div>
      </div>
    </div>

    <div class="split-right">
      <div class="login-container">
        <div class="logo-mobile">
          <svg width="56" height="56" viewBox="0 0 56 56" fill="none">
            <defs>
              <linearGradient id="logo-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#ff9933" />
                <stop offset="100%" style="stop-color:#ffcc00" />
              </linearGradient>
            </defs>
            <rect width="56" height="56" rx="16" fill="url(#logo-grad)" />
            <path d="M28 18L20 26H23V32H26V27H30V32H33V26H36L28 18Z" fill="#0a0a0f" />
          </svg>
        </div>

        <div class="welcome">
          <h2>欢迎回来</h2>
          <p>登录您的账户继续高效工作</p>
        </div>

        <el-form
          ref="loginForm"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          autocomplete="on"
          @submit.native.prevent="handleLogin"
        >
          <div class="form-group">
            <label class="field-label" for="username">用户名</label>
            <el-form-item prop="username" class="field-item">
              <div class="input-wrapper">
                <el-input
                  ref="username"
                  v-model="loginForm.username"
                  placeholder="请输入用户名"
                  name="username"
                  type="text"
                  tabindex="1"
                  autocomplete="on"
                >
                  <svg slot="prefix" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                  </svg>
                </el-input>
              </div>
            </el-form-item>
          </div>

          <div class="form-group">
            <label class="field-label" for="password">密码</label>
            <el-form-item prop="password" class="field-item">
              <div class="input-wrapper">
                <el-input
                  ref="password"
                  v-model="loginForm.password"
                  :type="passwordType"
                  placeholder="请输入密码"
                  name="password"
                  tabindex="2"
                  autocomplete="on"
                  @keyup.enter.native="handleLogin"
                >
                  <svg slot="prefix" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                    <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                  </svg>
                </el-input>
              </div>
            </el-form-item>
          </div>

          <div class="form-options">
            <div class="remember">
              <input id="remember" type="checkbox">
              <label for="remember">记住我</label>
            </div>
            <a class="forgot-link" href="javascript:void(0)">忘记密码？</a>
          </div>

          <el-button
            :loading="loading"
            class="login-btn"
            type="primary"
            @click.native.prevent="handleLogin"
          >
            登录
          </el-button>

          <div class="divider">
            <span>或使用以下方式登录</span>
          </div>

          <div class="social-login">
            <button class="social-btn" type="button" @click="showSocialUnavailable">
              <svg viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
              </svg>
              Google
            </button>
            <button class="social-btn" type="button" @click="showSocialUnavailable">
              <svg viewBox="0 0 24 24" fill="#07c160">
                <path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 0 1 .213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 0 0 .167-.054l1.903-1.114a.864.864 0 0 1 .717-.098 10.16 10.16 0 0 0 2.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 3.882-1.98 5.853-1.838-.576-3.583-4.196-6.348-8.596-6.348zM5.785 5.991c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 0 1-1.162 1.178A1.17 1.17 0 0 1 4.623 7.17c0-.651.52-1.18 1.162-1.18zm5.813 0c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 0 1-1.162 1.178 1.17 1.17 0 0 1-1.162-1.178c0-.651.52-1.18 1.162-1.18zm5.34 2.867c-1.797-.052-3.746.512-5.28 1.786-1.72 1.428-2.687 3.72-1.78 6.22.942 2.453 3.666 4.229 6.884 4.229.826 0 1.622-.12 2.361-.336a.722.722 0 0 1 .598.082l1.584.926a.272.272 0 0 0 .14.047c.134 0 .24-.111.24-.247 0-.06-.023-.12-.038-.177l-.327-1.233a.582.582 0 0 1-.023-.156.49.49 0 0 1 .201-.398C23.024 18.48 24 16.82 24 14.98c0-3.21-2.931-5.837-6.656-6.088V8.89c-.135-.01-.27-.027-.407-.03zm-2.53 3.274c.535 0 .969.44.969.982a.976.976 0 0 1-.969.983.976.976 0 0 1-.969-.983c0-.542.434-.982.97-.982zm4.844 0c.535 0 .969.44.969.982a.976.976 0 0 1-.969.983.976.976 0 0 1-.969-.983c0-.542.434-.982.969-.982z" />
              </svg>
              WeChat
            </button>
          </div>

          <p class="signup-link">
            还没有账户？<a href="javascript:void(0)">立即注册</a>
          </p>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Login',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入用户名'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('密码不能少于6位'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      passwordType: 'password',
      loading: false,
      showDialog: false,
      redirect: undefined,
      otherQuery: {}
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        const query = route.query
        if (query) {
          this.redirect = query.redirect
          this.otherQuery = this.getOtherQuery(query)
        }
      },
      immediate: true
    }
  },
  mounted() {
    if (this.loginForm.username === '') {
      this.$refs.username.focus()
    } else if (this.loginForm.password === '') {
      this.$refs.password.focus()
    }
  },
  methods: {
    ...mapActions(['user/login']),
    showSocialUnavailable() {
      this.$message({
        message: '暂不支持此登录方式',
        type: 'warning',
        duration: 2000
      })
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/login', this.loginForm)
            .then(() => {
              this.$message({
                message: '登录成功',
                type: 'success',
                duration: 2000
              })
              this.$router.push({ path: this.redirect || '/', query: this.otherQuery })
              this.loading = false
            })
            .catch(error => {
              console.error('Login error:', error)
              // 如果错误已经被 request.js 处理过，不再重复显示
              if (!error.isHandled) {
                this.$message({
                  message: error.response?.data?.message || error.message || '登录失败',
                  type: 'error',
                  duration: 3000
                })
              }
              this.loading = false
            })
        } else {
          return false
        }
      })
    },
    getOtherQuery(query) {
      return Object.keys(query).reduce((acc, cur) => {
        if (cur !== 'redirect') {
          acc[cur] = query[cur]
        }
        return acc
      }, {})
    }
  }
}
</script>

<style lang="scss" scoped>
$bg-dark: #0a0a0f;

.login-page {
  min-height: 100%;
  width: 100%;
  display: flex;
  overflow: hidden;
  background: $bg-dark;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.split-left {
  flex: 1;
  background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 60px;
  position: relative;
  overflow: hidden;
}

.grid-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    linear-gradient(rgba(0, 255, 136, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 136, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  opacity: 0.5;
}

.neon-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.15;
}

.neon-glow-1 {
  width: 400px;
  height: 400px;
  background: #00ff88;
  top: -150px;
  left: -150px;
  animation: float-glow 8s ease-in-out infinite alternate;
}

.neon-glow-2 {
  width: 300px;
  height: 300px;
  background: #00d4ff;
  bottom: -100px;
  right: -100px;
  animation: float-glow 10s ease-in-out infinite alternate;
  animation-delay: -4s;
}

.split-left-content {
  position: relative;
  z-index: 2;
  max-width: 520px;
}

.main-title {
  font-size: 56px;
  font-weight: 900;
  line-height: 1.15;
  margin-bottom: 24px;
  position: relative;
}

.main-title .line {
  display: block;
  position: relative;
  z-index: 2;
}

.main-title .line-1 {
  background: linear-gradient(180deg, #fff7e6 0%, #ffd9a0 50%, #ffb366 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow:
    0 0 20px rgba(255, 200, 100, 0.6),
    0 0 40px rgba(255, 200, 100, 0.4);
  animation: text-flicker 3s ease-in-out infinite alternate;
}

.main-title .line-2 {
  position: relative;
  display: inline-block;
}

.main-title .highlight {
  background: linear-gradient(135deg, #ff6b35 0%, #f7931e 25%, #ffcc00 50%, #ff6b35 75%, #f7931e 100%);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: fire-gradient 3s ease infinite;
  position: relative;
  z-index: 2;
  filter: drop-shadow(0 0 20px rgba(255, 107, 53, 0.8))
    drop-shadow(0 0 40px rgba(255, 155, 30, 0.6));
}

.main-title .highlight::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: -10px;
  right: -10px;
  height: 6px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(255, 107, 53, 0.8) 20%,
    rgba(255, 204, 0, 1) 50%,
    rgba(255, 107, 53, 0.8) 80%,
    transparent 100%);
  border-radius: 3px;
  filter: blur(4px);
  animation: fire-glow 2s ease-in-out infinite alternate;
}

.main-title .line-2::before,
.main-title .line-2::after {
  content: '🔥';
  position: absolute;
  font-size: 16px;
  animation: float-flame 2s ease-in-out infinite;
  z-index: 1;
}

.main-title .line-2::before {
  top: -25px;
  left: 10%;
  animation-delay: 0s;
  opacity: 0.9;
  filter: drop-shadow(0 0 10px rgba(255, 107, 53, 0.8));
}

.main-title .line-2::after {
  top: -20px;
  right: 15%;
  animation-delay: -1s;
  font-size: 14px;
  opacity: 0.7;
  filter: drop-shadow(0 0 10px rgba(255, 204, 0, 0.8));
}

.main-title .line-3 {
  background: linear-gradient(180deg, #ffe8d6 0%, #ffc9a8 50%, #ffb083 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow:
    0 0 20px rgba(255, 190, 120, 0.6),
    0 0 40px rgba(255, 170, 100, 0.4);
  animation: text-flicker 3s ease-in-out infinite alternate;
  animation-delay: -1.5s;
}

.subtitle {
  color: rgba(255, 220, 180, 0.7);
  font-size: 19px;
  line-height: 1.7;
  margin-bottom: 40px;
}

.subtitle strong {
  color: #ff9933;
  font-weight: 600;
  text-shadow: 0 0 10px rgba(255, 153, 51, 0.5);
}

.quote-section {
  padding: 28px;
  background: rgba(255, 150, 80, 0.08);
  border: 1px solid rgba(255, 180, 120, 0.2);
  border-radius: 20px;
  position: relative;
}

.quote-section::before {
  content: '"';
  position: absolute;
  top: 10px;
  left: 20px;
  font-size: 60px;
  color: #ff9933;
  opacity: 0.3;
  font-family: Georgia, serif;
  line-height: 1;
}

.quote-text {
  font-size: 17px;
  color: rgba(255, 230, 200, 0.85);
  line-height: 1.8;
  font-style: italic;
  padding-left: 20px;
}

.quote-text strong {
  color: #ff7722;
  font-style: normal;
}

.quote-author {
  margin-top: 16px;
  font-size: 14px;
  color: rgba(255, 200, 150, 0.6);
  text-align: right;
}

.split-right {
  flex: 1;
  background: linear-gradient(180deg, #0d1117 0%, #010409 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  position: relative;
}

.login-container {
  width: 100%;
  max-width: 400px;
  position: relative;
  z-index: 2;
}

.logo-mobile {
  display: none;
  text-align: center;
  margin-bottom: 32px;
}

.welcome {
  margin-bottom: 40px;
}

.welcome h2 {
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, #ffe8d6 0%, #ffb366 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
}

.welcome p {
  color: rgba(255, 200, 150, 0.6);
  font-size: 15px;
}

.form-group {
  margin-bottom: 20px;
}

.field-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 8px;
}

.input-wrapper {
  position: relative;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.remember {
  display: flex;
  align-items: center;
  gap: 8px;
}

.remember input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #ff9933;
}

.remember label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
}

.forgot-link {
  color: #ff9933;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.forgot-link:hover {
  text-shadow: 0 0 10px rgba(255, 153, 51, 0.5);
}

.login-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #ff9933 0%, #ffcc00 100%);
  color: #0a0a0f;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(255, 153, 51, 0.3);
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(255, 153, 51, 0.4);
}

.divider {
  display: flex;
  align-items: center;
  margin: 28px 0;
  color: rgba(255, 255, 255, 0.3);
  font-size: 14px;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
}

.divider span {
  padding: 0 12px;
}

.social-login {
  display: flex;
  gap: 12px;
}

.social-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.03);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
}

.social-btn:hover {
  border-color: rgba(255, 153, 51, 0.5);
  background: rgba(255, 153, 51, 0.1);
  color: #ff9933;
}

.social-btn svg {
  width: 20px;
  height: 20px;
}

.signup-link {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
}

.signup-link a {
  color: #ff9933;
  text-decoration: none;
  font-weight: 600;
}

@keyframes float-glow {
  0% { transform: translate(0, 0) scale(1); opacity: 0.1; }
  100% { transform: translate(30px, -30px) scale(1.1); opacity: 0.2; }
}

@keyframes fire-gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes fire-glow {
  0% {
    opacity: 0.6;
    transform: scaleX(0.9);
  }
  100% {
    opacity: 1;
    transform: scaleX(1.1);
  }
}

@keyframes float-flame {
  0%, 100% {
    transform: translateY(0) scale(1) rotate(-5deg);
  }
  50% {
    transform: translateY(-8px) scale(1.1) rotate(5deg);
  }
}

@keyframes text-flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.92; }
}

::v-deep .el-form-item {
  margin-bottom: 0;
}

::v-deep .el-form-item__content {
  line-height: 1;
}

::v-deep .el-input__inner {
  width: 100%;
  padding: 13px 14px 13px 44px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  font-size: 15px;
  transition: all 0.3s ease;
  color: #fff;
  height: 48px;
}

::v-deep .el-input__inner::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

::v-deep .el-input__inner:focus {
  outline: none;
  border-color: #ff9933;
  background: rgba(255, 153, 51, 0.05);
  box-shadow: 0 0 20px rgba(255, 153, 51, 0.15);
}

::v-deep .el-input__prefix {
  left: 14px;
  height: 100%;
  display: flex;
  align-items: center;
}

::v-deep .el-input__prefix svg {
  width: 20px;
  height: 20px;
  color: rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

::v-deep .el-input.is-focus .el-input__prefix svg {
  color: #ff9933;
  filter: drop-shadow(0 0 8px rgba(255, 153, 51, 0.5));
}

::v-deep .el-form-item__error {
  color: #ff6b6b;
  font-size: 12px;
  margin-top: 6px;
}

@media (max-width: 900px) {
  .login-page {
    flex-direction: column;
  }

  .split-left {
    display: none;
  }

  .split-right {
    padding: 24px;
    min-height: 100vh;
  }

  .logo-mobile {
    display: block;
  }

  .welcome h2 {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .split-right {
    padding: 20px;
  }

  .login-container {
    max-width: 100%;
  }

  .welcome h2 {
    font-size: 22px;
  }

  .social-login {
    flex-direction: column;
  }
}

@supports (padding: max(0px)) {
  .split-right {
    padding-left: max(40px, env(safe-area-inset-left));
    padding-right: max(40px, env(safe-area-inset-right));
  }
}
</style>
