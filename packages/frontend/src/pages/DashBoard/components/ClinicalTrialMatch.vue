<template>
  <div class="trial-match-container">
    <el-row :gutter="20" class="match-layout">
      <el-col :span="8" class="input-section">
        <el-card class="box-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>源临床试验</span>
            </div>
          </template>

          <el-form :model="form" label-position="top" :rules="rules" ref="formRef">
            <el-form-item label="试验库" prop="registry">
              <el-tabs v-model="form.registry" @tab-change="handleRegistryChange">
                <el-tab-pane label="美国" name="usa" />
                <el-tab-pane label="中国" name="china" />
              </el-tabs>
            </el-form-item>

            <el-form-item label="招募状态" prop="isRecruiting">
              <el-switch
                v-model="form.isRecruiting"
                active-text="仅显示招募中"
                inactive-text="全部状态"
              />
            </el-form-item>

            <el-form-item label="试验ID（可选）" prop="trialId">
              <el-input
                v-model="form.trialId"
                placeholder="美国：NCTxxxx；中国：ChiCTRxxxx"
                clearable
              />
            </el-form-item>

            <el-form-item label="试验文本（可选）" prop="trialText">
              <el-input
                v-model="form.trialText"
                type="textarea"
                :rows="8"
                placeholder="可粘贴标题/摘要/疾病等信息（trialId 与 trialText 至少填一个）"
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" class="submit-btn" :loading="loading" @click="handleMatch">
                开始匹配
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="16" class="result-section">
        <el-card class="box-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>匹配结果 (Top 10)</span>
              <el-tag v-if="results.length" type="success">匹配完成</el-tag>
            </div>
          </template>

          <div v-loading="loading" class="result-list">
            <el-empty v-if="!results.length && !loading" description="请输入源临床试验信息开始匹配" />

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
                  <el-tag size="small" type="warning" style="margin-left: 8px;">{{ item.registry === 'china' ? '中国' : '美国' }}</el-tag>
                  <el-tag v-if="item.phases" size="small" type="info" style="margin-left: 8px;">{{ item.phases }}</el-tag>
                </div>
                <p class="match-reason"><strong>推荐理由：</strong>{{ item.reason }}</p>
                <div class="match-meta">
                  <span class="label">针对病症：</span> {{ item.conditions }}
                </div>
                <div class="match-meta" v-if="item.study_status">
                  <span class="label">状态：</span> {{ item.study_status }}
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
import { aiApi } from '@/utils/api/modules/ai';

const formRef = ref<FormInstance>();
const loading = ref(false);

const form = reactive({
  registry: 'usa' as 'usa' | 'china',
  isRecruiting: true,
  trialId: '',
  trialText: ''
});

const rules = reactive<FormRules>({
  trialId: [
    {
      validator: (_rule, _value, callback) => {
        const hasId = String(form.trialId || '').trim().length > 0;
        const hasText = String(form.trialText || '').trim().length > 0;
        if (!hasId && !hasText) callback(new Error('trialId 与 trialText 至少填一个'));
        else callback();
      },
      trigger: 'blur'
    }
  ],
  trialText: [
    {
      validator: (_rule, _value, callback) => {
        const hasId = String(form.trialId || '').trim().length > 0;
        const hasText = String(form.trialText || '').trim().length > 0;
        if (!hasId && !hasText) callback(new Error('trialId 与 trialText 至少填一个'));
        else callback();
      },
      trigger: 'blur'
    }
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

const handleRegistryChange = () => {
  results.value = [];
};

const handleMatch = async () => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid) => {
    if (!valid) return;
    loading.value = true;
    results.value = [];
    try {
      const payload = {
        registry: form.registry,
        isRecruiting: form.isRecruiting,
        trialId: String(form.trialId || '').trim() || undefined,
        trialText: String(form.trialText || '').trim() || undefined
      };
      const res: any = await aiApi.matchTrial(payload);
      if (res && res.code === 200) {
        results.value = res.data;
        if (!res.data?.length) ElMessage.info('未找到匹配结果，请尝试调整源试验文本或切换试验库');
        else ElMessage.success('匹配完成');
      } else {
        ElMessage.error(res.msg || '匹配失败');
      }
    } catch (e) {
      console.error(e);
      ElMessage.error('请求出错，请稍后重试');
    } finally {
      loading.value = false;
    }
  });
};
</script>

<style scoped>
.trial-match-container {
  padding: 20px;
  height: 100%;
  box-sizing: border-box;
}

.match-layout {
  height: calc(100vh - 120px);
}

.input-section,
.result-section {
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
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
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
  color: #409eff;
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

