<template>
  <div class="header">
    <!-- 当前路径显示 -->
    <div class="currentPath">{{ currentPath }}</div>
    <!-- 右侧用户信息+退出登录 -->
    <div class="right-header">
      <span class="evaluator-name" style="margin-right: 20px;">您好，{{ userName }}</span>
      <el-button type="danger" class="logout" @click="handleLogout">
        <el-icon><SwitchButton /></el-icon>
        退出登录
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { SwitchButton } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { computed } from 'vue';

const router = useRouter();

const props = defineProps<{
  currentPath: string;
}>();

const userName = computed(() => {
  try {
    const userInfo = localStorage.getItem('userInfo');
    if (!userInfo) return '未知用户';
    const parsedUser = JSON.parse(userInfo);  
    return parsedUser.username || '未知用户';
  } catch (error) {
    console.error('解析用户信息失败：', error);
    return '未知用户';
  }
});

const handleLogout = () => {
  try {
    // 清除本地存储
    localStorage.clear();
    sessionStorage.clear();
    ElMessage.success('退出登录成功');
    router.push('/login');
  } catch (error) {
    console.error('退出登录失败：', error);
    ElMessage.error('退出登录失败，请重试');
  }
};
</script>

<style scoped>
.header {
  width: calc(100% - 40px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
}

.currentPath {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.evaluator-name {
  font-size: 14px;
}

.logout {
  background-color: #ff4d4f !important; /* 强制红色按钮 */
  border-color: #ff4d4f !important;
  transition: all 0.3s ease; /* 过渡动画，更流畅 */
}

</style>
