<template>
  <el-container>
    <el-main>
      <!-- 表格展示临床试验数据 -->
      <el-table :data="clinicalTrials" border style="width: 100%">
        <el-table-column prop="reg_number" label="REG编号" width="160" />
        <el-table-column prop="study_title" label="研究标题" min-width="300" />
        <el-table-column prop="study_status" label="研究状态" width="180" />
        <el-table-column prop="study_type" label="研究类型" width="150" />
        <el-table-column prop="conditions" label="研究病症" min-width="200" />
        <el-table-column prop="enrollment" label="招募人数" width="120" />
        <el-table-column prop="start_date" label="开始日期" width="150" />
        <el-table-column prop="last_update_posted" label="最后更新" width="150" />
        <!-- 添加到仓库按钮列 -->
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <AddToWarehouseButton 
              :row-data="scope.row" 
              :user-id="currentUserId"
              @added-to-warehouse="handleAddedToWarehouse"
            />
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页组件 -->
      <el-pagination
        style="margin-top: 20px; text-align: right"
        layout="prev, pager, next, jumper, ->, total"
        :total="totalCount"
        :page-size="pageSize"
        :current-page="currentPage"
        @current-change="handlePageChange"
        :disabled="loading"
      />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { ElMessage, ElLoading } from "element-plus";
import api from '@/utils/api/index';
import type { ClinicalTrialUSA as ClinicalTrial } from '@/types/clinicaltrial';
import AddToWarehouseButton from './components/AddToWarehouseButton.vue';

const clinicalTrials = ref<ClinicalTrial[]>([]);
const currentPage = ref(1);
const pageSize = ref(10);
const totalCount = ref(0);
const loading = ref(false);

// 获取当前用户ID
const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
const currentUserId = userInfo.userId ?? 0;

const fetchClinicalTrials = async () => {
  loading.value = true;
  const loadingInstance = ElLoading.service({
    lock: true,
    text: "加载临床试验数据中...",
    background: "rgba(255, 255, 255, 0.7)",
  });

  try {
    const res = await api.CTChina({
      page: currentPage.value,
      size: pageSize.value,
    });

    clinicalTrials.value = res.data.list || [];
    totalCount.value = res.data.total || res.data.totalElements || 0;

    if (clinicalTrials.value.length === 0 && currentPage.value === 1) {
      ElMessage.info("暂无临床试验数据");
    }
  } catch (error) {
    const errMsg = error instanceof Error ? error.message : "获取临床试验数据失败";
    ElMessage.error(errMsg);
    clinicalTrials.value = [];
    totalCount.value = 0;
  } finally {
    loading.value = false;
    loadingInstance.close();
  }
};

// 分页切换事件
const handlePageChange = (page: number) => {
  currentPage.value = page;
  fetchClinicalTrials();
};

// 处理添加到仓库事件
const handleAddedToWarehouse = (warehouseId: number, rowData: any) => {
  console.log('添加到仓库:', warehouseId, rowData);
  // 这里可以添加具体的业务逻辑，比如调用API将数据保存到指定仓库
  ElMessage.success(`已添加到仓库: ${warehouseId}`);
};

// 组件挂载时初始化数据
onMounted(() => {
  fetchClinicalTrials();
});

defineExpose({
  fetchClinicalTrials,
});
</script>

<style scoped>

</style>