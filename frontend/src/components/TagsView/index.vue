<template>
  <div class="tags-view-container">
    <el-tag
      v-for="tag in visitedViews"
      :key="tag.path"
      :closable="tag.path !== '/'"
      :type="isActive(tag) ? 'success' : 'info'"
      class="tag-item"
      @close="closeTag(tag)"
      @click="toTag(tag)"
    >
      {{ tag.title }}
    </el-tag>
    <div class="tag-actions">
      <el-dropdown trigger="click">
        <span class="el-dropdown-link">
          操作<i class="el-icon-arrow-down el-icon--right" />
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item @click.native="closeOthers">关闭其他</el-dropdown-item>
          <el-dropdown-item @click.native="closeAll">关闭全部</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'TagsView',
  computed: {
    ...mapGetters(['visitedViews'])
  },
  methods: {
    isActive(tag) {
      return tag.path === this.$route.path
    },
    toTag(tag) {
      if (tag.path !== this.$route.path) {
        this.$router.push(tag.path)
      }
    },
    closeTag(tag) {
      this.$store.dispatch('tagsView/delView', tag)
      if (this.$route.path === tag.path) {
        const latest = this.visitedViews.slice(-1)[0]
        this.$router.push(latest ? latest.path : '/')
      }
    },
    closeOthers() {
      const current = this.visitedViews.find(v => v.path === this.$route.path)
      if (current) {
        this.$store.dispatch('tagsView/delOthersViews', current)
      }
    },
    closeAll() {
      this.$store.dispatch('tagsView/delAllViews')
      this.$router.push('/')
    }
  }
}
</script>

<style lang="scss" scoped>
.tags-view-container {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  background: var(--header-bg);
  border-bottom: 1px solid #ebeef5;
  overflow-x: auto;
  white-space: nowrap;
}

.tag-item {
  margin-right: 8px;
  cursor: pointer;
  user-select: none;
}

.tag-actions {
  margin-left: auto;
  padding-left: 10px;
}
</style>
