<template>
  <div class="app-container">
    <div class="page-header">
      <h2>脚本管理</h2>
      <p>管理系统脚本与相关配置</p>
    </div>

    <el-row :gutter="16" class="stat-row">
      <el-col :span="6">
        <el-card>
          <div class="stat-item">
            <div class="stat-label">脚本总数</div>
            <div class="stat-value">12</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div class="stat-item">
            <div class="stat-label">启用中</div>
            <div class="stat-value">8</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div class="stat-item">
            <div class="stat-label">本月新增</div>
            <div class="stat-value">3</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div class="stat-item">
            <div class="stat-label">异常脚本</div>
            <div class="stat-value warning">1</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="box-card">
      <div class="filter-container">
        <el-input
          v-model="query.keyword"
          placeholder="搜索脚本名称"
          style="width: 220px;"
          class="filter-item"
          clearable
        />
        <el-select v-model="query.status" class="filter-item" clearable placeholder="状态">
          <el-option label="启用" value="enabled" />
          <el-option label="停用" value="disabled" />
        </el-select>
        <el-button class="filter-item" type="primary" icon="el-icon-search">
          搜索
        </el-button>
        <el-button class="filter-item" type="success" icon="el-icon-plus">
          新建脚本
        </el-button>
      </div>

      <el-table :data="list" border fit highlight-current-row style="margin-top: 20px;">
        <el-table-column label="脚本名称" min-width="200">
          <template slot-scope="scope">
            {{ scope.row.name }}
          </template>
        </el-table-column>
        <el-table-column label="类型" width="120">
          <template slot-scope="scope">
            {{ scope.row.type }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.enabled ? 'success' : 'info'" size="small">
              {{ scope.row.enabled ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="最近执行" width="180">
          <template slot-scope="scope">
            {{ scope.row.last_run | datetime }}
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="220">
          <template slot-scope="scope">
            <el-button size="mini" type="primary">编辑</el-button>
            <el-button size="mini" type="warning">执行</el-button>
            <el-button size="mini" type="danger">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'ScriptManagement',
  data() {
    return {
      query: {
        keyword: '',
        status: ''
      },
      list: [
        { name: '数据同步脚本', type: '定时', enabled: true, last_run: '2026-02-15T10:12:00+08:00' },
        { name: '告警推送脚本', type: '事件', enabled: true, last_run: '2026-02-15T09:30:00+08:00' },
        { name: '清理缓存脚本', type: '定时', enabled: false, last_run: '2026-02-10T22:00:00+08:00' }
      ]
    }
  }
}
</script>

<style lang="scss" scoped>
.page-header {
  margin-bottom: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #4facfe 0%, #00c6ff 100%);
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

.stat-row {
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 8px;

  .stat-label {
    color: #909399;
    font-size: 13px;
  }

  .stat-value {
    font-size: 24px;
    font-weight: 600;
    color: #303133;
  }

  .stat-value.warning {
    color: #e6a23c;
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
