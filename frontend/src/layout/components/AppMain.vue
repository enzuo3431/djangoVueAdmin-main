<template>
  <section class="app-main">
    <transition name="fade-transform" mode="out-in">
      <keep-alive :include="cachedViews">
        <router-view :key="key" />
      </keep-alive>
    </transition>
  </section>
</template>

<script>
export default {
  name: 'AppMain',
  computed: {
    cachedViews() {
      return []
    },
    key() {
      return this.$route.path
    }
  },
  watch: {
    $route: {
      immediate: true,
      handler(route) {
        this.$store.dispatch('tagsView/addView', route)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.app-main {
  min-height: calc(100vh - 90px);
  width: 100%;
  position: relative;
  overflow: hidden;
  padding: 20px;
  background-color: var(--app-bg);
  margin-top: 90px;
}

.fade-transform-leave-active,
.fade-transform-enter-active {
  transition: all .5s;
}

.fade-transform-enter {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
