<template>
  <div class="menu-container system-menus-page">
    <div class="page-header">
      <div class="header-left">
        <h2>菜单管理</h2>
        <p>只读模式：菜单/权限由配置文件维护</p>
      </div>
      <div class="header-actions">
        <el-button icon="el-icon-refresh" @click="fetchMenuList" size="mini">刷新</el-button>
      </div>
    </div>

    <div class="panel-grid">
      <el-card class="tree-card">
        <div class="card-title" slot="header">
          <span>菜单树</span>
          <span class="card-sub">{{ menuList.length }} 个</span>
        </div>
        <el-tree
          ref="menuTree"
          :data="menuTree"
          node-key="id"
          :props="{children: 'children', label: 'name'}"
          :expand-on-click-node="false"
          highlight-current
          @node-click="handleNodeClick"
        >
          <span class="custom-tree-node" slot-scope="{ data }">
            <i v-if="data.icon" :class="data.icon"></i>
            <span class="node-title">{{ data.name || data.title }}</span>
            <el-tag v-if="data.type" size="mini" class="node-tag">{{ data.type }}</el-tag>
          </span>
        </el-tree>
      </el-card>

      <el-card class="detail-card">
        <div slot="header" class="card-title">
          <span>菜单详情</span>
        </div>
        <div v-if="!selectedMenu || !selectedMenu.id" class="empty-state">
          <div class="empty-icon">⌘</div>
          <div class="empty-title">请选择左侧菜单</div>
          <div class="empty-desc">点击树节点查看详细配置</div>
        </div>
        <div v-else class="detail-grid">
          <div class="detail-hero">
            <div class="hero-icon">
              <i v-if="selectedMenu.icon" :class="selectedMenu.icon"></i>
              <span v-else>◎</span>
            </div>
            <div class="hero-info">
              <div class="hero-title">{{ selectedMenu.name || selectedMenu.title || '-' }}</div>
              <div class="hero-sub">{{ selectedMenu.code || '-' }}</div>
              <div class="hero-tags">
                <el-tag size="mini" type="info">{{ selectedMenu.type || '-' }}</el-tag>
                <el-tag size="mini" :type="selectedMenu.is_visible ? 'success' : 'danger'">
                  {{ selectedMenu.is_visible ? '显示' : '隐藏' }}
                </el-tag>
              </div>
            </div>
            <div class="hero-order">
              <div class="hero-order-label">排序</div>
              <div class="hero-order-value">{{ selectedMenu.sort_order ?? '-' }}</div>
            </div>
          </div>

          <div class="detail-section">
            <div class="section-title">路由信息</div>
            <div class="key-grid">
              <div class="key-item">
                <div class="key-label">路径</div>
                <div class="key-value">{{ selectedMenu.path || '-' }}</div>
              </div>
              <div class="key-item">
                <div class="key-label">组件</div>
                <div class="key-value">{{ selectedMenu.component || '-' }}</div>
              </div>
              <div class="key-item">
                <div class="key-label">重定向</div>
                <div class="key-value">{{ selectedMenu.redirect || '-' }}</div>
              </div>
              <div class="key-item">
                <div class="key-label">父级</div>
                <div class="key-value">{{ selectedMenu.parent_id || '-' }}</div>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <div class="section-title">状态概览</div>
            <div class="stat-grid">
              <div class="stat-card">
                <div class="stat-label">菜单类型</div>
                <div class="stat-value">{{ selectedMenu.type || '-' }}</div>
              </div>
              <div class="stat-card">
                <div class="stat-label">是否显示</div>
                <div class="stat-value">{{ selectedMenu.is_visible ? '显示' : '隐藏' }}</div>
              </div>
              <div class="stat-card">
                <div class="stat-label">排序号</div>
                <div class="stat-value">{{ selectedMenu.sort_order ?? '-' }}</div>
              </div>
              <div class="stat-card">
                <div class="stat-label">图标</div>
                <div class="stat-value">{{ selectedMenu.icon || '-' }}</div>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { getMenus } from '@/api/menu'

export default {
  name: 'MenuManagement',
  data() {
    return {
      menuList: [],
      menuTree: [],
      selectedMenu: {}
    }
  },
  created() {
    this.fetchMenuList()
  },
  methods: {
    async fetchMenuList() {
      try {
        const { data } = await getMenus()
        this.menuList = data
        this.buildMenuTree()
      } catch (error) {
        this.$message.error('获取菜单列表失败')
      }
    },
    buildMenuTree() {
      const map = {}
      const tree = []

      this.menuList.forEach(menu => {
        map[menu.id] = menu
        menu.children = []
      })

      this.menuList.forEach(menu => {
        if (menu.parent_id && map[menu.parent_id]) {
          map[menu.parent_id].children.push(menu)
        } else {
          tree.push(menu)
        }
      })

      this.menuTree = tree
    },
    handleNodeClick(data) {
      this.selectedMenu = { ...data }
    }
  }
}
</script>

