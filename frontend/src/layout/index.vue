<template>
  <div class="app-wrapper" :class="classObj">
    <black-gold-ambient />
    <sidebar class="sidebar-container" />
    <div class="main-container">
      <div class="fixed-header">
        <navbar />
        <tags-view />
      </div>
      <app-main />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { Navbar, Sidebar, AppMain } from './components'
import TagsView from '@/components/TagsView'
import BlackGoldAmbient from '@/components/BlackGoldAmbient'

export default {
  name: 'Layout',
  components: {
    Navbar,
    Sidebar,
    AppMain,
    TagsView,
    BlackGoldAmbient
  },
  computed: {
    ...mapGetters([
      'sidebar'
    ]),
    classObj() {
      return {
        hideSidebar: !this.sidebar.opened,
        openSidebar: this.sidebar.opened
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.app-wrapper {
  position: relative;
  height: 100%;
  width: 100%;

  &.openSidebar {
    .main-container {
      margin-left: 210px;
    }

    .sidebar-container {
      width: 210px !important;
    }

    .fixed-header {
      width: calc(100% - 210px);
    }
  }

  &.hideSidebar {
    .main-container {
      margin-left: 54px;
    }

    .sidebar-container {
      width: 54px !important;
    }

    .fixed-header {
      width: calc(100% - 54px);
    }
  }
}

.main-container {
  min-height: 100%;
  transition: margin-left 0.28s ease-in-out;
  margin-left: 210px;
  position: relative;
}

.sidebar-container {
  transition: width 0.28s ease-in-out;
  width: 210px !important;
  background-color: #304156;
  height: 100%;
  position: fixed;
  font-size: 0px;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 1001;
  overflow: hidden;
}

.fixed-header {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 9;
  width: calc(100% - 210px);
  transition: width 0.28s ease-in-out;
}

/* Prevent flickering during transitions */
* {
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}
</style>
