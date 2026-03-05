# WebSocket Hook 开发文档

> 最后更新: 2026-03-05

## 概述

WebSocket Hook 用于实时接收任务进度和日志更新。

## 文件位置

```
src/hooks/business/useEvaluationWebSocket.ts
```

## 实现代码

```typescript
import { ref, onUnmounted } from 'vue';

interface WebSocketCallbacks {
  onProgress?: (progress: number, data?: any) => void;
  onLog?: (level: string, message: string) => void;
  onStatus?: (status: string) => void;
  onError?: (error: Event) => void;
}

export function useEvaluationWebSocket() {
  const socket = ref<WebSocket | null>(null);
  const connected = ref(false);
  const subscriptions = new Map<string, WebSocketCallbacks>();

  // 连接 WebSocket
  function connect() {
    if (socket.value?.readyState === WebSocket.OPEN) return;

    const wsUrl = `${location.protocol === 'https:' ? 'wss:' : 'ws:'}//${location.host}/api/v1/ws`;
    socket.value = new WebSocket(wsUrl);

    socket.value.onopen = () => {
      connected.value = true;
      console.log('WebSocket connected');
    };

    socket.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleMessage(data);
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e);
      }
    };

    socket.value.onclose = () => {
      connected.value = false;
      console.log('WebSocket disconnected');
      // 自动重连
      setTimeout(connect, 3000);
    };

    socket.value.onerror = (error) => {
      console.error('WebSocket error:', error);
      subscriptions.forEach(cb => cb.onError?.(error));
    };
  }

  // 处理消息
  function handleMessage(data: { type: string; taskId: string; [key: string]: any }) {
    const callbacks = subscriptions.get(data.taskId);
    if (!callbacks) return;

    switch (data.type) {
      case 'progress':
        callbacks.onProgress?.(data.progress, data);
        break;
      case 'log':
        callbacks.onLog?.(data.level, data.message);
        break;
      case 'status':
        callbacks.onStatus?.(data.status);
        break;
    }
  }

  // 订阅任务
  function subscribe(taskId: string, callbacks: WebSocketCallbacks) {
    subscriptions.set(taskId, callbacks);

    if (!connected.value) {
      connect();
    }

    // 发送订阅消息
    if (socket.value?.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify({
        action: 'subscribe',
        taskId
      }));
    }
  }

  // 取消订阅
  function unsubscribe(taskId: string) {
    subscriptions.delete(taskId);

    if (socket.value?.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify({
        action: 'unsubscribe',
        taskId
      }));
    }
  }

  // 断开连接
  function disconnect() {
    socket.value?.close();
    socket.value = null;
  }

  // 组件卸载时自动清理
  onUnmounted(() => {
    disconnect();
  });

  return {
    connected,
    connect,
    subscribe,
    unsubscribe,
    disconnect
  };
}
```

## 使用示例

```vue
<template>
  <div>
    <NProgress :percentage="progress" />
    <div v-for="log in logs" :key="log.id" :class="log.level">
      {{ log.message }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useEvaluationWebSocket } from '@/hooks/business/useEvaluationWebSocket';

const props = defineProps<{ taskId: string }>();

const progress = ref(0);
const logs = ref<Array<{ id: number; level: string; message: string }>>([]);

const { subscribe, unsubscribe } = useEvaluationWebSocket();

onMounted(() => {
  subscribe(props.taskId, {
    onProgress: (p) => {
      progress.value = p;
    },
    onLog: (level, message) => {
      logs.value.push({
        id: Date.now(),
        level,
        message
      });
    },
    onStatus: (status) => {
      console.log('Task status:', status);
    },
    onError: (error) => {
      console.error('WebSocket error:', error);
    }
  });
});

onUnmounted(() => {
  unsubscribe(props.taskId);
});
</script>
```

## 消息类型

| 类型 | 字段 | 说明 |
|------|------|------|
| progress | taskId, progress, message | 进度更新 |
| log | taskId, level, message | 日志消息 |
| status | taskId, status | 状态变更 |

## 注意事项

1. **自动重连**：连接断开后 3 秒自动重连
2. **组件卸载清理**：`onUnmounted` 自动断开连接
3. **心跳机制**：客户端发送 `ping`，服务端响应 `pong`

---

## 变更记录

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化 WebSocket Hook 文档 |