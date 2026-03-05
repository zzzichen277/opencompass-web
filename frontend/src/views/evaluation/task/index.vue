<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { fetchTaskList, startTask, stopTask, deleteTask } from '@/service/api/evaluation';
import { useEvaluationWebSocket } from '@/hooks/business/useEvaluationWebSocket';

defineOptions({ name: 'EvaluationTaskList' });

const router = useRouter();
const { connected, connect, subscribe, unsubscribe, onProgress, onCompleted } = useEvaluationWebSocket();

interface Task {
  id: string;
  name: string;
  description?: string;
  status: string;
  progress: number;
  created_at: string;
  started_at?: string;
  completed_at?: string;
}

const tasks = ref<Task[]>([]);
const loading = ref(false);

const statusColors: Record<string, 'default' | 'primary' | 'info' | 'success' | 'warning' | 'error'> = {
  pending: 'warning',
  running: 'info',
  completed: 'success',
  failed: 'error',
  cancelled: 'default',
};

const statusLabels: Record<string, string> = {
  pending: '等待中',
  running: '运行中',
  completed: '已完成',
  failed: '失败',
  cancelled: '已取消',
};

onMounted(async () => {
  await loadTasks();
  connect();
});

async function loadTasks() {
  loading.value = true;
  try {
    const { data, error } = await fetchTaskList();
    if (!error && data) {
      tasks.value = data;
    }
  } finally {
    loading.value = false;
  }
}

function handleCreateTask() {
  router.push('/evaluation/task/create');
}

async function handleStartTask(id: string) {
  const { error } = await startTask(id);
  if (!error) {
    window.$message?.success('任务已启动');
    subscribe(id);
    onProgress(id, (progress) => {
      const task = tasks.value.find(t => t.id === id);
      if (task) {
        task.progress = progress;
        if (progress > 0 && task.status === 'pending') {
          task.status = 'running';
        }
      }
    });
    onCompleted(id, (status) => {
      const task = tasks.value.find(t => t.id === id);
      if (task) {
        task.status = status;
        task.progress = 100;
      }
      unsubscribe(id);
    });
    await loadTasks();
  }
}

async function handleStopTask(id: string) {
  const { error } = await stopTask(id);
  if (!error) {
    window.$message?.success('任务已停止');
    unsubscribe(id);
    await loadTasks();
  }
}

async function handleDeleteTask(id: string) {
  window.$dialog?.warning({
    title: '确认删除',
    content: '确定要删除该任务吗？',
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: async () => {
      const { error } = await deleteTask(id);
      if (!error) {
        window.$message?.success('删除成功');
        await loadTasks();
      }
    },
  });
}

function handleViewTask(id: string) {
  router.push(`/evaluation/task/${id}`);
}

function formatDate(dateStr: string) {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleString('zh-CN');
}
</script>

<template>
  <div class="h-full flex flex-col gap-4">
    <!-- Header -->
    <NCard title="评测任务" :bordered="false">
      <template #header-extra>
        <NSpace>
          <NButton @click="loadTasks">
            <template #icon>
              <icon-mdi-refresh />
            </template>
            刷新
          </NButton>
          <NButton type="primary" @click="handleCreateTask">
            <template #icon>
              <icon-ic-round-plus />
            </template>
            创建任务
          </NButton>
        </NSpace>
      </template>
    </NCard>

    <!-- Task List -->
    <NCard :bordered="false" class="flex-1 overflow-hidden">
      <NDataTable
        :data="tasks"
        :loading="loading"
        :columns="[
          { title: '任务名称', key: 'name', ellipsis: { tooltip: true } },
          { title: '状态', key: 'status', width: 120 },
          { title: '进度', key: 'progress', width: 200 },
          { title: '创建时间', key: 'created_at', width: 180 },
          { title: '操作', key: 'actions', width: 200 },
        ]"
        :row-key="(row: Task) => row.id"
        flex-height
      >
        <template #name="{ row }">
          <div>
            <div class="font-medium">{{ row.name }}</div>
            <div v-if="row.description" class="text-gray-500 text-sm truncate">{{ row.description }}</div>
          </div>
        </template>
        <template #status="{ row }">
          <NTag :type="statusColors[row.status]" size="small">
            {{ statusLabels[row.status] || row.status }}
          </NTag>
        </template>
        <template #progress="{ row }">
          <div v-if="row.status === 'running'" class="flex items-center gap-2">
            <NProgress
              type="line"
              :percentage="row.progress"
              :show-indicator="true"
              :height="8"
              style="width: 120px"
            />
          </div>
          <span v-else-if="row.status === 'completed'" class="text-green-500">100%</span>
          <span v-else class="text-gray-400">-</span>
        </template>
        <template #created_at="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
        <template #actions="{ row }">
          <NSpace>
            <NButton
              v-if="row.status === 'pending' || row.status === 'failed'"
              size="small"
              type="primary"
              @click="handleStartTask(row.id)"
            >
              启动
            </NButton>
            <NButton
              v-if="row.status === 'running'"
              size="small"
              type="warning"
              @click="handleStopTask(row.id)"
            >
              停止
            </NButton>
            <NButton size="small" @click="handleViewTask(row.id)">
              详情
            </NButton>
            <NButton
              v-if="row.status !== 'running'"
              size="small"
              type="error"
              @click="handleDeleteTask(row.id)"
            >
              删除
            </NButton>
          </NSpace>
        </template>
      </NDataTable>
    </NCard>
  </div>
</template>

<style scoped></style>