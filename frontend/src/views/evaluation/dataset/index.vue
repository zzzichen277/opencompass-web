<script setup lang="ts">
import { ref } from 'vue';

defineOptions({ name: 'DatasetManage' });

const datasets = ref([
  { id: '1', name: 'MMLU', type: 'builtin', category: 'qa', samples: 14042, description: '大规模多任务语言理解' },
  { id: '2', name: 'GSM8K', type: 'builtin', category: 'math', samples: 1319, description: '数学应用题求解' },
  { id: '3', name: 'HumanEval', type: 'builtin', category: 'code', samples: 164, description: '代码生成评测' },
  { id: '4', name: 'C-Eval', type: 'builtin', category: 'qa', samples: 13946, description: '中文语言能力评测' },
  { id: '5', name: 'MATH', type: 'builtin', category: 'math', samples: 5000, description: '数学竞赛题评测' },
  { id: '6', name: 'BBH', type: 'builtin', category: 'reasoning', samples: 6520, description: '大规模任务评测基准' },
]);

const categoryOptions = [
  { label: '问答', value: 'qa' },
  { label: '数学', value: 'math' },
  { label: '代码', value: 'code' },
  { label: '推理', value: 'reasoning' },
  { label: '主观', value: 'subjective' },
];

const selectedCategory = ref<string | null>(null);
const searchKeyword = ref('');
const showModal = ref(false);

const filteredDatasets = ref(datasets.value);

function handleSearch() {
  filteredDatasets.value = datasets.value.filter(d => {
    const matchCategory = !selectedCategory.value || d.category === selectedCategory.value;
    const matchKeyword = !searchKeyword.value || d.name.toLowerCase().includes(searchKeyword.value.toLowerCase());
    return matchCategory && matchKeyword;
  });
}

function handleUploadDataset() {
  showModal.value = true;
}

function handleViewDataset(id: string) {
  window.$message?.info(`查看数据集 ${id}`);
}
</script>

<template>
  <div class="h-full flex flex-col gap-4">
    <!-- Header -->
    <NCard title="数据集管理" :bordered="false">
      <template #header-extra>
        <NButton type="primary" @click="handleUploadDataset">
          <template #icon>
            <icon-ic-round-upload />
          </template>
          上传数据集
        </NButton>
      </template>
      <NSpace>
        <NInput v-model:value="searchKeyword" placeholder="搜索数据集" clearable @update:value="handleSearch">
          <template #prefix>
            <icon-ic-round-search />
          </template>
        </NInput>
        <NSelect
          v-model:value="selectedCategory"
          :options="categoryOptions"
          placeholder="选择类别"
          clearable
          style="width: 150px"
          @update:value="handleSearch"
        />
      </NSpace>
    </NCard>

    <!-- Dataset Grid -->
    <NCard :bordered="false" class="flex-1 overflow-auto">
      <NGrid :x-gap="16" :y-gap="16" :cols="3" responsive="screen" item-responsive>
        <NGi v-for="dataset in filteredDatasets" :key="dataset.id" class="break-inside-avoid">
          <NCard size="small" hoverable class="cursor-pointer" @click="handleViewDataset(dataset.id)">
            <div class="flex flex-col gap-2">
              <div class="flex items-center justify-between">
                <span class="font-medium text-lg">{{ dataset.name }}</span>
                <NTag :type="dataset.type === 'builtin' ? 'info' : 'warning'" size="small">
                  {{ dataset.type === 'builtin' ? '内置' : '自定义' }}
                </NTag>
              </div>
              <p class="text-gray-500 text-sm line-clamp-2">{{ dataset.description }}</p>
              <div class="flex items-center gap-4 text-sm text-gray-400">
                <span>
                  <icon-mdi-database class="mr-1" />
                  {{ dataset.samples }} 样本
                </span>
                <span>
                  <icon-mdi-tag class="mr-1" />
                  {{ dataset.category }}
                </span>
              </div>
            </div>
          </NCard>
        </NGi>
      </NGrid>
    </NCard>

    <!-- Upload Modal -->
    <NModal v-model:show="showModal" preset="card" title="上传自定义数据集" style="width: 600px">
      <NForm label-placement="left" label-width="100">
        <NFormItem label="数据集名称" required>
          <NInput placeholder="请输入数据集名称" />
        </NFormItem>
        <NFormItem label="类别" required>
          <NSelect :options="categoryOptions" placeholder="选择数据集类别" />
        </NFormItem>
        <NFormItem label="描述">
          <NInput type="textarea" placeholder="请输入数据集描述" :rows="3" />
        </NFormItem>
        <NFormItem label="数据文件">
          <NUpload :max="1" accept=".json,.csv" :default-upload="false">
            <NButton>选择文件</NButton>
          </NUpload>
        </NFormItem>
      </NForm>
      <template #footer>
        <NSpace justify="end">
          <NButton @click="showModal = false">取消</NButton>
          <NButton type="primary">上传</NButton>
        </NSpace>
      </template>
    </NModal>
  </div>
</template>

<style scoped></style>