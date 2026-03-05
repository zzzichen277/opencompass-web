/** OpenCompass Evaluation API Types */

declare namespace Api {
  namespace Evaluation {
    // ==================== Model Types ====================

    interface Model {
      id: string;
      name: string;
      type: 'huggingface' | 'api' | 'custom';
      path?: string;
      api_config?: {
        base_url: string;
        api_key?: string;
        model_name: string;
      };
      parameters?: {
        max_length?: number;
        temperature?: number;
        top_p?: number;
      };
      tags?: string[];
      created_at: string;
      updated_at: string;
    }

    type ModelList = Model[];

    interface ModelCreate {
      name: string;
      type: 'huggingface' | 'api' | 'custom';
      path?: string;
      api_config?: Record<string, unknown>;
      parameters?: Record<string, unknown>;
      tags?: string[];
    }

    // ==================== Dataset Types ====================

    interface Dataset {
      id: string;
      name: string;
      type: 'builtin' | 'custom';
      category?: 'qa' | 'math' | 'code' | 'subjective' | 'reasoning';
      description?: string;
      config_path?: string;
      custom_data?: {
        format: 'json' | 'csv';
        path: string;
      };
      metrics?: string[];
      sample_count?: number;
      tags?: string[];
      created_at: string;
    }

    type DatasetList = Dataset[];

    interface DatasetCreate {
      name: string;
      type: 'builtin' | 'custom';
      category?: string;
      description?: string;
      config_path?: string;
      custom_data?: Record<string, unknown>;
      metrics?: string[];
      tags?: string[];
    }

    // ==================== Task Types ====================

    interface TaskConfig {
      models: string[];
      datasets: string[];
      accelerator: 'huggingface' | 'vllm' | 'lmdeploy';
      resources: {
        gpu_count: number;
        max_num_worker: number;
        batch_size?: number;
      };
      eval_config: {
        mode: 'gen' | 'ppl';
        max_out_len?: number;
        batch_size?: number;
      };
    }

    interface Task {
      id: string;
      name: string;
      description?: string;
      config: TaskConfig;
      status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
      progress: number;
      error_message?: string;
      created_at: string;
      started_at?: string;
      completed_at?: string;
    }

    type TaskList = Task[];

    interface TaskCreate {
      name: string;
      description?: string;
      config: TaskConfig;
    }

    interface TaskLogs {
      task_id: string;
      logs: Array<{
        timestamp: string;
        level: string;
        message: string;
      }>;
      offset: number;
      limit: number;
    }

    // ==================== Result Types ====================

    interface Result {
      id: string;
      task_id: string;
      model_id: string;
      dataset_id: string;
      overall_score?: number;
      metrics?: Record<string, number>;
      summary?: {
        correct: number;
        total: number;
        accuracy: number;
      };
      details_path?: string;
      created_at: string;
    }

    type ResultList = Result[];

    interface ResultDetails {
      result_id: string;
      details: Array<{
        question: string;
        answer: string;
        prediction: string;
        score: number;
        reasoning?: string;
      }>;
      skip: number;
      limit: number;
    }

    interface LeaderboardEntry {
      model_id: string;
      model_name: string;
      dataset_id: string;
      dataset_name: string;
      score: number;
      rank: number;
      metrics?: Record<string, number>;
    }

    // ==================== WebSocket Types ====================

    interface WSProgressMessage {
      type: 'progress';
      task_id: string;
      data: {
        status: string;
        progress: number;
        current_dataset?: string;
        completed_samples?: number;
        total_samples?: number;
        eta?: string;
      };
    }

    interface WSLogMessage {
      type: 'log';
      task_id: string;
      data: {
        timestamp: string;
        level: string;
        message: string;
      };
    }

    interface WSCompletedMessage {
      type: 'completed';
      task_id: string;
      data: {
        status: string;
        results: {
          overall_score?: number;
        };
      };
    }

    type WSMessage = WSProgressMessage | WSLogMessage | WSCompletedMessage;
  }
}