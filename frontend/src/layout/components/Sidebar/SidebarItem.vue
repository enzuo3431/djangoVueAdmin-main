<template>
  <div v-if="!item.hidden">
    <!-- 如果有子菜单，显示为可折叠菜单 -->
    <el-submenu v-if="item.children && item.children.length > 0" ref="subMenu" :index="item.path || String(item.id)" popper-append-to-body>
      <template slot="title">
        <i v-if="getIcon(item)" :class="getIcon(item)" />
        <span>{{ getTitle(item) }}</span>
      </template>
      <template v-for="child in item.children">
        <template v-if="!child.hidden">
          <sidebar-item
            v-if="child.children && child.children.length > 0"
            :key="child.path || child.id"
            :is-nest="true"
            :item="child"
            :base-path="resolvePath(child.path)"
            class="nest-menu"
          />
          <app-link v-else :key="child.path || child.id" :to="resolvePath(child.path)">
            <el-menu-item :index="resolvePath(child.path)">
              <i v-if="getIcon(child)" :class="getIcon(child)" />
              <template #title><span>{{ getTitle(child) }}</span></template>
            </el-menu-item>
          </app-link>
        </template>
      </template>
    </el-submenu>

    <!-- 没有子菜单，直接显示菜单项 -->
    <app-link v-else :to="resolvePath(item.path)">
      <el-menu-item :index="resolvePath(item.path)" :class="{'submenu-title-noDropdown':isNest}">
        <i :class="getIcon(item)" />
        <template #title><span>{{ getTitle(item) }}</span></template>
      </el-menu-item>
    </app-link>
  </div>
</template>

<script>
import * as path from 'path-browserify'
import AppLink from './Link'

export default {
  name: 'SidebarItem',
  components: { AppLink },
  props: {
    item: {
      type: Object,
      required: true
    },
    isNest: {
      type: Boolean,
      default: false
    },
    basePath: {
      type: String,
      default: ''
    }
  },
  data() {
    this.onlyOneChild = null
    return {}
  },
  methods: {
    hasOneShowingChild(children = [], parent) {
      const showingChildren = children.filter(item => {
        if (item.hidden) {
          return false
        } else {
          this.onlyOneChild = item
          return true
        }
      })

      if (showingChildren.length === 1) {
        return true
      }

      if (showingChildren.length === 0) {
        this.onlyOneChild = { ...parent, path: '', noShowingChildren: true }
        return true
      }

      return false
    },
    getTitle(item) {
      // 支持菜单结构（title）和路由结构（meta.title）
      if (item.meta) {
        return item.meta.title
      }
      return item.title || item.path
    },
    getIcon(item, parent = null) {
      // 支持菜单结构（icon）和路由结构（meta.icon）
      if (item.meta && item.meta.icon) {
        return item.meta.icon
      }
      if (item.icon) {
        return item.icon
      }
      if (parent && parent.meta && parent.meta.icon) {
        return parent.meta.icon
      }
      if (parent && parent.icon) {
        return parent.icon
      }
      return ''
    },
    resolvePath(routePath) {
      if (this.isExternalLink(routePath)) {
        return routePath
      }
      if (this.isExternalLink(this.basePath)) {
        return this.basePath
      }
      // 如果是绝对路径，直接返回
      if (routePath.startsWith('/')) {
        return routePath
      }
      // 否则拼接路径
      if (this.basePath) {
        return path.resolve(this.basePath, routePath)
      }
      return routePath
    },
    isExternalLink(path) {
      return /^(https?:|mailto:|tel:)/.test(path)
    }
  }
}
</script>

<style lang="scss" scoped>
// 子菜单样式
.nest-menu {
  ::v-deep .el-submenu__title {
    i {
      color: #bfcbd9 !important;
    }
  }

  ::v-deep .el-menu-item {
    i {
      color: #bfcbd9 !important;
    }

    &.is-active {
      i {
        color: #409EFF !important;
      }
    }
  }
}

// 确保图标颜色正确
::v-deep .el-menu-item {
  i {
    color: #bfcbd9;
  }

  &.is-active {
    i {
      color: #409EFF;
    }
  }
}

::v-deep .el-submenu__title {
  i {
    color: #bfcbd9;
  }

  &:hover {
    i {
      color: #409EFF;
    }
  }
}
</style>
