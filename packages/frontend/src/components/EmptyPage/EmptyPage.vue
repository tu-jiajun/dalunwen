<template>
  <div class="empty-page-container">
    <el-empty 
      :image-size="200"
      description="功能开发中，敬请期待..."
    >
      <template #description>
        <div class="description-text">
          <h2>🚧 功能正在施工中</h2>
          <p>当前页面 {{ pageName }} 暂未开发完成</p>
        </div>
      </template>
      <el-button type="primary" @click="goBack">返回上一页</el-button>
    </el-empty>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

// 获取当前页面的名称（从路由元信息或路径中获取）
const pageName = computed(() => {
  return (route.meta.breadcrumb as string) || '此模块';
});

// 返回上一页
const goBack = () => {
  router.back();
};
</script>

<style scoped>
.empty-page-container {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #fff;
}

.description-text h2 {
  color: #303133;
  margin-bottom: 10px;
}

.description-text p {
  color: #909399;
  font-size: 14px;
}
</style>
