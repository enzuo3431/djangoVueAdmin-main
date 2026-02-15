<template>
  <div class="app-container">
    <div class="page-header">
      <h2>登录日志</h2>
      <p>查看用户登录记录与登录状态</p>
    </div>

    <el-card class="box-card">
      <div class="filter-container">
        <el-input
          v-model="listQuery.keyword"
          placeholder="搜索用户名"
          style="width: 200px;"
          class="filter-item"
          clearable
          @keyup.enter.native="handleFilter"
        />
        <el-select v-model="listQuery.status" class="filter-item" clearable placeholder="状态">
          <el-option label="成功" value="success" />
          <el-option label="失败" value="failed" />
        </el-select>
        <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
          搜索
        </el-button>
      </div>

      <el-table
        v-loading="listLoading"
        :data="list"
        border
        fit
        highlight-current-row
        style="margin-top: 20px;"
      >
        <el-table-column label="用户名" min-width="160">
          <template slot-scope="scope">
            {{ scope.row.username || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'" size="small">
              {{ scope.row.status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="IP" width="160">
          <template slot-scope="scope">
            {{ scope.row.ip_address || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="备注" min-width="200">
          <template slot-scope="scope">
            {{ scope.row.message || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="时间" width="180">
          <template slot-scope="scope">
            {{ scope.row.login_time | datetime }}
          </template>
        </el-table-column>
      </el-table>

      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.page_size"
        @pagination="getList"
      />
    </el-card>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { getLoginLogs } from '@/api/log'

export default {
  name: 'LoginLogs',
  components: { Pagination },
  data() {
    return {
      list: [],
      total: 0,
      listLoading: false,
      listQuery: {
        page: 1,
        page_size: 10,
        keyword: '',
        status: ''
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      getLoginLogs(this.listQuery).then(res => {
        this.list = res.data.list
        this.total = res.data.total
        this.listLoading = false
      }).catch(() => {
        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    }
  }
}
</script>

<style lang="scss" scoped>
.page-header {
  margin-bottom: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%);
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
</style>
