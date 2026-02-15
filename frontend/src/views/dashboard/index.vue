<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h2>欢迎使用 Django Vue Admin 管理系统</h2>
      <p>基于 Django REST Framework + Vue Element Admin 构建</p>
    </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon user-icon">
              <i class="el-icon-user" />
            </div>
            <div class="stats-info">
              <h3>{{ stats.total_users }}</h3>
              <p>总用户数</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon active-icon">
              <i class="el-icon-success" />
            </div>
            <div class="stats-info">
              <h3>{{ stats.active_users }}</h3>
              <p>活跃用户</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon order-icon">
              <i class="el-icon-shopping-cart-2" />
            </div>
            <div class="stats-info">
              <h3>{{ stats.total_orders }}</h3>
              <p>总订单数</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon revenue-icon">
              <i class="el-icon-coin" />
            </div>
            <div class="stats-info">
              <h3>¥{{ stats.total_revenue.toLocaleString() }}</h3>
              <p>总收入</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :xs="24" :lg="12">
        <el-card class="chart-card">
          <div slot="header" class="card-header">
            <span>访问量统计</span>
          </div>
          <div class="chart-container">
            <div class="mock-chart">
              <div v-for="(value, index) in stats.chart_data.visits" :key="'visits-' + index" class="chart-bar">
                <div class="bar" :style="{ height: (value / 250 * 100) + '%' }">
                  <span>{{ value }}</span>
                </div>
                <span class="label">{{ stats.chart_data.dates[index] }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="12">
        <el-card class="chart-card">
          <div slot="header" class="card-header">
            <span>销售统计</span>
          </div>
          <div class="chart-container">
            <div class="mock-chart">
              <div v-for="(value, index) in stats.chart_data.sales" :key="'sales-' + index" class="chart-bar">
                <div class="bar sales-bar" :style="{ height: (value / 350 * 100) + '%' }">
                  <span>{{ value }}</span>
                </div>
                <span class="label">{{ stats.chart_data.dates[index] }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getDashboardStats } from '@/api/system'

export default {
  name: 'Dashboard',
  data() {
    return {
      stats: {
        total_users: 0,
        active_users: 0,
        total_orders: 0,
        total_revenue: 0,
        chart_data: {
          visits: [],
          sales: [],
          dates: []
        }
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      getDashboardStats().then(response => {
        if (response.success) {
          this.stats = response.data
        } else {
          // 使用默认数据
          this.stats = {
            total_users: 1256,
            active_users: 856,
            total_orders: 3420,
            total_revenue: 125680,
            chart_data: {
              visits: [120, 132, 101, 134, 90, 230, 210],
              sales: [220, 182, 191, 234, 290, 330, 310],
              dates: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            }
          }
        }
      }).catch(() => {
        // 使用默认数据
        this.stats = {
          total_users: 1256,
          active_users: 856,
          total_orders: 3420,
          total_revenue: 125680,
          chart_data: {
            visits: [120, 132, 101, 134, 90, 230, 210],
            sales: [220, 182, 191, 234, 290, 330, 310],
            dates: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
          }
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-container {
  padding: 20px;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 30px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  color: #fff;

  h2 {
    font-size: 28px;
    margin-bottom: 10px;
  }

  p {
    font-size: 16px;
    opacity: 0.9;
  }
}

.stats-row {
  margin-bottom: 20px;
}

.stats-card {
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

  .stats-content {
    display: flex;
    align-items: center;
    padding: 10px;

    .stats-icon {
      width: 60px;
      height: 60px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 20px;

      i {
        font-size: 30px;
        color: #fff;
      }

      &.user-icon {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      }

      &.active-icon {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      }

      &.order-icon {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      }

      &.revenue-icon {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
      }
    }

    .stats-info {
      flex: 1;

      h3 {
        font-size: 28px;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
      }

      p {
        font-size: 14px;
        color: #999;
        margin: 0;
      }
    }
  }
}

.chart-card {
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

  .card-header {
    font-size: 16px;
    font-weight: bold;
    color: #333;
  }

  .chart-container {
    height: 300px;
    padding: 20px 0;
  }

  .mock-chart {
    display: flex;
    justify-content: space-around;
    align-items: flex-end;
    height: 100%;
    padding: 20px;

    .chart-bar {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      margin: 0 5px;

      .bar {
        width: 40px;
        background: linear-gradient(180deg, #409EFF 0%, #53a8ff 100%);
        border-radius: 5px 5px 0 0;
        display: flex;
        align-items: flex-start;
        justify-content: center;
        padding-top: 5px;
        color: #fff;
        font-size: 12px;
        min-height: 20px;
        transition: all 0.3s;

        &:hover {
          transform: scaleY(1.05);
          box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
        }

        &.sales-bar {
          background: linear-gradient(180deg, #67C23A 0%, #85ce61 100%);

          &:hover {
            box-shadow: 0 4px 12px rgba(103, 194, 58, 0.3);
          }
        }
      }

      .label {
        margin-top: 10px;
        font-size: 12px;
        color: #666;
      }
    }
  }
}
</style>
