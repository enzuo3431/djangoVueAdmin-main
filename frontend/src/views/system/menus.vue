<template>
  <div class="menu-container">
    <div class="page-header">
      <h2>菜单管理</h2>
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">添加菜单</el-button>
    </div>

    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="tree-card">
          <div slot="header" class="card-header">
            <span>菜单树</span>
            <el-button icon="el-icon-refresh" @click="fetchMenuList" size="small">刷新</el-button>
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
              <span>{{ data.name || data.title }}</span>
            </span>
          </el-tree>
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-card class="form-card">
          <div slot="header">
            <span>{{ dialogTitle }}</span>
          </div>
          <el-form ref="menuFormRef" :model="menuForm" :rules="menuRules" label-width="100px">
            <el-form-item label="菜单名称" prop="name">
              <el-input v-model="menuForm.name" placeholder="请输入菜单名称" />
            </el-form-item>
            <el-form-item label="权限代码" prop="code">
              <el-input v-model="menuForm.code" placeholder="请输入权限代码，如：system:user" />
            </el-form-item>
            <el-form-item label="菜单类型" prop="type">
              <el-radio-group v-model="menuForm.type">
                <el-radio label="menu">菜单</el-radio>
                <el-radio label="button">按钮</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="路由路径" prop="path">
              <el-input v-model="menuForm.path" placeholder="请输入路由路径，如：/system/users" />
            </el-form-item>
            <el-form-item label="组件路径" prop="component">
              <el-input v-model="menuForm.component" placeholder="请输入组件路径，如：system/users/index" />
            </el-form-item>
            <el-form-item label="菜单图标" prop="icon">
              <el-input v-model="menuForm.icon" placeholder="请输入图标类名，如：el-icon-user" />
            </el-form-item>
            <el-form-item label="排序顺序" prop="sort_order">
              <el-input-number v-model="menuForm.sort_order" :min="0" placeholder="请输入排序顺序，数字越小越靠前" />
            </el-form-item>
            <el-form-item label="是否显示" prop="is_visible">
              <el-switch v-model="menuForm.is_visible" active-text="显示" inactive-text="隐藏" />
            </el-form-item>
            <el-form-item label="重定向" prop="redirect">
              <el-input v-model="menuForm.redirect" placeholder="请输入重定向路径，留空则不重定向" />
            </el-form-item>
            <el-form-item label="父级菜单" prop="parent_id" v-if="isEdit">
              <el-select v-model="menuForm.parent_id" placeholder="请选择父级菜单（留空为顶级菜单）" clearable>
                <el-option
                  v-for="item in parentMenuOptions"
                  :key="item.id"
                  :label="item.name || item.title"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="loading" @click="handleSubmit">{{ isEdit ? '更新' : '创建' }}</el-button>
              <el-button @click="handleCancel">取消</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getMenus, createMenu, updateMenu, deleteMenu } from '@/api/menu'

export default {
  name: 'MenuManagement',
  data() {
    return {
      menuList: [],
      menuTree: [],
      dialogVisible: false,
      dialogTitle: '',
      isEdit: false,
      loading: false,
      parentMenuOptions: [],
      menuForm: {
        id: null,
        name: '',
        code: '',
        type: 'menu',
        path: '',
        component: '',
        icon: '',
        sort_order: 0,
        is_visible: true,
        redirect: '',
        parent_id: null
      },
      menuRules: {
        name: [{ required: true, message: '请输入菜单名称', trigger: 'blur' }],
        code: [{ required: true, message: '请输入权限代码', trigger: 'blur' }]
      }
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
    handleNodeClick(data, node) {
      this.isEdit = true
      this.dialogTitle = '编辑菜单'
      this.dialogVisible = true
      this.menuForm = {
        id: data.id,
        name: data.name || data.title,
        code: data.code,
        type: data.type,
        path: data.path,
        component: data.component,
        icon: data.icon,
        sort_order: data.sort_order || 0,
        is_visible: data.is_visible,
        redirect: data.redirect,
        parent_id: data.parent_id
      }
      this.buildParentOptions(data.id)
    },
    handleAdd() {
      this.isEdit = false
      this.dialogTitle = '添加菜单'
      this.dialogVisible = true
      this.resetForm()
    },
    handleEdit(data) {
      this.isEdit = true
      this.dialogTitle = '编辑菜单'
      this.dialogVisible = true
      this.menuForm = {
        id: data.id,
        name: data.name || data.title,
        code: data.code,
        type: data.type,
        path: data.path,
        component: data.component,
        icon: data.icon,
        sort_order: data.sort_order || 0,
        is_visible: data.is_visible,
        redirect: data.redirect,
        parent_id: data.parent_id
      }
      this.buildParentOptions(data.id)
    },
    buildParentOptions(excludeId = null) {
      this.parentMenuOptions = this.menuList
        .filter(m => m.id !== excludeId)
        .map(m => ({ id: m.id, name: m.name || m.title }))
    },
    handleDelete(row) {
      this.$confirm(`确定要删除菜单"${row.name || row.title}"吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await deleteMenu(row.id)
          this.$message.success('删除成功')
          this.fetchMenuList()
        } catch (error) {
          this.$message.error('删除失败')
        }
      }).catch(() => {})
    },
    handleCancel() {
      this.dialogVisible = false
      this.resetForm()
    },
    async handleSubmit() {
      this.$refs.menuFormRef.validate(async valid => {
        if (valid) {
          this.loading = true
          try {
            const data = { ...this.menuForm }
            if (this.isEdit) {
              await updateMenu(data.id, data)
              this.$message.success('更新成功')
            } else {
              await createMenu(data)
              this.$message.success('创建成功')
            }
            this.dialogVisible = false
            this.resetForm()
            this.fetchMenuList()
          } catch (error) {
            this.$message.error(error.message || '操作失败')
          } finally {
            this.loading = false
          }
        }
      })
    },
    resetForm() {
      this.menuForm = {
        id: null,
        name: '',
        code: '',
        type: 'menu',
        path: '',
        component: '',
        icon: '',
        sort_order: 0,
        is_visible: true,
        redirect: '',
        parent_id: null
      }
      if (this.$refs.menuFormRef) {
        this.$refs.menuFormRef.clearValidate()
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.menu-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  color: #fff;

  h2 {
    margin: 0;
    font-size: 24px;
  }
}

.tree-card {
  height: calc(100vh - 200px);
  overflow-y: auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
}

.custom-tree-node {
  flex: 1;
  align-items: center;
  padding: 8px 0;

  i {
    margin-right: 8px;
    font-size: 16px;
  }

  span {
    font-size: 14px;
  }
}

.form-card {
  height: calc(100vh - 200px);
}
</style>