<style lang="scss" scoped>
.menu-container {
  padding: 20px 24px;
  background:
    radial-gradient(1200px 400px at 10% -10%, rgba(125, 143, 255, 0.18), transparent 50%),
    radial-gradient(900px 300px at 90% -10%, rgba(0, 201, 255, 0.18), transparent 50%);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 18px 20px;
  background: linear-gradient(135deg, #1f2a44 0%, #2d3a66 100%);
  border-radius: 14px;
  color: #fff;
  box-shadow: 0 12px 30px rgba(31, 42, 68, 0.2);

  h2 {
    margin: 0;
    font-size: 22px;
    letter-spacing: 0.5px;
  }

  p {
    margin: 6px 0 0 0;
    opacity: 0.8;
    font-size: 13px;
  }
}

.header-left {
  display: flex;
  flex-direction: column;
}

.header-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.panel-grid {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 18px;
}

.tree-card {
  height: calc(100vh - 220px);
  overflow-y: auto;
  border-radius: 14px;
}

.detail-card {
  height: calc(100vh - 220px);
  border-radius: 14px;
}

.card-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 16px;
  font-weight: 600;
}

.card-sub {
  font-size: 12px;
  color: var(--menu-card-sub);
}

.custom-tree-node {
  flex: 1;
  align-items: center;
  padding: 8px 0;
  display: flex;
  gap: 8px;

  i {
    font-size: 16px;
    color: var(--menu-tree-icon);
  }

  .node-title {
    font-size: 14px;
    color: var(--menu-node-title);
  }
}

.node-tag {
  margin-left: auto;
  background: var(--menu-node-tag-bg);
  color: var(--menu-node-tag-text);
  border: 1px solid var(--menu-node-tag-border);
}

.empty-state {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--menu-empty-text);
  text-align: center;
  gap: 6px;
}

.empty-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: var(--menu-empty-icon-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--menu-empty-icon-text);
  font-weight: 700;
}

.empty-title {
  font-size: 14px;
  color: var(--menu-empty-title);
}

.empty-desc {
  font-size: 12px;
  opacity: 0.7;
}

.detail-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-hero {
  display: grid;
  grid-template-columns: 56px 1fr 120px;
  gap: 14px;
  padding: 16px;
  border-radius: 12px;
  background: var(--menu-hero-bg);
  border: 1px solid var(--menu-hero-border);
  align-items: center;
}

.hero-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--menu-hero-icon-bg);
  color: var(--menu-hero-icon-text);
  font-size: 22px;
}

.hero-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.hero-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--menu-hero-title);
}

.hero-sub {
  font-size: 12px;
  color: var(--menu-hero-sub);
}

.hero-tags {
  display: flex;
  gap: 6px;
}

.hero-order {
  text-align: right;
}

.hero-order-label {
  font-size: 12px;
  color: var(--menu-hero-order-label);
}

.hero-order-value {
  font-size: 22px;
  font-weight: 700;
  color: var(--menu-hero-order-value);
}

.detail-section {
  padding: 14px 16px;
  border-radius: 12px;
  background: var(--menu-section-bg);
  border: 1px solid var(--menu-section-border);
}

.section-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--menu-section-title);
  margin-bottom: 10px;
}

.key-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.key-item {
  padding: 10px 12px;
  border-radius: 10px;
  background: var(--menu-key-bg);
  border: 1px solid var(--menu-key-border);
}

.key-label {
  font-size: 12px;
  color: var(--menu-key-label);
  margin-bottom: 6px;
}

.key-value {
  font-size: 13px;
  color: var(--menu-key-value);
  word-break: break-all;
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.stat-card {
  padding: 12px;
  border-radius: 10px;
  background: var(--menu-stat-bg);
  border: 1px solid var(--menu-stat-border);
}

.stat-label {
  font-size: 12px;
  color: var(--menu-stat-label);
  margin-bottom: 6px;
}

.stat-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--menu-stat-value);
}

@media (max-width: 1200px) {
  .panel-grid {
    grid-template-columns: 1fr;
  }
}

::v-deep .el-tree-node__content {
  color: var(--menu-tree-text);
}

::v-deep .el-tree-node__content:hover {
  background-color: var(--menu-tree-hover);
}

::v-deep .el-tree--highlight-current .el-tree-node.is-current > .el-tree-node__content {
  background-color: var(--menu-tree-current);
}
</style>
