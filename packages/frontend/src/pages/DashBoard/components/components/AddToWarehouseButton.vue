<template>
  <!-- 添加到仓库按钮 -->
  <el-button type="primary" size="small" @click="openWarehouseDialog">
    添加到仓库
  </el-button>

  <!-- 选择仓库对话框 -->
  <el-dialog
    v-model="dialogVisible"
    title="选择仓库"
    width="500px"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="100px"
    >
      <el-form-item label="选择仓库" prop="warehouseId">
        <el-select 
          v-model="formData.warehouseId" 
          placeholder="请选择仓库" 
          style="width: 100%"
          :loading="warehouseLoading"
        >
          <el-option
            v-for="warehouse in warehouseList"
            :key="warehouse.id"
            :label="warehouse.warehouse_name"
            :value="warehouse.id"
          />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button 
        type="primary" 
        @click="handleSubmit" 
        :loading="submitLoading"
        :disabled="warehouseLoading || !formData.warehouseId"
      >
        确定
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { FormInstance, FormRules } from 'element-plus';
import { ElMessage } from 'element-plus';
import api from '@/utils/api/index';
import type { Warehouse } from '@/types/warehouse';

const props = defineProps<{
  rowData: any; // 行数据
  userId: number; // 用户ID
}>();

const emit = defineEmits<{
  (e: 'added-to-warehouse', warehouseId: number, rowData: any): void;
}>();

// 对话框可见性
const dialogVisible = ref(false);

// 表单引用
const formRef = ref<FormInstance>();

// 提交加载状态
const submitLoading = ref(false);

// 仓库列表加载状态
const warehouseLoading = ref(false);

// 仓库列表
const warehouseList = ref<Warehouse[]>([]);

// 表单数据
const formData = ref({
  warehouseId: null as number | null
});

// 表单验证规则
const formRules = ref<FormRules>({
  warehouseId: [
    { required: true, message: '请选择仓库', trigger: 'change' }
  ]
});

// 打开对话框
const openWarehouseDialog = async () => {
  dialogVisible.value = true;
  await fetchWarehouseList();
};

// 获取仓库列表
const fetchWarehouseList = async () => {
  warehouseLoading.value = true;
  try {
    const res = await api.getWarehouseByUserId(props.userId.toString());
    warehouseList.value = res.data.list || [];
  } catch (error) {
    const errMsg = error instanceof Error ? error.message : "获取仓库列表失败";
    ElMessage.error(errMsg);
  } finally {
    warehouseLoading.value = false;
  }
};

// 取消按钮
const handleCancel = () => {
  dialogVisible.value = false;
  resetForm();
};

// 关闭对话框
const handleClose = () => {
  resetForm();
};

// 重置表单
const resetForm = () => {
  formData.value.warehouseId = null;
  formRef.value?.resetFields();
};

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return;
  
  try {
    await formRef.value.validate();
    if (!formData.value.warehouseId) {
      ElMessage.warning('请选择仓库');
      return;
    }
    
    submitLoading.value = true;
    
    // 这里可以添加将数据保存到仓库的逻辑
    // 调用API将数据保存到仓库
    await api.addTrialToWarehouse(formData.value.warehouseId, props.rowData);

    // 触发事件通知父组件
    emit('added-to-warehouse', formData.value.warehouseId, props.rowData);
    
    // 关闭对话框
    dialogVisible.value = false;
    resetForm();
    
    ElMessage.success('已添加到仓库');
  } catch (error) {
    const errMsg = error instanceof Error ? error.message : "操作失败";
    ElMessage.error(errMsg);
  } finally {
    submitLoading.value = false;
  }
};

// 组件挂载时初始化
onMounted(() => {
  // 可以在这里做一些初始化工作
});
</script>