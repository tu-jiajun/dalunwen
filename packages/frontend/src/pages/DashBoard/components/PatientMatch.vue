<template>
  <div class="patient-match-container">
    <el-row :gutter="20" class="match-layout">
      <!-- Left Side: Input Form -->
      <el-col :span="8" class="input-section">
        <el-card class="box-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>患者信息录入</span>
            </div>
          </template>
          
          <el-form :model="form" label-position="top" :rules="rules" ref="formRef">
            <el-form-item label="试验库" prop="registry">
              <el-tabs v-model="form.registry" @tab-change="handleRegistryChange">
                <el-tab-pane label="美国" name="usa" />
                <el-tab-pane label="中国" name="china" />
              </el-tabs>
            </el-form-item>

            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="form.age" :min="0" :max="120" style="width: 100%;" />
            </el-form-item>
            
            <el-form-item label="性别" prop="gender">
              <el-select v-model="form.gender" placeholder="请选择性别" style="width: 100%;">
                <el-option label="男 (Male)" value="Male" />
                <el-option label="女 (Female)" value="Female" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="疾病/病情描述" prop="condition">
              <el-input 
                v-model="form.condition" 
                type="textarea" 
                :rows="6"
                placeholder="请输入疾病名称（如 Liver Cancer）或具体病情描述..."
              />
            </el-form-item>
            
            <el-form-item label="招募状态" prop="isRecruiting">
              <el-switch
                v-model="form.isRecruiting"
                active-text="仅显示招募中 (Recruiting/Not yet recruiting)"
                inactive-text="全部状态"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" class="submit-btn" :loading="loading" @click="handleMatch">
                开始智能匹配
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      
      <!-- Right Side: Results -->
      <el-col :span="16" class="result-section">
        <el-card class="box-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>匹配结果 (Top 10)</span>
              <el-tag v-if="results.length" type="success">匹配完成</el-tag>
            </div>
          </template>
          
          <div v-loading="loading" class="result-list">
            <el-empty v-if="!results.length && !loading" description="请输入患者信息开始匹配" />
            
            <div v-for="item in results" :key="item.trial_id" class="match-item">
              <div class="match-score">
                <el-progress type="circle" :percentage="item.score" :width="60" :color="getScoreColor(item.score)" />
                <span class="score-label">匹配度</span>
              </div>
              <div class="match-info">
                <div class="match-header">
                  <h3 class="match-title">
                  <a v-if="item.url" :href="item.url" target="_blank">{{ item.title }}</a>
                  <span v-else>{{ item.title }}</span>
                  </h3>
                <el-tag size="small">{{ item.trial_id }}</el-tag>
                  <el-tag size="small" type="info" style="margin-left: 8px;">{{ item.phases }}</el-tag>
                <el-tag size="small" type="warning" style="margin-left: 8px;">{{ item.registry === 'china' ? '中国' : '美国' }}</el-tag>
                </div>
                <p class="match-reason"><strong>推荐理由：</strong>{{ item.reason }}</p>
                <div class="match-meta">
                  <span class="label">针对病症：</span> {{ item.conditions }}
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import type { FormInstance, FormRules } from 'element-plus';
import { aiApi } from '@/utils/api/modules/ai'; // We'll add matchPatient to aiApi or create matchApi

const formRef = ref<FormInstance>();
const loading = ref(false);

const form = reactive({
  age: 45,
  gender: 'Male',
  condition: '',
  isRecruiting: true,
  registry: 'usa' as 'usa' | 'china'
});

const rules = reactive<FormRules>({
  condition: [
    { required: true, message: '请输入疾病或病情描述', trigger: 'blur' },
    { min: 2, message: '描述太短', trigger: 'blur' }
  ]
});

interface MatchResult {
  trial_id: string;
  registry: 'usa' | 'china';
  title: string;
  url: string;
  score: number;
  reason: string;
  conditions: string;
  phases: string;
  study_status: string;
}

const results = ref<MatchResult[]>([]);

const getScoreColor = (score: number) => {
  if (score >= 80) return '#67C23A';
  if (score >= 60) return '#E6A23C';
  return '#F56C6C';
};

const handleMatch = async () => {
  if (!formRef.value) return;
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      results.value = [];
      try {
        const res: any = await aiApi.matchPatient(form);
        if (res && res.code === 200) {
          results.value = res.data;
          if (res.data.length === 0) {
            ElMessage.info('未找到符合初步筛选条件的临床试验，请尝试调整关键词');
          } else {
            ElMessage.success('匹配完成');
          }
        } else {
          ElMessage.error(res.msg || '匹配失败');
        }
      } catch (error) {
        console.error(error);
        ElMessage.error('请求出错，请稍后重试');
      } finally {
        loading.value = false;
      }
    }
  });
};

const handleRegistryChange = () => {
  results.value = [];
};
</script>

<style scoped>
.patient-match-container {
  padding: 20px;
  height: 100%;
  box-sizing: border-box;
}

.match-layout {
  height: calc(100vh - 120px);
}

.input-section, .result-section {
  height: 100%;
}

.box-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

:deep(.el-card__body) {
  flex: 1;
  overflow-y: auto;
}

.submit-btn {
  width: 100%;
  margin-top: 20px;
}

.result-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.match-item {
  display: flex;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 16px;
  background: #fff;
  transition: all 0.3s;
}

.match-item:hover {
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.match-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  min-width: 80px;
}

.score-label {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.match-info {
  flex: 1;
}

.match-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.match-title {
  margin: 0 10px 0 0;
  font-size: 16px;
  font-weight: 600;
}

.match-title a {
  color: #303133;
  text-decoration: none;
}

.match-title a:hover {
  color: #409EFF;
}

.match-reason {
  font-size: 14px;
  color: #606266;
  margin: 8px 0;
  line-height: 1.5;
  background: #f4f4f5;
  padding: 8px;
  border-radius: 4px;
}

.match-meta {
  font-size: 13px;
  color: #909399;
}
</style>
