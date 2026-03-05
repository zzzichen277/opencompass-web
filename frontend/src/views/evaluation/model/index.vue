<script setup lang="ts">
import { ref, onMounted } from 'vue';

defineOptions({ name: 'ModelManage' });

const models = ref([
  { id: '1', name: 'Qwen2.5-72B-Instruct', type: 'huggingface', path: 'Qwen/Qwen2.5-72B-Instruct', createdAt: '2026-03-01' },
  { id: '2', name: 'InternLM3-8B-Instruct', type: 'huggingface', path: 'internlm/internlm3-8b-instruct', createdAt: '2026-03-02' },
  { id: '3', name: 'GPT-4o', type: 'api', apiConfig: { baseUrl: 'https://api.openai.com/v1' }, createdAt: '2026-03-03' },
]);

const showModal = ref(false);
const editingModel = ref<any>(null);
const loading = ref(false);

function handleAddModel() {
  editingModel.value = null;
  showModal.value = true;
}

function handleEditModel(model: any) {
  editingModel.value = { ...model };
  showModal.value = true;
}

function handleDeleteModel(id: string) {
  window.$dialog?.warning({
    title: '确认删除',
    content: '确定要删除该模型配置吗？',
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: () => {
      models.value = models.value.filter(m => m.id !== id);
      window.$message?.success('删除成功');
    },
  });
}

function handleSaveModel() {
  // TODO: Save model to API
  showModal.value = false;
  window.$message?.success('保存成功');
}
</script>

<template>
  <div class="h-full flex flex-col gap-4">
    <!-- Header -->
    <NCard title="模型管理" :bordered="false">
      <template #header-extra>
        <NButton type="primary" @click="handleAddModel">
          <template #icon>
            <icon-ic-round-plus />
          </template>
          添加模型
        </NButton>
      </template>
    </NCard>

    <!-- Model List -->
    <NCard :bordered="false" class="flex-1 overflow-hidden">
      <NDataTable
        :data="models"
        :loading="loading"
        :columns="[
          { title: '模型名称', key: 'name' },
          { title: '类型', key: 'type' },
          { title: '路径/配置', key: 'path' },
          { title: '添加时间', key: 'createdAt' },
          { title: '操作', key: 'actions' },
        ]"
        :row-key="(row: any) => row.id"
        flex-height
      >
        <template #type="{ row }">
          <NTag :type="row.type === 'huggingface' ? 'info' : 'warning'" size="small">
            {{ row.type }}
          </NTag>
        </template>
        <template #path="{ row }">
          <span class="text-gray-600">{{ row.path || row.apiConfig?.baseUrl || '-' }}</span>
        </template>
        <template #actions="{ row }">
          <NSpace>
            <NButton size="small" @click="handleEditModel(row)">编辑</NButton>
            <NButton size="small" type="error" @click="handleDeleteModel(row.id)">删除</NButton>
          </NSpace>
        </template>
      </NDataTable>
    </NCard>

    <!-- Add/Edit Modal -->
    <NModal v-model:show="showModal" preset="card" title="添加模型" style="width: 600px">
      <NForm label-placement="left" label-width="100">
        <NFormItem label="模型名称" required>
          <NInput placeholder="请输入模型名称" />
        </NFormItem>
        <NFormItem label="模型类型" required>
          <NSelect
            :options="[
              { label: 'HuggingFace', value: 'huggingface' },
              { label: 'API', value: 'api' },
            ]"
          />
        </NFormItem>
        <NFormItem label="模型路径">
          <NInput placeholder="HuggingFace 模型路径，如 Qwen/Qwen2.5-72B-Instruct" />
        </NFormItem>
        <NFormItem label="API Base URL">
          <NInput placeholder="API 服务地址" />
        </NFormItem>
        <NFormItem label="API Key">
          <NInput type="password" placeholder="API Key" />
        </NFormItem>
      </NForm>
      <template #footer>
        <NSpace justify="end">
          <NButton @click="showModal = false">取消</NButton>
          <NButton type="primary" @click="handleSaveModel">保存</NButton>
        </NSpace>
      </template>
    </NModal>
  </div>
</template>

<style scoped></style>