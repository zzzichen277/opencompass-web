<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { fetchLeaderboard, fetchTaskResults } from '@/service/api/evaluation';
import EvaluationRadarChart from '@/components/custom/evaluation-radar-chart.vue';
import EvaluationBarChart from '@/components/custom/evaluation-bar-chart.vue';
import EvaluationCompareChart from '@/components/custom/evaluation-compare-chart.vue';

defineOptions({ name: 'ResultLeaderboard' });

const router = useRouter();
const loading = ref(false);
const selectedDataset = ref<string | null>(null);
const activeTab = ref<'leaderboard' | 'charts'>('leaderboard');

// Leaderboard data
const leaderboardData = ref<Array<{
  model_id: string;
  model_name: string;
  dataset_id: string;
  dataset_name: string;
  score: number;
  rank: number;
}>>([]);

// Mock data for demonstration
const mockResults = ref([
  { model: 'GPT-4o', mmlu: 86.4, gsm8k: 92.1, humaneval: 90.2, math: 76.6, overall: 86.3 },
  { model: 'Claude-3.5-Sonnet', mmlu: 85.2, gsm8k: 91.8, humaneval: 89.5, math: 75.2, overall: 85.4 },
  { model: 'Qwen2.5-72B', mmlu: 84.1, gsm8k: 89.5, humaneval: 86.3, math: 73.1, overall: 83.3 },
  { model: 'InternLM3-8B', mmlu: 76.8, gsm8k: 82.1, humaneval: 78.5, math: 62.4, overall: 75.0 },
  { model: 'Llama3-70B', mmlu: 79.5, gsm8k: 85.2, humaneval: 81.7, math: 65.8, overall: 78.1 },
]);

const datasetOptions = [
  { label: '全部', value: null },
  { label: 'MMLU', value: 'mmlu' },
  { label: 'GSM8K', value: 'gsm8k' },
  { label: 'HumanEval', value: 'humaneval' },
  { label: 'MATH', value: 'math' },
];

const sortKey = ref<string>('overall');
const sortOrder = ref<'asc' | 'desc'>('desc');

const sortedResults = computed(() => {
  const sorted = [...mockResults.value].sort((a, b) => {
    const aVal = a[sortKey.value as keyof typeof a] as number;
    const bVal = b[sortKey.value as keyof typeof b] as number;
    return sortOrder.value === 'desc' ? bVal - aVal : aVal - bVal;
  });
  return sorted.map((r, i) => ({ ...r, rank: i + 1 }));
});

// Chart data
const radarData = computed(() => {
  if (sortedResults.value.length === 0) return {};
  const top = sortedResults.value[0];
  return {
    MMLU: top.mmlu,
    GSM8K: top.gsm8k,
    HumanEval: top.humaneval,
    MATH: top.math,
  };
});

const barData = computed(() => {
  return sortedResults.value.slice(0, 5).map(r => ({
    name: r.model,
    value: r.overall,
  }));
});

const compareCategories = ['MMLU', 'GSM8K', 'HumanEval', 'MATH'];
const compareSeries = computed(() => {
  return sortedResults.value.slice(0, 3).map(r => ({
    name: r.model,
    data: [r.mmlu, r.gsm8k, r.humaneval, r.math],
  }));
});

function handleSort(key: string) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'desc' ? 'asc' : 'desc';
  } else {
    sortKey.value = key;
    sortOrder.value = 'desc';
  }
}

function getScoreColor(score: number): string {
  if (score >= 85) return '#18a058';
  if (score >= 70) return '#2080f0';
  if (score >= 50) return '#f0a020';
  return '#d03050';
}

function handleExport() {
  window.$message?.info('报告导出功能开发中...');
}

onMounted(async () => {
  // Load real data
  // const { data } = await fetchLeaderboard();
  // if (data) leaderboardData.value = data;
});
</script>

