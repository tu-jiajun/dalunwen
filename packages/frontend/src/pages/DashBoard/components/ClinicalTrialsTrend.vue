<template>
  <div class="trend-analysis-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="box-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>历年注册试验数量趋势分析</span>
            </div>
          </template>
          <iframe src="http://localhost:8000/api/analysis/trend" class="chart-iframe"></iframe>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card class="box-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>不同治疗方式的年度注册数量</span>
            </div>
          </template>
          <iframe src="http://localhost:8000/api/analysis/treatment" class="chart-iframe"></iframe>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card class="box-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>全球临床试验分布</span>
            </div>
          </template>
          <iframe src="http://localhost:8000/api/analysis/map" class="chart-iframe"></iframe>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card class="box-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>主要分类变量权重分析</span>
            </div>
          </template>
          <iframe src="http://localhost:8000/api/analysis/weights" class="chart-iframe"></iframe>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>试验失败原因分布</span>
            </div>
          </template>
          <iframe src="http://localhost:8000/api/analysis/failure" class="chart-iframe"></iframe>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card class="box-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>各个类别生存分析</span>
            </div>
          </template>
          <iframe src="http://localhost:8000/api/analysis/survival" class="chart-iframe"></iframe>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
// No script needed for simple iframes
</script>

<style scoped>
.trend-analysis-container {
  padding: 20px;
}
.chart-iframe {
  width: 100%;
  height: 520px; /* Slightly larger than chart height to avoid scrollbars */
  border: none;
  overflow: hidden;
}
</style>
