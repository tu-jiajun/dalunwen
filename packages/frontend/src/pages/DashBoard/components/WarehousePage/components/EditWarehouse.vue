<!-- components/EditWarehouse.vue -->
<template>
  <!-- 核心修改：v-model → :model-value + @update:model-value -->
  <el-dialog
    @update:model-value="handleModelUpdate"
    title="编辑仓库"
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
      <el-form-item label="仓库ID" prop="id">
        <el-input v-model="formData.id" placeholder="仓库ID" disabled />
      </el-form-item>
      <el-form-item label="归属用户ID" prop="user_id">
        <el-input v-model="formData.user_id" placeholder="归属用户ID" disabled />
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

interface WarehouseForm {
  id: number;
  user_id: number;
  warehouse_name: string;
}

const props = defineProps<{
  initialData: WarehouseForm;
}>();

// 修改Emits：新增update:model-value
const emit = defineEmits<{
  (e: 'submit', formData: WarehouseForm): void;
  (e: 'update:model-value', value: boolean): void;
}>();

// 其余变量不变
const formRef = ref<FormInstance>();
const submitLoading = ref(false);
const formData = ref<WarehouseForm>({
  id: 0,
  user_id: 0,
  warehouse_name: ''
});

const formRules = ref<FormRules>({
  warehouse_name: [
    { required: true, message: '请输入仓库名称', trigger: 'blur' },
    { min: 1, max: 100, message: '仓库名称长度需在1-100个字符之间', trigger: 'blur' }
  ]
});

// 新增：处理el-dialog状态更新
const handleModelUpdate = (value: boolean) => {
  emit('update:model-value', value);
};

// 取消按钮
const handleCancel = () => {
  emit('update:model-value', false);
  formRef.value?.resetFields();
};

// 关闭弹窗
const handleClose = () => {
  emit('update:model-value', false);
  formRef.value?.resetFields();
};

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return;
  try {
    await formRef.value.validate();
    submitLoading.value = true;
    emit('submit', formData.value);
    emit('update:model-value', false); // 提交后隐藏
  } catch (error) {
    console.error('编辑仓库表单校验失败：', error);
  } finally {
    submitLoading.value = false;
  }
};

// 监听初始数据
watch(
  () => props.initialData,
  (val) => {
    formData.value = { ...val };
  },
  { immediate: true }
);
</script>