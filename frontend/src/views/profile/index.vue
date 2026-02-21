<template>
  <div class="profile-container">
    <div class="profile-content">
      <div class="profile-banner">
        <div class="banner-title">个人中心</div>
        <div class="banner-sub">账户资料与安全设置</div>
      </div>

      <el-row :gutter="20" class="profile-grid">
        <el-col :xs="24" :sm="24" :lg="8" class="top-card-col">
          <el-card class="user-card">
          <div class="profile-hero">
            <div class="avatar-section">
              <div class="avatar-click" :class="{ uploading: avatarUploading }" @click="handleAvatarClick">
                <el-avatar :size="96" :src="userInfo.avatar || ''" icon="el-icon-user-solid" />
                <div class="avatar-mask">
                  <i class="el-icon-camera" />
                  <span>{{ avatarUploading ? '上传中...' : '更换头像' }}</span>
                </div>
              </div>
              <input
                ref="avatarInput"
                type="file"
                accept="image/*"
                class="avatar-input"
                @change="handleAvatarSelected"
              >
            </div>
            <div class="info-section">
              <h3>{{ userInfo.nickname || userInfo.username || '用户' }}</h3>
              <div class="role-group">
                <el-tag v-for="(role, index) in userInfo.roles" :key="index" size="small">{{ role.name }}</el-tag>
              </div>
              <div class="meta-row">
                <div class="meta-item">
                  <span class="meta-label">邮箱</span>
                  <span class="meta-value">{{ userInfo.email || '-' }}</span>
                </div>
                <div v-if="userInfo.phone" class="meta-item">
                  <span class="meta-label">手机号</span>
                  <span class="meta-value">{{ userInfo.phone }}</span>
                </div>
              </div>
              <div class="identity-pills">
                <span class="identity-pill">账号：{{ userInfo.username || '-' }}</span>
                <span class="identity-pill">角色数：{{ (userInfo.roles || []).length }}</span>
              </div>
            </div>
          </div>
          <div class="stats-row">
            <div class="stat-item">
              <h4>{{ userInfo.username || '-' }}</h4>
              <span>账号</span>
            </div>
            <div class="stat-item">
              <h4>{{ userInfo.gender || '-' }}</h4>
              <span>性别</span>
            </div>
          </div>
          </el-card>
        </el-col>

        <el-col :xs="24" :sm="24" :lg="16" class="top-card-col">
          <el-card class="form-card section-card info-card">
          <div slot="header" class="card-header">
            <span>基本信息</span>
          </div>
          <el-form
            ref="profileForm"
            :model="profileForm"
            :rules="profileRules"
            label-width="100px"
            class="profile-form"
          >
            <el-form-item label="用户名" prop="username">
              <el-input v-model="profileForm.username" disabled />
            </el-form-item>
            <el-form-item label="昵称" prop="nickname">
              <el-input v-model="profileForm.nickname" placeholder="请输入昵称" />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="profileForm.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="profileForm.phone" placeholder="请输入手机号" />
            </el-form-item>
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="profileForm.gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="loading" @click="handleUpdate">
                保存修改
              </el-button>
            </el-form-item>
          </el-form>
          </el-card>
        </el-col>

        <el-col :xs="24" :sm="24" :lg="24" class="password-col">
          <el-card class="password-card section-card">
          <div slot="header" class="card-header">
            <span>修改密码</span>
          </div>
          <el-form
            ref="passwordForm"
            :model="passwordForm"
            :rules="passwordRules"
            label-width="100px"
            class="password-form"
          >
            <el-form-item label="旧密码" prop="old_password">
              <el-input
                v-model="passwordForm.old_password"
                type="password"
                placeholder="请输入旧密码"
                show-password
              />
            </el-form-item>
            <el-form-item label="新密码" prop="new_password">
              <el-input
                v-model="passwordForm.new_password"
                type="password"
                placeholder="请输入新密码（至少6位）"
                show-password
              />
            </el-form-item>
            <el-form-item label="确认密码" prop="confirm_password">
              <el-input
                v-model="passwordForm.confirm_password"
                type="password"
                placeholder="请再次输入新密码"
                show-password
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="passwordLoading" @click="handleChangePassword">
                修改密码
              </el-button>
            </el-form-item>
          </el-form>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { updateProfile, changePassword, uploadAvatar } from '@/api/auth'
import { mapGetters } from 'vuex'

