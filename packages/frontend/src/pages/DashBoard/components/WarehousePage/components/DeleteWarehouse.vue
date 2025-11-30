<!-- components/DeleteWarehouse.vue -->
<template>
  <!-- 按钮触发弹窗（可自定义按钮样式） -->
  <el-button
    type="danger"
    size="small"
    @click="openDeleteModal"
    :disabled="!row.id"
  >
    删除
  </el-button>

  <!-- 删除确认模态框 -->
  <el-dialog
    :model-value="modalVisible"
    @update:model-value="modalVisible = $event"
    title="删除确认"
    width="400px"
    :close-on-click-modal="false"
  >
    <div class="delete-tips">
      确定要删除仓库【{{ row.warehouse_name || '未知仓库' }}】吗？<br/>
    </div>
    <template #footer>
      <el-button @click="modalVisible = false">取消</el-button>
      <el-button
        type="danger"
        @click="handleConfirmDelete"
        :loading="deleteLoading"
      >
        确定删除
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue';
import { ElMessage } from 'element-plus';

// 定义接收的Props：当前行数据（至少包含id和warehouse_name）
const props = defineProps<{
  row: {
    id: number;
    warehouse_name: string;
  };
}>();

// 定义触发的事件：通知父组件执行删除（传递要删除的ID）
const emit = defineEmits<{
  (e: 'confirm-delete', rowId: number): void;
}>();

// 模态框显隐状态
const modalVisible = ref(false);
// 删除加载状态
const deleteLoading = ref(false);

// 打开删除确认弹窗
const openDeleteModal = () => {
  if (!props.row.id) {
    ElMessage.warning('暂无可删除的仓库数据！');
    return;
  }
  modalVisible.value = true;
};

// 确认删除：触发事件通知父组件
const handleConfirmDelete = () => {
  deleteLoading.value = true;
  // 向父组件传递要删除的ID
  emit('confirm-delete', props.row.id);
  // 关闭弹窗 + 重置加载状态
  modalVisible.value = false;
  deleteLoading.value = false;
};
</script>