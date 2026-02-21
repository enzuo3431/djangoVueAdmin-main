<template>
  <div class="navbar">
    <!-- 汉堡菜单按钮 -->
    <hamburger id="hamburger-container" :is-active="sidebar.opened" class="hamburger-container" @toggleClick="toggleSideBar" />

    <!-- 面包屑导航 -->
    <breadcrumb id="breadcrumb-container" class="breadcrumb-container" />

    <!-- 个人头像放在最右侧 -->
    <div class="right-menu">
      <div class="theme-switch">
        <el-select v-model="theme" size="mini" @change="handleThemeChange" placeholder="主题">
          <el-option label="默认" value="default" />
          <el-option label="海洋护眼" value="ocean" />
          <el-option label="丛林护眼" value="jungle-eye" />
        </el-select>
        <el-switch
          v-model="darkMode"
          active-text="黑金"
          inactive-text="明亮"
          @change="toggleDark"
        />
      </div>
      <el-dropdown trigger="click" class="avatar-container" @command="handleCommand">
        <div class="avatar-wrapper">
          <el-avatar :size="36" :src="avatar || ''" icon="el-icon-user-solid" />
          <span class="user-name">{{ name || '管理员' }}</span>
          <i class="el-icon-caret-bottom" />
        </div>
        <el-dropdown-menu slot="dropdown" class="user-dropdown">
          <router-link to="/profile">
            <el-dropdown-item>个人中心</el-dropdown-item>
          </router-link>
          <el-dropdown-item divided command="logout" class="logout-item">
            退出登录
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Hamburger from '@/components/Hamburger'
import Breadcrumb from '@/components/Breadcrumb'

export default {
  components: {
    Hamburger,
    Breadcrumb
  },
  computed: {
    ...mapGetters([
      'sidebar',
      'name',
      'avatar'
    ])
  },
  data() {
    return {
      theme: this.$store.state.app.theme,
      darkMode: this.$store.state.app.darkMode
    }
  },
  watch: {
    '$store.state.app.theme'(val) {
      this.theme = val
    },
    '$store.state.app.darkMode'(val) {
      this.darkMode = val
    }
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch('app/toggleSideBar')
    },
    handleThemeChange(val) {
      this.$store.dispatch('app/setTheme', val)
    },
    toggleDark() {
      this.$store.dispatch('app/toggleDarkMode')
    },
    async handleCommand(command) {
      if (command === 'logout') {
        try {
          await this.$store.dispatch('user/logout')
          this.$message({
            message: '退出成功',
            type: 'success',
            duration: 2000
          })
          // 使用 replace 避免重定向错误
          this.$router.replace(`/login`)
        } catch (error) {
          console.error('Logout error:', error)
          // 即使退出失败，也跳转到登录页
          this.$router.replace(`/login`)
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: var(--header-bg);
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
  display: flex;
  align-items: center;
  padding: 0 20px;

  .hamburger-container {
    line-height: 46px;
    height: 100%;
    cursor: pointer;
    transition: background .3s;
    -webkit-tap-highlight-color:transparent;
    padding: 0 10px;

    &:hover {
      background: rgba(0, 0, 0, .025);
    }
  }

  .breadcrumb-container {
    flex: 1;
    margin-left: 15px;
  }

  .right-menu {
    display: flex;
    align-items: center;
    gap: 12px;

    .theme-switch {
      display: flex;
      align-items: center;
      gap: 10px;
      .el-select {
        width: 100px;
      }
    }

    .avatar-container {
      .avatar-wrapper {
        display: flex;
        align-items: center;
        cursor: pointer;
        padding: 5px 10px;
        border-radius: 4px;
        transition: background .3s;

        &:hover {
          background: rgba(0, 0, 0, .025);
        }

        .user-name {
          margin-left: 10px;
          font-size: 14px;
          color: var(--app-text);
          max-width: 100px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        .el-icon-caret-bottom {
          margin-left: 5px;
          font-size: 12px;
          color: #909399;
        }
      }
    }
  }
}
</style>
