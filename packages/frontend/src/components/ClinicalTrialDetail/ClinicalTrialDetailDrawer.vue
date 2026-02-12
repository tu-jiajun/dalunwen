<template>
  <el-drawer
    v-model="visible"
    title="临床试验详情"
    direction="rtl"
    size="50%"
    :before-close="handleClose"
  >
    <div v-if="detailData" class="detail-container">
      <el-descriptions :column="1" border>
        <!-- 通用字段 -->
        <el-descriptions-item label="试验编号">
          {{ identifier }}
        </el-descriptions-item>
        <el-descriptions-item label="试验标题">
          {{ detailData.study_title }}
        </el-descriptions-item>
        <el-descriptions-item label="试验状态">
          <el-tag :type="getStatusType(detailData.study_status)">
            {{ detailData.study_status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="链接">
          <a :href="detailData.study_url" target="_blank" class="link">
            {{ detailData.study_url }}
          </a>
        </el-descriptions-item>

        <!-- 详细信息 -->
        <el-descriptions-item label="简要摘要">
          <div class="multiline-text">{{ detailData.brief_summary || '无' }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="研究结果">
          <div class="multiline-text">{{ detailData.study_results || '无' }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="适应症/疾病">
          {{ detailData.conditions || '无' }}
        </el-descriptions-item>
        <el-descriptions-item label="干预措施">
          {{ detailData.interventions || '无' }}
        </el-descriptions-item>
        
        <!-- 结果指标 -->
        <el-descriptions-item label="主要结果指标">
          <div class="multiline-text">{{ detailData.primary_outcome_measures || '无' }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="次要结果指标">
          <div class="multiline-text">{{ detailData.secondary_outcome_measures || '无' }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="其他结果指标">
          <div class="multiline-text">{{ detailData.other_outcome_measures || '无' }}</div>
        </el-descriptions-item>

        <!-- 参与者信息 -->
        <el-descriptions-item label="性别">
          {{ detailData.sex || '不限' }}
        </el-descriptions-item>
        <el-descriptions-item label="年龄">
          {{ detailData.age || '不限' }}
        </el-descriptions-item>
        <el-descriptions-item label="入组人数">
          {{ detailData.enrollment || 0 }}
        </el-descriptions-item>
        <el-descriptions-item label="阶段">
          {{ detailData.phases || 'N/A' }}
        </el-descriptions-item>

        <!-- 组织信息 -->
        <el-descriptions-item label="申办方">
          {{ detailData.sponsor || '无' }}
        </el-descriptions-item>
        <el-descriptions-item label="合作方">
          {{ detailData.collaborators || '无' }}
        </el-descriptions-item>
        <el-descriptions-item label="资助类型">
          {{ detailData.funder_type || '无' }}
        </el-descriptions-item>

        <!-- 研究设计 -->
        <el-descriptions-item label="研究类型">
          {{ detailData.study_type || '无' }}
        </el-descriptions-item>
        <el-descriptions-item label="研究设计">
          <div class="multiline-text">{{ detailData.study_design || '无' }}</div>
        </el-descriptions-item>
        
        <!-- 时间信息 -->
        <el-descriptions-item label="开始日期">
          {{ detailData.start_date || '无' }}
        </el-descriptions-item>
        <el-descriptions-item label="主要完成日期">
          {{ detailData.primary_completion_date || '无' }}
        </el-descriptions-item>
        <el-descriptions-item label="完成日期">
          {{ detailData.completion_date || '无' }}
        </el-descriptions-item>
        <el-descriptions-item label="首次发布日期">
          {{ detailData.first_posted || '无' }}
        </el-descriptions-item>
        <el-descriptions-item label="结果首次发布">
          {{ detailData.results_first_posted || '无' }}
        </el-descriptions-item>
        <el-descriptions-item label="最后更新发布">
          {{ detailData.last_update_posted || '无' }}
        </el-descriptions-item>

        <!-- 其他 -->
        <el-descriptions-item label="地点">
          <div class="multiline-text">{{ detailData.locations || '无' }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="文档">
          <div class="multiline-text">{{ detailData.study_documents || '无' }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="其他ID">
          {{ detailData.other_ids || '无' }}
        </el-descriptions-item>
      </el-descriptions>
    </div>
    <el-empty v-else description="暂无数据" />
  </el-drawer>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { ClinicalTrial } from '@/types/clinicaltrial';

const props = defineProps<{
  modelValue: boolean;
  data: ClinicalTrial | null;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
}>();

// 双向绑定 drawer 的可见性
const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
});

// 当前展示的数据
const detailData = computed(() => props.data);

// 获取试验编号（兼容 USA 和 China）
const identifier = computed(() => {
  if (!detailData.value) return '';
  // 使用类型守卫或直接判断属性
  if ('nct_number' in detailData.value) {
    return detailData.value.nct_number;
  } else {
    return (detailData.value as any).reg_number || '';
  }
});

// 关闭处理
const handleClose = (done: () => void) => {
  emit('update:modelValue', false);
  done();
};

// 状态标签颜色辅助函数
const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    'Completed': 'success',
    'Recruiting': 'primary',
    'Active, not recruiting': 'info',
    'Terminated': 'danger',
    'Withdrawn': 'danger',
    'Enrolling by invitation': 'warning',
    'Not yet recruiting': 'info'
  };
  return statusMap[status] || 'info';
};
</script>

<style scoped>
.detail-container {
  padding: 0 10px;
}

.multiline-text {
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 200px;
  overflow-y: auto;
}

.link {
  color: #409eff;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

:deep(.el-descriptions__label) {
  width: 120px;
  font-weight: bold;
}
</style>
