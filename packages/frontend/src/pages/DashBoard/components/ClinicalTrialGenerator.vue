<template>
  <div class="clinical-trial-generator">
    <el-container class="generator-container">
      <!-- 左侧输入区 -->
      <el-aside width="40%" class="input-panel">
        <el-card class="box-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>输入需求</span>
              <el-button type="primary" link @click="clearConversation">新建对话</el-button>
            </div>
          </template>
          
          <div class="input-content">
            <el-input
              v-model="userIdea"
              type="textarea"
              :rows="15"
              placeholder="请输入您的临床试验想法、研究背景、目标人群等信息..."
              resize="none"
            />
            
            <el-upload
              class="upload-demo"
              action="#"
              :auto-upload="false"
              :on-change="handleFileChange"
              :show-file-list="true"
              v-model:file-list="fileList"
              style="margin-top: 20px;"
            >
              <el-button type="primary" plain>上传参考文件 (txt/md)</el-button>
              <template #tip>
                <div class="el-upload__tip">
                  支持 txt, md 文件，内容将追加到输入框
                </div>
              </template>
            </el-upload>

            <div class="action-area">
              <el-button type="primary" :loading="loading" @click="generateProtocol" style="width: 100%;">
                生成临床试验方案
              </el-button>
            </div>
          </div>
        </el-card>
      </el-aside>

      <!-- 右侧生成区 -->
      <el-main class="output-panel">
        <el-card class="box-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>生成的临床试验方案</span>
              <el-button v-if="generatedContent" type="success" link @click="copyContent">复制内容</el-button>
            </div>
          </template>
          
          <div class="output-content" v-loading="loading">
            <div v-if="generatedContent" class="markdown-body" v-html="renderedContent"></div>
            <el-empty v-else description="暂无生成内容，请在左侧输入并点击生成"></el-empty>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { ElMessage } from 'element-plus';
import type { UploadFile } from 'element-plus';
import MarkdownIt from 'markdown-it';
import { aiApi } from '@/utils/api/modules/ai';

const md = new MarkdownIt();

// State
const userIdea = ref('');
const generatedContent = ref('');
const loading = ref(false);
const fileList = ref<UploadFile[]>([]);

// Storage Key
const STORAGE_KEY = 'clinical_trial_generator_state';

// Rendered Content
const renderedContent = computed(() => {
  return md.render(generatedContent.value);
});

// Load state from local storage
onMounted(() => {
  const savedState = localStorage.getItem(STORAGE_KEY);
  if (savedState) {
    try {
      const parsed = JSON.parse(savedState);
      userIdea.value = parsed.userIdea || '';
      generatedContent.value = parsed.generatedContent || '';
    } catch (e) {
      console.error('Failed to load saved state', e);
    }
  }
});

// Save state to local storage automatically
watch([userIdea, generatedContent], () => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({
    userIdea: userIdea.value,
    generatedContent: generatedContent.value
  }));
});

// Methods
const clearConversation = () => {
  userIdea.value = '';
  generatedContent.value = '';
  fileList.value = [];
  localStorage.removeItem(STORAGE_KEY);
  ElMessage.success('已清空对话内容');
};

const handleFileChange = (uploadFile: UploadFile) => {
  const rawFile = uploadFile.raw;
  if (!rawFile) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    const text = e.target?.result as string;
    if (text) {
      userIdea.value += `\n\n--- 文件内容 (${uploadFile.name}) ---\n${text}\n------------------\n`;
      ElMessage.success(`已读取文件: ${uploadFile.name}`);
    }
  };
  reader.onerror = () => {
    ElMessage.error('读取文件失败');
  };
  reader.readAsText(rawFile);
};

const generateProtocol = async () => {
  if (!userIdea.value.trim()) {
    ElMessage.warning('请输入您的想法或需求');
    return;
  }

  loading.value = true;
  try {
    const messages = [
      { role: 'system', content: `你是一个专业的临床试验方案设计专家。请根据用户的需求，生成一份详细、专业的临床试验方案。
      方案内容必须包含以下字段信息（请不要包含nctTitle, 如果还有别的内容，请补充）：
      - study title: 研究标题
      - acronym: 简称
      - study status: 研究状态
      - brief summary: 简要摘要
      - study results: 研究结果
      - conditions: 研究病症
      - interventions: 干预措施
      - primary outcome measures: 主要结果指标
      - secondary outcome measures: 次要结果指标
      - other outcome measures: 其他结果指标
      - sponsor: 申办方
      - collaborators: 合作方
      - sex: 性别
      - age: 年龄
      - phases: 阶段
      - enrollment: 招募人数
      - funder type: 资助类型
      - study type: 研究类型
      - study design: 研究设计
      - other ids: 其他ID
      - start date: 开始日期
      - primary completion date: 主要完成日期
      - completion date: 完成日期
      - first posted: 首次发布日期
      - results first posted: 结果首次发布日期
      - last update posted: 最后更新发布日期
      - locations: 地点
      - study documents: 研究文件

      请确保生成的内容结构清晰，逻辑严密。` },
      { role: 'user', content: userIdea.value }
    ];

    const res = await aiApi.generateProtocol(messages);
    console.log("AI Generation Response:", res);
    
    // Assuming the response structure matches standard Axios response wrapped by our interceptor
    // The interceptor returns response.data directly
    if (res && res.code === 200) {
      generatedContent.value = res.data;
      ElMessage.success('生成成功');
    } else {
      ElMessage.error(res.msg || '生成失败');
    }
  } catch (error) {
    console.error(error);
    ElMessage.error('生成请求失败，请稍后重试');
  } finally {
    loading.value = false;
  }
};

const copyContent = async () => {
  try {
    await navigator.clipboard.writeText(generatedContent.value);
    ElMessage.success('内容已复制到剪贴板');
  } catch (err) {
    ElMessage.error('复制失败');
  }
};
</script>

<style scoped>
.clinical-trial-generator {
  height: 100%;
  padding: 20px;
  background-color: #f5f7fa;
  box-sizing: border-box;
}

.generator-container {
  height: calc(100vh - 120px); /* Adjust based on header height */
  gap: 20px;
}

.input-panel, .output-panel {
  height: 100%;
  overflow: hidden;
  padding: 0;
}

.box-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

:deep(.el-card__body) {
  flex: 1;
  overflow: hidden;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.input-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

:deep(.el-textarea__inner) {
  flex: 1;
  font-family: inherit;
}

.action-area {
  margin-top: 20px;
}

.output-content {
  height: 100%;
  overflow-y: auto;
  padding: 10px;
  background-color: #fff;
}

.markdown-body {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
}

/* Add basic markdown styles if not imported */
.markdown-body h1, .markdown-body h2, .markdown-body h3 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-body ul, .markdown-body ol {
  padding-left: 2em;
}

.markdown-body blockquote {
  padding: 0 1em;
  color: #6a737d;
  border-left: 0.25em solid #dfe2e5;
}
</style>
