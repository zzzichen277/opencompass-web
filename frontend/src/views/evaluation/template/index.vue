<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { request } from '@/service/request';

defineOptions({ name: 'TaskTemplates' });

const router = useRouter();
const templates = ref<Array<{
  id: string;
  name: string;
  description?: string;
  config: Record<string, any>;
  created_at: string;
}>>([]);
const loading = ref(false);
const showModal = ref(false);
const editingTemplate = ref<any>(null);

// Form data
const formData = ref({
  name: '',
  description: '',
  config: {
    models: [],
    datasets: [],
    accelerator: 'huggingface',
    resources: { gpu_count: 1, max_num_worker: 1 },
    eval_config: { mode: 'gen', max_out_len: 2048 },
  },
});

const API_PREFIX = '/api/v1/templates';

onMounted(async () => {
  await loadTemplates();
});

async function loadTemplates() {
  loading.value = true;
  try {
    const { data, error } = await request({ url: API_PREFIX, method: 'get' });
    if (!error && data) {
      templates.value = data;
    }
  } finally {
    loading.value = false;
  }
}

function handleCreateTemplate() {
  editingTemplate.value = null;
  formData.value = {
    name: '',
    description: '',
    config: {
      models: [],
      datasets: [],
      accelerator: 'huggingface',
      resources: { gpu_count: 1, max_num_worker: 1 },
      eval_config: { mode: 'gen', max_out_len: 2048 },
    },
  };
  showModal.value = true;
}

function handleEditTemplate(template: any) {
  editingTemplate.value = template;
  formData.value = {
    name: template.name,
    description: template.description || '',
    config: template.config,
  };
  showModal.value = true;
}

async function handleDeleteTemplate(id: string) {
  window.$dialog?.warning({
    title: '确认删除',
    content: '确定要删除该模板吗？',
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: async () => {
      const { error } = await request({ url: `${API_PREFIX}/${id}`, method: 'delete' });
      if (!error) {
        window.$message?.success('删除成功');
        await loadTemplates();
      }
    },
  });
}

function handleUseTemplate(template: any) {
  // Navigate to create task with template config
  router.push({
    path: '/evaluation/task/create',
    query: { template: template.id },
  });
}

async function handleSaveTemplate() {
  const url = editingTemplate.value ? `${API_PREFIX}/${editingTemplate.value.id}` : API_PREFIX;
  const method = editingTemplate.value ? 'put' : 'post';

  const { error } = await request({
    url,
    method,
    data: formData.value,
  });

  if (!error) {
    window.$message?.success(editingTemplate.value ? '更新成功' : '创建成功');
    showModal.value = false;
    await loadTemplates();
  }
}

function formatDate(dateStr: string) {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleString('zh-CN');
}

function getConfigSummary(config: Record<string, any>) {
  const models = config.models?.length || 0;
  const datasets = config.datasets?.length || 0;
  return `${models} 个模型, ${datasets} 个数据集`;
}
</script>

<template>
  <div class="h-full flex flex-col gap-4">
    <!-- Header -->
    <NCard title="任务模板" :bordered="false">
      <template #header-extra>
        <NButton type="primary" @click="handleCreateTemplate">
          <template #icon>
            <icon-ic-round-plus />
          </template>
          创建模板
        </NButton>
      </template>
    </NCard>

    <!-- Template List -->
    <NCard :bordered="false" class="flex-1 overflow-auto">
      <NGrid :x-gap="16" :y-gap="16" :cols="3" responsive="screen" item-responsive>
        <NGi v-for="template in templates" :key="template.id" class="break-inside-avoid">
          <NCard size="small" hoverable>
            <template #header>
              <div class="flex items-center justify-between">
                <span class="font-medium">{{ template.name }}</span>
                <NDropdown
                  :options="[
                    { label: '编辑', key: 'edit' },
                    { label: '删除', key: 'delete' },
                  ]"
                  @select="(key: string) => {
                    if (key === 'edit') handleEditTemplate(template);
                    if (key === 'delete') handleDeleteTemplate(template.id);
                  }"
                >
                  <NButton quaternary size="small">
                    <icon-mdi-dots-vertical />
                  </NButton>
                </NDropdown>
              </div>
            </template>
            <div class="flex flex-col gap-2">
              <p v-if="template.description" class="text-gray-500 text-sm">
                {{ template.description }}
              </p>
              <p class="text-gray-400 text-xs">
                {{ getConfigSummary(template.config) }}
              </p>
              <p class="text-gray-400 text-xs">
                创建于 {{ formatDate(template.created_at) }}
              </p>
            </div>
            <template #footer>
              <NButton type="primary" size="small" block @click="handleUseTemplate(template)">
                使用模板
              </NButton>
            </template>
          </NCard>
        </NGi>
      </NGrid>

      <NEmpty v-if="templates.length === 0 && !loading" description="暂无模板，点击上方按钮创建" />
    </NCard>

    <!-- Create/Edit Modal -->
    <NModal v-model:show="showModal" preset="card" :title="editingTemplate ? '编辑模板' : '创建模板'" style="width: 600px">
      <NForm label-placement="left" label-width="100">
        <NFormItem label="模板名称" required>
          <NInput v-model:value="formData.name" placeholder="请输入模板名称" />
        </NFormItem>
        <NFormItem label="描述">
          <NInput v-model:value="formData.description" type="textarea" placeholder="请输入模板描述" :rows="2" />
        </NFormItem>
        <NFormItem label="推理后端">
          <NSelect
            v-model:value="formData.config.accelerator"
            :options="[
              { label: 'HuggingFace', value: 'huggingface' },
              { label: 'vLLM', value: 'vllm' },
              { label: 'LMDeploy', value: 'lmdeploy' },
            ]"
          />
        </NFormItem>
        <NFormItem label="GPU 数量">
          <NInputNumber v-model:value="formData.config.resources.gpu_count" :min="0" :max="8" />
        </NFormItem>
      </NForm>
      <template #footer>
        <NSpace justify="end">
          <NButton @click="showModal = false">取消</NButton>
          <NButton type="primary" @click="handleSaveTemplate">保存</NButton>
        </NSpace>
      </template>
    </NModal>
  </div>
</template>

<style scoped></style>