<template>
  <div class="profile-container">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :lg="8">
        <el-card class="user-card">
          <div class="user-info">
            <div class="avatar-section">
              <div class="avatar-click" @click="handleAvatarClick">
                <el-avatar :size="100" :src="userInfo.avatar || ''" icon="el-icon-user-solid" />
                <div class="avatar-mask">
                  <i class="el-icon-camera" />
                  <span>更换头像</span>
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
              <p class="user-role" v-for="(role, index) in userInfo.roles" :key="index">
                <el-tag size="small">{{ role.name }}</el-tag>
              </p>
            </div>
          </div>
          <div class="stats-row">
            <div class="stat-item">
              <h4>{{ userInfo.email || '-' }}</h4>
              <span>邮箱</span>
            </div>
            <div class="stat-item" v-if="userInfo.phone">
              <h4>{{ userInfo.phone }}</h4>
              <span>手机号</span>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :lg="16">
        <el-card class="form-card">
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

      <el-col :xs="24" :sm="24" :lg="24" style="margin-top: 20px;">
        <el-card class="password-card">
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
</template>

<script>
import { updateProfile, changePassword } from '@/api/auth'
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
      this.$message({
        message: '已选择头像文件（上传接口未接入）',
        type: 'info',
        duration: 2000
      })
      // 重置 input，允许重复选择同一文件
      event.target.value = ''
    }
  }
}
</script>

<style lang="scss" scoped>
.profile-container {
  padding: 20px;
}
.page-header {
  margin-bottom: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  color: #fff;
}
h2 {
  margin: 0;
  font-size: 24px;
}
p {
  margin: 0;
  opacity: 0.9;
}
.user-card {
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
.user-info {
  text-align: center;
  padding: 20px 0;
}
.avatar-section {
  position: relative;
  margin-bottom: 20px;
}
.avatar-click {
  position: relative;
  display: inline-block;
  cursor: pointer;
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
.avatar-input {
  display: none;
}
.info-section {
  h3 {
    margin: 10px 0;
    font-size: 20px;
    color: #333;
  }
  .user-role {
    margin: 5px;
    display: inline-block;
  }
}
.stats-row {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}
.stat-item {
  text-align: center;
  h4 {
    margin: 0;
    font-size: 16px;
    color: #333;
  }
  span {
    font-size: 12px;
    color: #999;
  }
}
.form-card, .password-card {
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
.card-header {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}
</style>
