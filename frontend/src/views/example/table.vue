<template>
  <div class="app-container">
    <div class="page-header">
      <h2>表格示例</h2>
      <p>展示 Element UI 表格组件的使用</p>
    </div>

    <el-card class="box-card">
      <div class="filter-container">
        <el-input
          v-model="listQuery.title"
          placeholder="标题"
          style="width: 200px;"
          class="filter-item"
          @keyup.enter.native="handleFilter"
        />
        <el-select v-model="listQuery.importance" placeholder="重要性" clearable style="width: 120px" class="filter-item">
          <el-option v-for="item in importanceOptions" :key="item" :label="item" :value="item" />
        </el-select>
        <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
          搜索
        </el-button>
        <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
          添加
        </el-button>
      </div>

      <el-table
        v-loading="listLoading"
        :data="list"
        border
        fit
        highlight-current-row
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column label="ID" align="center" width="80">
          <template slot-scope="{row}">
            {{ row.id }}
          </template>
        </el-table-column>
        <el-table-column label="日期" width="150px" align="center">
          <template slot-scope="{row}">
            <span>{{ row.timestamp | datetime }}</span>
          </template>
        </el-table-column>
        <el-table-column label="标题" min-width="150px">
          <template slot-scope="{row}">
            <span class="link-type" @click="handleUpdate(row)">{{ row.title }}</span>
          </template>
        </el-table-column>
        <el-table-column label="作者" width="110px" align="center">
          <template slot-scope="{row}">
            <span>{{ row.author }}</span>
          </template>
        </el-table-column>
        <el-table-column label="重要性" width="80px" align="center">
          <template slot-scope="{row}">
            <el-rate v-model="row.importance" disabled show-score text-color="#ff9900" score-template="{value}" />
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="{row}">
            <el-tag :type="statusMap[row.status]">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="200">
          <template slot-scope="{row}">
            <el-button type="primary" size="mini" @click="handleUpdate(row)">
              编辑
            </el-button>
            <el-button type="danger" size="mini" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />
    </el-card>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'

const importanceOptions = [1, 2, 3]

export default {
  name: 'ComplexTable',
  components: { Pagination },
  data() {
    return {
      list: [],
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 10,
        importance: undefined,
        title: undefined
      },
      importanceOptions,
      statusMap: {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      // 模拟数据
      setTimeout(() => {
        this.list = [
          { id: 1, timestamp: '2024-01-15 10:30', title: '测试文章1', author: '张三', importance: 3, status: 'published' },
          { id: 2, timestamp: '2024-01-16 14:20', title: '测试文章2', author: '李四', importance: 2, status: 'draft' },
          { id: 3, timestamp: '2024-01-17 09:15', title: '测试文章3', author: '王五', importance: 1, status: 'published' },
          { id: 4, timestamp: '2024-01-18 16:45', title: '测试文章4', author: '赵六', importance: 2, status: 'deleted' },
          { id: 5, timestamp: '2024-01-19 11:00', title: '测试文章5', author: '孙七', importance: 3, status: 'published' }
        ]
        this.total = this.list.length
        this.listLoading = false
      }, 500)
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleCreate() {
      this.$message('添加功能开发中...')
    },
    handleUpdate(row) {
      this.$message('编辑: ' + row.title)
    },
    handleDelete(row) {
      this.$confirm('确定要删除这篇文章吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.page-header {
  margin-bottom: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  color: #fff;

  h2 {
    margin: 0 0 10px 0;
    font-size: 24px;
  }

  p {
    margin: 0;
    opacity: 0.9;
  }
}

.filter-container {
  padding-bottom: 10px;

  .filter-item {
    display: inline-block;
    vertical-align: middle;
    margin-bottom: 10px;
    margin-right: 10px;
  }
}

.link-type {
  color: #409EFF;
  cursor: pointer;

  &:hover {
    text-decoration: underline;
  }
}
</style>
