<template>
  <el-container>
    <el-main>
      <!-- 表格 -->
      <el-table
        :data="trialList"
        border
        style="width: 100%"
        v-loading="loading"
        :row-key="(row) => row.id"
      >
        <el-table-column prop="id" label="记录ID" width="100" />
        <el-table-column label="试验编号">
          <template #default="scope">
            <span v-if="scope.row.nct_number">{{ scope.row.nct_number }}</span>
            <span v-else-if="scope.row.reg_number">{{ scope.row.reg_number }}</span>
            <span v-else>无编号</span>
          </template>
        </el-table-column>
        <el-table-column label="试验标题">
          <template #default="scope">
            <span v-if="scope.row.clinicalUSA">{{ scope.row.clinicalUSA.study_title }}</span>
            <span v-else-if="scope.row.clinicalChina">{{ scope.row.clinicalChina.study_title }}</span>
            <span v-else>暂无标题</span>
          </template>
        </el-table-column>
        <el-table-column label="试验状态">
          <template #default="scope">
            <span v-if="scope.row.clinicalUSA">{{ scope.row.clinicalUSA.study_status }}</span>
            <span v-else-if="scope.row.clinicalChina">{{ scope.row.clinicalChina.study_status }}</span>
            <span v-else>未知状态</span>
          </template>
        </el-table-column>
        <!-- 操作列 -->
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <el-button
              type="danger"
              size="small"
              @click="removeTrialFromWarehouse(scope.row)"
            >
              移除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="totalCount"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        style="margin-top: 20px; justify-content: center;"
      />

    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import apiClient from '@/utils/api/apiClient';

import type { ClinicalTrialWarehouseWithDetails } from '@/types/clinicalTrialWarehouse';

// ========== Props ==========
const props = defineProps<{
  warehouseId: string;
}>();

// ========== 响应式数据 ==========
const currentPage = ref(1);
const pageSize = ref(10);
const totalCount = ref(0);
const loading = ref(false);
const trialList = ref<ClinicalTrialWarehouseWithDetails[]>([]);

// ========== 方法 ==========
// 获取仓库中的临床试验列表
const fetchTrialList = async () => {
  if (!props.warehouseId) return;
  
  loading.value = true;
  try {
    const res = await apiClient.get(
      `api/warehouse/${props.warehouseId}/trials?pageNum=${currentPage.value}&pageSize=${pageSize.value}`
    );
    
    if (res.data.code === 200) {
      trialList.value = res.data.data.list || [];
      totalCount.value = res.data.data.total || 0;
      
      if (trialList.value.length === 0 && currentPage.value === 1) {
        ElMessage.info("当前仓库暂无临床试验");
      }
    } else {
      ElMessage.error(res.data.msg || "获取临床试验数据失败");
      trialList.value = [];
      totalCount.value = 0;
    }
  } catch (error) {
    const errMsg = error instanceof Error ? error.message : "获取临床试验数据失败";
    ElMessage.error(errMsg);
    trialList.value = [];
    totalCount.value = 0;
  } finally {
    loading.value = false;
  }
};

// 移除临床试验
const removeTrialFromWarehouse: (row: ClinicalTrialWarehouseWithDetails) => void = (row) => {
  const trialIdentifier = row.nct_number || row.reg_number;
  if (!trialIdentifier) {
    ElMessage.error("无法识别试验标识符");
    return;
  }
  
  ElMessageBox.confirm(
    `确定要从仓库中移除试验 ${trialIdentifier} 吗？`,
    '确认移除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      const res = await apiClient.delete(
        `api/warehouse/${props.warehouseId}/trials?trialIdentifier=${trialIdentifier}`
      );
      
      if (res.data.code === 200) {
        ElMessage.success("移除成功");
        fetchTrialList(); // 刷新列表
      } else {
        ElMessage.error(res.data.msg || "移除失败");
      }
    } catch (error) {
      const errMsg = error instanceof Error ? error.message : "移除失败";
      ElMessage.error(errMsg);
    }
  }).catch(() => {
    // 用户取消操作
  });
};

// 分页相关方法
const handleSizeChange = (val: number) => {
  pageSize.value = val;
  currentPage.value = 1;
  fetchTrialList();
};

const handleCurrentChange = (val: number) => {
  currentPage.value = val;
  fetchTrialList();
};

// 监听仓库ID变化
watch(() => props.warehouseId, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    currentPage.value = 1;
    fetchTrialList();
  }
});

// 初始化加载
onMounted(() => {
  fetchTrialList();
});

// 暴露方法给父组件
defineExpose({
  fetchTrialList
});
</script>

<style scoped>
.el-pagination {
  margin-top: 20px;
  justify-content: center;
}
</style>