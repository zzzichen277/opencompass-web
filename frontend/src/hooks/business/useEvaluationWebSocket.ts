/** WebSocket hook for real-time evaluation updates */

import { ref, onUnmounted } from 'vue';

interface WSMessage {
  type: 'progress' | 'log' | 'completed' | 'subscribed' | 'pong';
  task_id: string;
  timestamp: string;
  data: Record<string, any>;
}

export function useEvaluationWebSocket() {
  const ws = ref<WebSocket | null>(null);
  const connected = ref(false);
  const error = ref<string | null>(null);

  const progressCallbacks = new Map<string, (progress: number, data: any) => void>();
  const logCallbacks = new Map<string, (level: string, message: string) => void>();
  const completedCallbacks = new Map<string, (status: string, results: any) => void>();

  function connect(taskId?: string) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const wsUrl = `${protocol}//${host}/api/v1/ws${taskId ? `?task_id=${taskId}` : ''}`;

    ws.value = new WebSocket(wsUrl);

    ws.value.onopen = () => {
      connected.value = true;
      error.value = null;
    };

    ws.value.onclose = () => {
      connected.value = false;
    };

    ws.value.onerror = (e) => {
      error.value = 'WebSocket connection error';
      console.error('WebSocket error:', e);
    };

    ws.value.onmessage = (event) => {
      try {
        const message: WSMessage = JSON.parse(event.data);
        handleMessage(message);
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e);
      }
    };
  }

  function handleMessage(message: WSMessage) {
    const { type, task_id, data } = message;

    switch (type) {
      case 'progress':
        const progressCallback = progressCallbacks.get(task_id);
        if (progressCallback && typeof data.progress === 'number') {
          progressCallback(data.progress, data);
        }
        break;

      case 'log':
        const logCallback = logCallbacks.get(task_id);
        if (logCallback && data.level && data.message) {
          logCallback(data.level, data.message);
        }
        break;

      case 'completed':
        const completedCallback = completedCallbacks.get(task_id);
        if (completedCallback && data.status) {
          completedCallback(data.status, data.results);
        }
        break;
    }
  }

  function subscribe(taskId: string) {
    if (ws.value && connected.value) {
      ws.value.send(JSON.stringify({ type: 'subscribe', taskId }));
    }
  }

  function unsubscribe(taskId: string) {
    if (ws.value && connected.value) {
      ws.value.send(JSON.stringify({ type: 'unsubscribe', taskId }));
    }
    progressCallbacks.delete(taskId);
    logCallbacks.delete(taskId);
    completedCallbacks.delete(taskId);
  }

  function onProgress(taskId: string, callback: (progress: number, data: any) => void) {
    progressCallbacks.set(taskId, callback);
  }

  function onLog(taskId: string, callback: (level: string, message: string) => void) {
    logCallbacks.set(taskId, callback);
  }

  function onCompleted(taskId: string, callback: (status: string, results: any) => void) {
    completedCallbacks.set(taskId, callback);
  }

  function disconnect() {
    if (ws.value) {
      ws.value.close();
      ws.value = null;
    }
  }

  function ping() {
    if (ws.value && connected.value) {
      ws.value.send(JSON.stringify({ type: 'ping' }));
    }
  }

  onUnmounted(() => {
    disconnect();
  });

  return {
    ws,
    connected,
    error,
    connect,
    disconnect,
    subscribe,
    unsubscribe,
    onProgress,
    onLog,
    onCompleted,
    ping,
  };
}