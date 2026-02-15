<template>
  <div class="app-container">
    <div class="page-header">
      <h2>图表示例</h2>
      <p>展示 Element UI 和数据可视化组件的使用</p>
    </div>

    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :lg="12">
        <el-card class="chart-card">
          <div slot="header" class="card-header">
            <span>柱状图示例</span>
          </div>
          <div class="chart-container">
            <div class="mock-bar-chart">
              <div v-for="(item, index) in barData" :key="index" class="bar-item">
                <div class="bar" :style="{ height: item.value + '%', background: item.color }">
                  <span class="value">{{ item.value }}</span>
                </div>
                <span class="label">{{ item.label }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :lg="12">
        <el-card class="chart-card">
          <div slot="header" class="card-header">
            <span>饼图示例</span>
          </div>
          <div class="chart-container">
            <div class="mock-pie-chart">
              <div class="pie-legend">
                <div v-for="(item, index) in pieData" :key="index" class="legend-item">
                  <span class="color" :style="{ background: item.color }" />
                  <span class="label">{{ item.label }}: {{ item.value }}%</span>
                </div>
              </div>
              <div class="pie" :style="{ background: pieGradient }" />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :xs="24" :sm="24" :lg="24">
        <el-card class="chart-card">
          <div slot="header" class="card-header">
            <span>进度条示例</span>
          </div>
          <div class="progress-container">
            <div class="progress-item">
              <span class="label">用户增长</span>
              <el-progress :percentage="75" :color="progressColors[0]" />
            </div>
            <div class="progress-item">
              <span class="label">订单完成</span>
              <el-progress :percentage="60" :color="progressColors[1]" />
            </div>
            <div class="progress-item">
              <span class="label">目标达成</span>
              <el-progress :percentage="90" :color="progressColors[2]" />
            </div>
            <div class="progress-item">
              <span class="label">系统负载</span>
              <el-progress :percentage="45" :color="progressColors[3]" />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :xs="24" :sm="24" :lg="24">
        <el-card class="chart-card">
          <div slot="header" class="card-header">
            <span>统计卡片</span>
          </div>
          <el-row :gutter="20">
            <el-col :xs="12" :sm="6" :lg="6">
              <div class="stat-item">
                <div class="stat-icon primary">
                  <i class="el-icon-user" />
                </div>
                <div class="stat-content">
                  <h3>1,254</h3>
                  <p>用户总数</p>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="6" :lg="6">
              <div class="stat-item">
                <div class="stat-icon success">
                  <i class="el-icon-shopping-cart-2" />
                </div>
                <div class="stat-content">
                  <h3>3,420</h3>
                  <p>订单总数</p>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="6" :lg="6">
              <div class="stat-item">
                <div class="stat-icon warning">
                  <i class="el-icon-view" />
                </div>
                <div class="stat-content">
                  <h3>8,521</h3>
                  <p>访问量</p>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="6" :lg="6">
              <div class="stat-item">
                <div class="stat-icon danger">
                  <i class="el-icon-coin" />
                </div>
                <div class="stat-content">
                  <h3>¥125,680</h3>
                  <p>总收入</p>
                </div>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'ChartExample',
  data() {
    return {
      barData: [
        { label: '一月', value: 65, color: '#409EFF' },
        { label: '二月', value: 78, color: '#67C23A' },
        { label: '三月', value: 90, color: '#E6A23C' },
        { label: '四月', value: 85, color: '#F56C6C' },
        { label: '五月', value: 70, color: '#909399' }
      ],
      pieData: [
        { label: '直接访问', value: 35, color: '#409EFF' },
        { label: '邮件营销', value: 20, color: '#67C23A' },
        { label: '联盟广告', value: 25, color: '#E6A23C' },
        { label: '视频广告', value: 20, color: '#F56C6C' }
      ],
      progressColors: ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C']
    }
  },
  computed: {
    pieGradient() {
      return `conic-gradient(
        ${this.pieData[0].color} 0% ${this.pieData[0].value}%,
        ${this.pieData[1].color} ${this.pieData[0].value}% ${this.pieData[0].value + this.pieData[1].value}%,
        ${this.pieData[2].color} ${this.pieData[0].value + this.pieData[1].value}% ${this.pieData[0].value + this.pieData[1].value + this.pieData[2].value}%,
        ${this.pieData[3].color} ${this.pieData[0].value + this.pieData[1].value + this.pieData[2].value}% 100%
      )`
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
    padding: 20px;
  }
}

.mock-bar-chart {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  height: 100%;

  .bar-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0 10px;

    .bar {
      width: 50px;
      border-radius: 5px 5px 0 0;
      display: flex;
      align-items: flex-start;
      justify-content: center;
      padding-top: 5px;
      color: #fff;
      font-size: 14px;
      font-weight: bold;
      min-height: 20px;
      transition: all 0.3s;

      &:hover {
        transform: scaleY(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
      }

      .value {
        color: #fff;
      }
    }

    .label {
      margin-top: 10px;
      font-size: 12px;
      color: #666;
    }
  }
}

.mock-pie-chart {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 100%;

  .pie-legend {
    .legend-item {
      display: flex;
      align-items: center;
      margin-bottom: 15px;

      .color {
        width: 20px;
        height: 20px;
        border-radius: 3px;
        margin-right: 10px;
      }

      .label {
        font-size: 14px;
        color: #666;
      }
    }
  }

  .pie {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    transition: transform 0.3s;

    &:hover {
      transform: scale(1.05);
    }
  }
}

.progress-container {
  .progress-item {
    margin-bottom: 25px;

    .label {
      display: block;
      margin-bottom: 10px;
      font-size: 14px;
      color: #666;
    }
  }
}

.stat-item {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  margin-bottom: 20px;

  .stat-icon {
    width: 60px;
    height: 60px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 20px;

    i {
      font-size: 28px;
      color: #fff;
    }

    &.primary {
      background: linear-gradient(135deg, #409EFF 0%, #53a8ff 100%);
    }

    &.success {
      background: linear-gradient(135deg, #67C23A 0%, #85ce61 100%);
    }

    &.warning {
      background: linear-gradient(135deg, #E6A23C 0%, #ebb563 100%);
    }

    &.danger {
      background: linear-gradient(135deg, #F56C6C 0%, #f78989 100%);
    }
  }

  .stat-content {
    flex: 1;

    h3 {
      font-size: 24px;
      font-weight: bold;
      color: #333;
      margin: 0 0 5px 0;
    }

    p {
      font-size: 14px;
      color: #999;
      margin: 0;
    }
  }
}
</style>
