<template>
  <div class="app-container">
    <div class="page-header">
      <div class="header-left">
        <h2>操作日志</h2>
        <p>查看用户操作记录与接口调用信息</p>
      </div>
      <div class="header-actions">
        <el-button icon="el-icon-refresh" @click="getList" size="mini">刷新</el-button>
      </div>
    </div>

    <el-card class="box-card">
      <div class="filter-container">
        <el-input
          v-model="listQuery.keyword"
          placeholder="搜索路径"
          style="width: 220px;"
          class="filter-item"
          clearable
          @keyup.enter.native="handleFilter"
        />
        <el-select v-model="listQuery.method" class="filter-item" clearable placeholder="方法">
          <el-option label="GET" value="GET" />
          <el-option label="POST" value="POST" />
          <el-option label="PUT" value="PUT" />
          <el-option label="PATCH" value="PATCH" />
          <el-option label="DELETE" value="DELETE" />
        </el-select>
        <el-input
          v-model="listQuery.status_code"
          placeholder="状态码"
          style="width: 120px;"
          class="filter-item"
          clearable
          @keyup.enter.native="handleFilter"
        />
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
        <el-table-column label="用户" width="140">
          <template slot-scope="scope">
            {{ scope.row.username || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="方法" width="90" align="center">
          <template slot-scope="scope">
            <el-tag size="small">{{ scope.row.method }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="路径" min-width="280">
          <template slot-scope="scope">
            {{ scope.row.path }}
          </template>
        </el-table-column>
        <el-table-column label="状态码" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status_code >= 400 ? 'danger' : 'success'" size="small">
              {{ scope.row.status_code }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="耗时(ms)" width="110" align="center">
          <template slot-scope="scope">
            {{ scope.row.duration_ms }}
          </template>
        </el-table-column>
        <el-table-column label="时间" width="180">
          <template slot-scope="scope">
            {{ scope.row.created_at | datetime }}
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
import { getOperationLogs } from '@/api/log'

export default {
  name: 'OperationLogs',
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
        method: '',
        status_code: ''
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      getOperationLogs(this.listQuery).then(res => {
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
.app-container {
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
