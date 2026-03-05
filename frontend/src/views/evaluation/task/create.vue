<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { createTask } from '@/service/api/evaluation';
import { fetchModelList } from '@/service/api/evaluation';
import { fetchDatasetList } from '@/service/api/evaluation';

defineOptions({ name: 'EvaluationTaskCreate' });

const router = useRouter();
const currentStep = ref(0);
const loading = ref(false);

// Step 1: Basic info
const taskName = ref('');
const taskDescription = ref('');

// Step 2: Model selection
const selectedModels = ref<string[]>([]);
const availableModels = ref<Array<{ id: string; name: string; type: string }>>([]);
const modelLoading = ref(false);

// Step 3: Dataset selection
const selectedDatasets = ref<string[]>([]);
const availableDatasets = ref<Array<{ id: string; name: string; category: string; sample_count?: number }>>([]);
const datasetLoading = ref(false);

// Step 4: Configuration
const config = ref({
  accelerator: 'huggingface',
  resources: {
    gpu_count: 1,
    max_num_worker: 1,
  },
  eval_config: {
    mode: 'gen',
    max_out_len: 2048,
  },
});

const steps = [
  { title: '基本信息', description: '任务名称和描述' },
  { title: '选择模型', description: '选择要评测的模型' },
  { title: '选择数据集', description: '选择评测数据集' },
  { title: '资源配置', description: 'GPU和运行参数' },
];

// Load models and datasets on mount
(async () => {
  modelLoading.value = true;
  const { data: models } = await fetchModelList();
  if (models) {
    availableModels.value = models;
  }
  modelLoading.value = false;

  datasetLoading.value = true;
  const { data: datasets } = await fetchDatasetList();
  if (datasets) {
    availableDatasets.value = datasets;
  }
  datasetLoading.value = false;
})();

const canProceed = computed(() => {
  switch (currentStep.value) {
    case 0:
      return taskName.value.trim() !== '';
    case 1:
      return selectedModels.value.length > 0;
    case 2:
      return selectedDatasets.value.length > 0;
    default:
      return true;
  }
});

function handleNext() {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++;
  }
}

function handlePrev() {
  if (currentStep.value > 0) {
    currentStep.value--;
  }
}

async function handleSubmit() {
  loading.value = true;

  const { error } = await createTask({
    name: taskName.value,
    description: taskDescription.value,
    config: {
      models: selectedModels.value,
      datasets: selectedDatasets.value,
      accelerator: config.value.accelerator,
      resources: config.value.resources,
      eval_config: config.value.eval_config,
    },
  });

  loading.value = false;

  if (!error) {
    window.$message?.success('任务创建成功');
    router.push('/evaluation/task');
  }
}
</script>

<template>
  <div class="h-full flex flex-col gap-4">
    <NCard title="创建评测任务" :bordered="false">
      <NSteps :current="currentStep" :steps="steps" />
    </NCard>

    <NCard :bordered="false" class="flex-1 overflow-auto">
      <!-- Step 1: Basic Info -->
      <div v-show="currentStep === 0" class="max-w-2xl mx-auto py-8">
        <NForm label-placement="left" label-width="100">
          <NFormItem label="任务名称" required>
            <NInput v-model:value="taskName" placeholder="请输入任务名称" />
          </NFormItem>
          <NFormItem label="任务描述">
            <NInput
              v-model:value="taskDescription"
              type="textarea"
              placeholder="请输入任务描述（可选）"
              :rows="4"
            />
          </NFormItem>
        </NForm>
      </div>

      <!-- Step 2: Model Selection -->
      <div v-show="currentStep === 1" class="py-8">
        <NSpin :show="modelLoading">
          <NCheckboxGroup v-model:value="selectedModels">
            <NSpace vertical class="w-full">
              <NCard
                v-for="model in availableModels"
                :key="model.id"
                size="small"
                hoverable
                class="cursor-pointer"
              >
                <div class="flex items-center gap-4">
                  <NCheckbox :value="model.id" />
                  <div class="flex-1">
                    <div class="font-medium">{{ model.name }}</div>
                    <div class="text-gray-500 text-sm">{{ model.type }}</div>
                  </div>
                </div>
              </NCard>
              <NEmpty v-if="availableModels.length === 0 && !modelLoading" description="暂无模型，请先添加模型" />
            </NSpace>
          </NCheckboxGroup>
        </NSpin>
      </div>

      <!-- Step 3: Dataset Selection -->
      <div v-show="currentStep === 2" class="py-8">
        <NSpin :show="datasetLoading">
          <NCheckboxGroup v-model:value="selectedDatasets">
            <NSpace vertical class="w-full">
              <NCard
                v-for="dataset in availableDatasets"
                :key="dataset.id"
                size="small"
                hoverable
                class="cursor-pointer"
              >
                <div class="flex items-center gap-4">
                  <NCheckbox :value="dataset.id" />
                  <div class="flex-1">
                    <div class="font-medium">{{ dataset.name }}</div>
                    <div class="flex gap-4 text-gray-500 text-sm">
                      <span>类型: {{ dataset.category }}</span>
                      <span v-if="dataset.sample_count">样本数: {{ dataset.sample_count }}</span>
                    </div>
                  </div>
                </div>
              </NCard>
              <NEmpty v-if="availableDatasets.length === 0 && !datasetLoading" description="暂无数据集" />
            </NSpace>
          </NCheckboxGroup>
        </NSpin>
      </div>

      <!-- Step 4: Configuration -->
      <div v-show="currentStep === 3" class="max-w-2xl mx-auto py-8">
        <NForm label-placement="left" label-width="120">
          <NFormItem label="推理后端">
            <NSelect
              v-model:value="config.accelerator"
              :options="[
                { label: 'HuggingFace', value: 'huggingface' },
                { label: 'vLLM', value: 'vllm' },
                { label: 'LMDeploy', value: 'lmdeploy' },
              ]"
            />
          </NFormItem>
          <NFormItem label="GPU 数量">
            <NInputNumber v-model:value="config.resources.gpu_count" :min="0" :max="8" />
          </NFormItem>
          <NFormItem label="并行 Worker">
            <NInputNumber v-model:value="config.resources.max_num_worker" :min="1" :max="8" />
          </NFormItem>
          <NFormItem label="评测模式">
            <NSelect
              v-model:value="config.eval_config.mode"
              :options="[
                { label: '生成模式 (gen)', value: 'gen' },
                { label: '困惑度模式 (ppl)', value: 'ppl' },
              ]"
            />
          </NFormItem>
          <NFormItem label="最大输出长度">
            <NInputNumber v-model:value="config.eval_config.max_out_len" :min="256" :max="8192" :step="256" />
          </NFormItem>
        </NForm>
      </div>

      <!-- Actions -->
      <div class="flex justify-between pt-4 border-t border-gray-200">
        <NButton v-if="currentStep > 0" @click="handlePrev">上一步</NButton>
        <div v-else></div>
        <NSpace>
          <NButton v-if="currentStep < steps.length - 1" type="primary" :disabled="!canProceed" @click="handleNext">
            下一步
          </NButton>
          <NButton v-else type="primary" :loading="loading" @click="handleSubmit">
            创建任务
          </NButton>
        </NSpace>
      </div>
    </NCard>
  </div>
</template>

<style scoped></style>