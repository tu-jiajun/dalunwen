<template>
  <el-container>
    <el-main>
      <!-- 操作按钮区：仅保留新增 + 刷新 -->
      <div class="action-bar">
        <el-button type="primary" @click="openAddModal">新增仓库</el-button>
      </div>

      <!-- 表格 -->
      <el-table
        :data="warehouseList"
        border
        style="width: 100%"
        v-loading="loading"
        :row-key="(row) => row.id"
        @row-click="handleRowClick"
      >
        <el-table-column prop="id" label="仓库ID" width="100" />
        <el-table-column prop="warehouse_name" label="仓库名称" />
        <!-- 新增：操作列（编辑+删除） -->
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <el-button
              type="warning"
              size="small"
              @click="openEditModal(scope.row)"
            >
              编辑
            </el-button>
            <DeleteWarehouse
              :row="scope.row"
              @confirm-delete="handleConfirmDelete"
            />
          </template>
        </el-table-column>
      </el-table>

      <AddWarehouse
        v-model="addModalVisible"
        :user-id="currentUserId"
        @submit="handleAddWarehouse"
      />

      <EditWarehouse
        v-model="editModalVisible"
        :initial-data="currentEditRow"
        @submit="handleEditWarehouse"
      />

    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { useRouter } from "vue-router";
import api from "@/utils/api";

import AddWarehouse from "./components/AddButton.vue";
import EditWarehouse from "./components/EditWarehouse.vue";
import DeleteWarehouse from "./components/DeleteWarehouse.vue";

import type { Warehouse } from '@/types/warehouse';

const router = useRouter();

// ========== 基础配置（修正currentUserId非响应式） ==========
const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
const currentUserId = ref(userInfo.userId ?? 0); // 改为响应式，避免取值错误
const currentPage = ref(1);
const pageSize = ref(10);
const totalCount = ref(0);
const loading = ref(false);
const warehouseList = ref<Warehouse[]>([]);
const searchKeyword = ref('');

// ========== 弹窗/编辑状态 ==========
const addModalVisible = ref(false);
const editModalVisible = ref(false);
const currentEditRow = ref<Warehouse>({ id: 0, user_id: 0, warehouse_name: '' }); // 当前编辑的行数据

// 获取仓库列表
const fetchWarehouseList = async () => {
  loading.value = true;
  try {
    const res = await api.getWarehouseByUserId(currentUserId.value);
    warehouseList.value = res.data.list || [];
    totalCount.value = res.data.total || 0;

    if (warehouseList.value.length === 0 && currentPage.value === 1) {
      ElMessage.info("当前用户仓库暂无信息");
    }
  } catch (error) {
    const errMsg = error instanceof Error ? error.message : "获取仓库数据失败";
    ElMessage.error(errMsg);
    warehouseList.value = [];
    totalCount.value = 0;
  } finally {
    loading.value = false;
  }
};

// 2. 新增仓库
const handleAddWarehouse = async (formData: { user_id: number; warehouse_name: string }) => {
  try {
    await api.createWarehouse(formData);
    ElMessage.success("新增仓库成功");
    addModalVisible.value = false;
    fetchWarehouseList();
  } catch (error) {
    const errMsg = error instanceof Error ? error.message : "新增仓库失败";
    ElMessage.error(errMsg);
  }
};

// 3. 打开编辑弹窗（接收当前行数据）
const openEditModal = (row: Warehouse) => {
  currentEditRow.value = { ...row }; // 赋值当前行数据
  editModalVisible.value = true;
};

// 4. 编辑仓库提交
const handleEditWarehouse = async (formData: { id: number; warehouse_name: string }) => {
  try {
    await api.updateWarehouse(formData.id, { warehouse_name: formData.warehouse_name });
    ElMessage.success("编辑仓库成功");
    editModalVisible.value = false;
    fetchWarehouseList();
  } catch (error) {
    const errMsg = error instanceof Error ? error.message : "编辑仓库失败";
    ElMessage.error(errMsg);
  }
};

// 处理删除确认（父组件执行实际的API调用）
const handleConfirmDelete = async (rowId: number) => {
  try {
    await api.deleteWarehouse(rowId); // 调用删除API
    ElMessage.success("删除仓库成功");
    fetchWarehouseList(); // 刷新列表
  } catch (error) {
    const errMsg = error instanceof Error ? error.message : "删除仓库失败";
    ElMessage.error(errMsg);
  }
};

// 6. 搜索仓库
const handleSearchWarehouse = (keyword: string) => {
  searchKeyword.value = keyword;
  currentPage.value = 1;
  fetchWarehouseList();
};

// 7. 打开新增弹窗
const openAddModal = () => {
  addModalVisible.value = true;
};

const handleRowClick = (row: Warehouse) => {
  router.push(`/ct-rep/${row.id}`); 
};

onMounted(() => {
  fetchWarehouseList();
});

defineExpose({
  fetchWarehouseList
});
</script>

<style scoped>
.action-bar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

</style>
