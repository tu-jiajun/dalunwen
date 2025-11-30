<!-- components/AddWarehouse.vue -->
<template>
  <!-- 核心修改：v-model → :model-value + @update:model-value -->
  <el-dialog
    @update:model-value="handleModelUpdate"
    title="新增仓库"
    width="500px"
    @close="handleClose"
  >
    <!-- 其余内容不变 -->
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="100px"
      style="max-width: 400px"
    >
      <el-form-item label="归属用户ID" prop="user_id">
        <el-input v-model="formData.user_id" placeholder="请输入用户ID" disabled />
      </el-form-item>
      <el-form-item label="仓库名称" prop="warehouse_name">
        <el-input v-model="formData.warehouse_name" placeholder="请输入仓库名称" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="submitLoading">提交</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, watch } from 'vue';
import type { FormInstance, FormRules } from 'element-plus';

// 写死仓库数据类型
interface WarehouseForm {
  user_id: number;
  warehouse_name: string;
}

const props = defineProps<{
  userId: number;
}>();

// 修改Emits：新增update:model-value事件（通知父组件更新visible）
const emit = defineEmits<{
  (e: 'submit', formData: WarehouseForm): void;
  (e: 'update:model-value', value: boolean): void;  // 新增：更新显隐状态
}>();

// 其余变量不变
const formRef = ref<FormInstance>();
const submitLoading = ref(false);
const formData = ref<WarehouseForm>({
  user_id: props.userId,
  warehouse_name: ''
});

const formRules = ref<FormRules>({
  warehouse_name: [
    { required: true, message: '请输入仓库名称', trigger: 'blur' },
    { min: 1, max: 100, message: '仓库名称长度需在1-100个字符之间', trigger: 'blur' }
  ],
  user_id: [
    { required: true, message: '归属用户ID不能为空', trigger: 'blur' }
  ]
});

// 新增：处理el-dialog的状态更新
const handleModelUpdate = (value: boolean) => {
  emit('update:model-value', value);
};

// 取消按钮/关闭弹窗：通知父组件隐藏
const handleCancel = () => {
  emit('update:model-value', false);
  formRef.value?.resetFields();
};

// 关闭弹窗：同步通知父组件
const handleClose = () => {
  emit('update:model-value', false);
  formRef.value?.resetFields();
};

// 提交表单逻辑不变
const handleSubmit = async () => {
  if (!formRef.value) return;
  try {
    await formRef.value.validate();
    submitLoading.value = true;
    emit('submit', formData.value);
    // 提交成功后隐藏弹窗
    emit('update:model-value', false);
  } catch (error) {
    console.error('新增仓库表单校验失败：', error);
  } finally {
    submitLoading.value = false;
  }
};

// 监听用户ID变化
watch(
  () => props.userId,
  (val) => {
    formData.value.user_id = val;
  },
  { immediate: true }
);
</script>