export default {
  name: 'Profile',
  data() {
    // 密码确认验证
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.passwordForm.new_password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }

    return {
      loading: false,
      passwordLoading: false,
      avatarUploading: false,
      profileForm: {
        username: '',
        nickname: '',
        email: '',
        phone: '',
        gender: ''
      },
      profileRules: {
        email: [
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        phone: [
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ]
      },
      passwordForm: {
        old_password: '',
        new_password: '',
        confirm_password: ''
      },
      passwordRules: {
        old_password: [
          { required: true, message: '请输入旧密码', trigger: 'blur' }
        ],
        new_password: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, message: '密码不能少于6位', trigger: 'blur' }
        ],
        confirm_password: [
          { required: true, message: '请再次输入新密码', trigger: 'blur' },
          { validator: validateConfirmPassword, trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters(['name', 'avatar', 'roles', 'nickname', 'email', 'phone', 'gender']),
    userInfo() {
      return {
        username: this.name,
        nickname: this.nickname,
        avatar: this.avatar,
        roles: this.roles,
        email: this.email,
        phone: this.phone,
        gender: this.gender
      }
    }
  },
  created() {
    this.initData()
  },
  methods: {
    initData() {
      this.profileForm.username = this.name
      this.profileForm.nickname = this.nickname || this.name
      this.profileForm.email = this.email || ''
      this.profileForm.phone = this.phone || ''
      this.profileForm.gender = this.gender || ''
      // 获取最新用户信息并同步表单
      this.$store.dispatch('user/getInfo').then(() => {
        this.profileForm.username = this.name
        this.profileForm.nickname = this.nickname || this.name
        this.profileForm.email = this.email || ''
        this.profileForm.phone = this.phone || ''
        this.profileForm.gender = this.gender || ''
      }).catch(() => {
        // 获取用户信息失败时不做处理，避免干扰用户
      })
    },
    handleUpdate() {
      this.$refs.profileForm.validate(valid => {
        if (valid) {
          this.loading = true
          updateProfile(this.profileForm).then(() => {
            this.$message({
              message: '更新成功',
              type: 'success',
              duration: 2000
            })
            // 更新用户信息
            this.$store.dispatch('user/getInfo')
          }).catch(error => {
            const errorMsg = error.response?.data?.message || error.message || '更新失败'
            this.$message({
              message: errorMsg,
              type: 'error',
              duration: 3000
            })
          }).finally(() => {
            this.loading = false
          })
        }
      })
    },
    handleChangePassword() {
      this.$refs.passwordForm.validate(valid => {
        if (valid) {
          this.passwordLoading = true
          changePassword({
            old_password: this.passwordForm.old_password,
            new_password: this.passwordForm.new_password
          }).then(() => {
            this.$message({
              message: '修改密码成功，请重新登录',
              type: 'success',
              duration: 2000
            })
            this.passwordForm = {
              old_password: '',
              new_password: '',
              confirm_password: ''
            }
            // 清除本地状态
            this.$store.dispatch('user/resetToken')
            // 跳转到登录页
            setTimeout(() => {
              this.$router.replace('/login')
            }, 1000)
          }).catch(error => {
            const errorMsg = error.response?.data?.message || error.message || '修改密码失败'
            this.$message({
              message: errorMsg,
              type: 'error',
              duration: 3000
            })
          }).finally(() => {
            this.passwordLoading = false
          })
        }
      })
    },
    handleAvatarClick() {
      if (this.$refs.avatarInput) {
        this.$refs.avatarInput.click()
      }
    },
    handleAvatarSelected(event) {
      const file = event.target.files && event.target.files[0]
      if (!file) return
      const isImage = file.type && file.type.startsWith('image/')
      const isLt2M = file.size <= 2 * 1024 * 1024

      if (!isImage) {
        this.$message({
          message: '请选择图片文件',
          type: 'warning',
          duration: 2000
        })
        event.target.value = ''
        return
      }

      if (!isLt2M) {
        this.$message({
          message: '头像大小不能超过 2MB',
          type: 'warning',
          duration: 2000
        })
        event.target.value = ''
        return
      }

      const formData = new FormData()
      formData.append('file', file)
      this.avatarUploading = true
      uploadAvatar(formData).then(response => {
        if (response && response.data && response.data.avatar) {
          this.$store.commit('user/SET_AVATAR', response.data.avatar)
          this.$message({
            message: '头像更新成功',
            type: 'success',
            duration: 2000
          })
        }
      }).catch(() => {
        this.$message({
          message: '头像上传失败',
          type: 'error',
          duration: 2000
        })
      }).finally(() => {
        this.avatarUploading = false
        // 重置 input，允许重复选择同一文件
        event.target.value = ''
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.profile-container {
  padding: 24px;
  width: 100%;
  min-height: calc(100vh - 84px);
  margin: 0;
  position: relative;
  overflow: hidden;
}

.profile-content {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.profile-ambient {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 2;
}

.profile-ambient .ingot {
  position: absolute;
  border-radius: 0 0 10px 10px;
  background: linear-gradient(180deg, rgba(255, 225, 152, 0.96) 0%, rgba(227, 179, 84, 0.96) 58%, rgba(181, 129, 49, 0.96) 100%);
  box-shadow:
    0 0 16px rgba(221, 176, 87, 0.62),
    inset 0 1px 0 rgba(255, 243, 205, 0.68);
  opacity: 0;
  transform: translateY(4px) scale(0.9);
  animation: ingotBlink 6.4s ease-in-out infinite, ingotDrift 5.8s ease-in-out infinite;
  mix-blend-mode: screen;
}

.profile-ambient .ingot::before,
.profile-ambient .ingot::after {
  content: '';
  position: absolute;
  top: -3px;
  width: 7px;
  height: 8px;
  border-radius: 8px 8px 4px 4px;
  background: linear-gradient(180deg, rgba(255, 235, 176, 0.95) 0%, rgba(219, 168, 74, 0.95) 100%);
}

.profile-ambient .ingot::before {
  left: -3px;
  transform: rotate(-18deg);
}

.profile-ambient .ingot::after {
  right: -3px;
  transform: rotate(18deg);
}

.profile-ambient .spark {
  position: absolute;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 239, 188, 0.95) 0%, rgba(230, 186, 94, 0.8) 60%, rgba(0, 0, 0, 0) 100%);
  box-shadow: 0 0 10px rgba(237, 196, 110, 0.5);
  opacity: 0;
  animation: sparkBlink 3.8s ease-in-out infinite;
}

.profile-banner {
  margin-bottom: 18px;
  padding: 18px 22px;
  border-radius: 16px;
  border: 1px solid rgba(210, 169, 80, 0.34);
  background:
    radial-gradient(520px 180px at 8% -10%, rgba(210, 169, 80, 0.2), transparent 60%),
    radial-gradient(420px 160px at 92% -20%, rgba(166, 122, 53, 0.18), transparent 58%),
    repeating-linear-gradient(127deg, rgba(210, 169, 80, 0.06) 0 1px, rgba(0, 0, 0, 0) 1px 8px),
    linear-gradient(140deg, rgba(30, 23, 16, 0.96) 0%, rgba(22, 17, 12, 0.98) 100%);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(236, 210, 160, 0.12);
}

.banner-title {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 0.4px;
  color: #f2dfbb;
}

.banner-sub {
  margin-top: 6px;
  font-size: 13px;
  color: #cdb58a;
}

.profile-grid {
  position: relative;
}

.top-card-col {
  display: flex;
}

.user-card {
  border-radius: 16px;
  border: 1px solid rgba(210, 169, 80, 0.28);
  overflow: hidden;
  background:
    repeating-linear-gradient(127deg, rgba(210, 169, 80, 0.045) 0 1px, rgba(0, 0, 0, 0) 1px 8px),
    linear-gradient(145deg, rgba(28, 21, 15, 0.96) 0%, rgba(22, 17, 12, 0.98) 100%);
  box-shadow:
    0 10px 24px rgba(0, 0, 0, 0.32),
    0 0 0 1px rgba(210, 169, 80, 0.12),
    0 0 24px rgba(184, 138, 58, 0.18);
  flex: 1;
}

.profile-hero {
  display: flex;
  gap: 18px;
  align-items: center;
  padding: 20px 20px 16px 20px;
  background: transparent;
  border-bottom: 1px solid rgba(210, 169, 80, 0.2);
}

.avatar-section {
  position: relative;
}
.avatar-click {
  position: relative;
  display: inline-block;
  cursor: pointer;
  border-radius: 50%;
}
.avatar-click::before {
  content: '';
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(214, 178, 99, 0.28) 0%, rgba(214, 178, 99, 0.08) 45%, transparent 70%);
  animation: avatarPulse 2.8s ease-in-out infinite;
  pointer-events: none;
}
.avatar-mask {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.45);
  color: #fff;
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.2s ease;
  font-size: 12px;
  gap: 4px;
}
.avatar-click:hover .avatar-mask {
  opacity: 1;
}
.avatar-click.uploading .avatar-mask {
  opacity: 1;
}
.avatar-click.uploading {
  cursor: progress;
}
.avatar-input {
  display: none;
}
.info-section {
  display: flex;
  flex-direction: column;
  gap: 10px;

  h3 {
    margin: 0;
    font-size: 20px;
    color: #f0ddb6;
  }
}
.role-group {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.identity-pills {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.identity-pill {
  display: inline-flex;
  align-items: center;
  height: 24px;
  padding: 0 10px;
  border-radius: 999px;
  border: 1px solid rgba(210, 169, 80, 0.32);
  background: rgba(216, 177, 91, 0.12);
  color: #ecd8ad;
  font-size: 12px;
}

.meta-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #bfa57a;
  font-size: 13px;
}

.meta-item {
  display: flex;
  gap: 10px;
}

.meta-label {
  min-width: 44px;
  color: #bfa57a;
}

.meta-value {
  color: #ead8b2;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  padding: 16px 20px 20px 20px;
  background: rgba(24, 19, 13, 0.6);
  border-top: 1px solid rgba(210, 169, 80, 0.18);
}
.stat-item {
  padding: 12px 14px;
  border-radius: 12px;
  background: rgba(39, 30, 21, 0.78);
  border: 1px solid rgba(210, 169, 80, 0.2);
  h4 {
    margin: 0;
    font-size: 15px;
    color: #f0ddb6;
  }
  span {
    font-size: 12px;
    color: #bfa57a;
  }
}

.section-card {
  border-radius: 16px;
  border: 1px solid rgba(210, 169, 80, 0.26);
  background:
    repeating-linear-gradient(127deg, rgba(210, 169, 80, 0.045) 0 1px, rgba(0, 0, 0, 0) 1px 8px),
    linear-gradient(145deg, rgba(28, 21, 15, 0.96) 0%, rgba(22, 17, 12, 0.98) 100%);
  box-shadow:
    0 10px 24px rgba(0, 0, 0, 0.28),
    0 0 0 1px rgba(210, 169, 80, 0.1),
    0 0 22px rgba(184, 138, 58, 0.16);
  flex: 1;
}

.card-header {
  font-size: 16px;
  font-weight: 600;
  color: #f2dfbb;
}

.password-col {
  margin-top: 20px;
}

::v-deep .el-form-item__label {
  color: #c6ac80;
}

::v-deep .el-card__header {
  border-bottom: 1px solid rgba(210, 169, 80, 0.2);
}

::v-deep .el-input__inner,
::v-deep .el-textarea__inner {
  background: #221a12;
  border-color: rgba(210, 169, 80, 0.34);
  color: #efddb6;
}

::v-deep .el-input__inner::placeholder {
  color: rgba(226, 201, 151, 0.58);
}

::v-deep .el-input__inner:focus,
::v-deep .el-textarea__inner:focus {
  border-color: #dcb467;
  box-shadow: 0 0 0 2px rgba(220, 180, 103, 0.2);
}

::v-deep .el-radio__label {
  color: #e1cca2;
}

::v-deep .el-button--primary {
  background: linear-gradient(90deg, #8f6b31 0%, #d6ae63 100%);
  border-color: #d2a95f;
  color: #1a1309;
  box-shadow: 0 8px 18px rgba(180, 136, 56, 0.36);
}

::v-deep .el-button--primary:hover,
::v-deep .el-button--primary:focus {
  transform: translateY(-1px);
  background: linear-gradient(90deg, #a47b3b 0%, #e5c177 100%);
  border-color: #e1bc72;
  color: #120c06;
  box-shadow: 0 12px 24px rgba(198, 151, 69, 0.42), 0 0 0 1px rgba(232, 194, 114, 0.24);
}

::v-deep .el-button--primary:active {
  transform: translateY(0);
}

@media (max-width: 768px) {
  .profile-hero {
    flex-direction: column;
    align-items: flex-start;
  }

  .stats-row {
    grid-template-columns: 1fr;
  }

  .top-card-col {
    display: block;
  }

  .banner-title {
    font-size: 21px;
  }
}

@keyframes avatarPulse {
  0% {
    opacity: 0.55;
    transform: scale(0.98);
  }
  50% {
    opacity: 0.95;
    transform: scale(1.03);
  }
  100% {
    opacity: 0.55;
    transform: scale(0.98);
  }
}

@keyframes ingotBlink {
  0% {
    opacity: 0;
    transform: translateY(4px) scale(0.88);
  }
  22% {
    opacity: 0.52;
    transform: translateY(0) scale(1);
  }
  38% {
    opacity: 0.35;
  }
  55% {
    opacity: 0.68;
    transform: translateY(-2px) scale(1.03) rotate(4deg);
  }
  100% {
    opacity: 0;
    transform: translateY(-6px) scale(0.9) rotate(-5deg);
  }
}

@keyframes ingotDrift {
  0% {
    margin-left: 0;
  }
  50% {
    margin-left: 4px;
  }
  100% {
    margin-left: 0;
  }
}

@keyframes sparkBlink {
  0% {
    opacity: 0;
    transform: scale(0.7);
  }
  30% {
    opacity: 0.85;
    transform: scale(1.2);
  }
  55% {
    opacity: 0.45;
    transform: scale(0.95);
  }
  100% {
    opacity: 0;
    transform: scale(0.7);
  }
}

</style>