<template>
  <div class="h-full flex flex-col gap-4">
    <!-- Header -->
    <NCard title="评测结果" :bordered="false">
      <template #header-extra>
        <NSpace>
          <NSelect
            v-model:value="selectedDataset"
            :options="datasetOptions"
            placeholder="筛选数据集"
            clearable
            style="width: 150px"
          />
          <NButton type="primary" @click="handleExport">
            <template #icon>
              <icon-mdi-download />
            </template>
            导出报告
          </NButton>
        </NSpace>
      </template>
    </NCard>

    <!-- Tabs -->
    <NCard :bordered="false">
      <NTabs v-model:value="activeTab">
        <NTab name="leaderboard">排行榜</NTab>
        <NTab name="charts">可视化</NTab>
      </NTabs>
    </NCard>

    <!-- Leaderboard Tab -->
    <NCard v-show="activeTab === 'leaderboard'" :bordered="false" class="flex-1 overflow-hidden">
      <NDataTable
        :data="sortedResults"
        :loading="loading"
        :columns="[
          { title: '排名', key: 'rank', width: 80 },
          { title: '模型', key: 'model', width: 200 },
          { title: 'MMLU', key: 'mmlu', sorter: true },
          { title: 'GSM8K', key: 'gsm8k', sorter: true },
          { title: 'HumanEval', key: 'humaneval', sorter: true },
          { title: 'MATH', key: 'math', sorter: true },
          { title: '综合', key: 'overall', sorter: true },
        ]"
        :row-key="(row: any) => row.model"
        flex-height
      >
        <template #rank="{ row }">
          <div class="flex items-center justify-center">
            <span
              v-if="row.rank <= 3"
              class="w-6 h-6 rounded-full flex items-center justify-center text-white text-sm font-bold"
              :style="{
                backgroundColor: row.rank === 1 ? '#ffd700' : row.rank === 2 ? '#c0c0c0' : '#cd7f32'
              }"
            >
              {{ row.rank }}
            </span>
            <span v-else class="text-gray-500">{{ row.rank }}</span>
          </div>
        </template>
        <template #mmlu="{ row }">
          <span :style="{ color: getScoreColor(row.mmlu), fontWeight: 'bold' }">{{ row.mmlu }}%</span>
        </template>
        <template #gsm8k="{ row }">
          <span :style="{ color: getScoreColor(row.gsm8k), fontWeight: 'bold' }">{{ row.gsm8k }}%</span>
        </template>
        <template #humaneval="{ row }">
          <span :style="{ color: getScoreColor(row.humaneval), fontWeight: 'bold' }">{{ row.humaneval }}%</span>
        </template>
        <template #math="{ row }">
          <span :style="{ color: getScoreColor(row.math), fontWeight: 'bold' }">{{ row.math }}%</span>
        </template>
        <template #overall="{ row }">
          <NTag :type="row.overall >= 80 ? 'success' : row.overall >= 60 ? 'warning' : 'error'" size="small">
            {{ row.overall }}%
          </NTag>
        </template>
      </NDataTable>
    </NCard>

    <!-- Charts Tab -->
    <div v-show="activeTab === 'charts'" class="flex-1 overflow-auto">
      <NGrid :x-gap="16" :y-gap="16" :cols="2" responsive="screen">
        <NGi>
          <NCard title="模型能力雷达图" :bordered="false">
            <EvaluationRadarChart :data="radarData" height="350" />
          </NCard>
        </NGi>
        <NGi>
          <NCard title="模型综合得分" :bordered="false">
            <EvaluationBarChart :data="barData" height="350" />
          </NCard>
        </NGi>
        <NGi :span="2">
          <NCard title="多模型能力对比" :bordered="false">
            <EvaluationCompareChart
              :categories="compareCategories"
              :series="compareSeries"
              height="400"
            />
          </NCard>
        </NGi>
      </NGrid>
    </div>
  </div>
</template>

<style scoped></style>