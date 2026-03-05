/** OpenCompass Evaluation API Service */

import { request } from '@/service/request';

const API_PREFIX = '/api/v1';

// ==================== Model APIs ====================

/** Get model list */
export function fetchModelList(params?: { skip?: number; limit?: number; type?: string }) {
  return request<Api.Evaluation.ModelList>({
    url: `${API_PREFIX}/models`,
    method: 'get',
    params
  });
}

/** Get model by ID */
export function fetchModel(id: string) {
  return request<Api.Evaluation.Model>({
    url: `${API_PREFIX}/models/${id}`,
    method: 'get'
  });
}

/** Create model */
export function createModel(data: Api.Evaluation.ModelCreate) {
  return request<Api.Evaluation.Model>({
    url: `${API_PREFIX}/models`,
    method: 'post',
    data
  });
}

/** Update model */
export function updateModel(id: string, data: Partial<Api.Evaluation.ModelCreate>) {
  return request<Api.Evaluation.Model>({
    url: `${API_PREFIX}/models/${id}`,
    method: 'put',
    data
  });
}

/** Delete model */
export function deleteModel(id: string) {
  return request<void>({
    url: `${API_PREFIX}/models/${id}`,
    method: 'delete'
  });
}

// ==================== Dataset APIs ====================

/** Get dataset list */
export function fetchDatasetList(params?: { skip?: number; limit?: number; type?: string; category?: string }) {
  return request<Api.Evaluation.DatasetList>({
    url: `${API_PREFIX}/datasets`,
    method: 'get',
    params
  });
}

/** Get builtin datasets */
export function fetchBuiltinDatasets() {
  return request<Api.Evaluation.DatasetList>({
    url: `${API_PREFIX}/datasets/builtin`,
    method: 'get'
  });
}

/** Get dataset by ID */
export function fetchDataset(id: string) {
  return request<Api.Evaluation.Dataset>({
    url: `${API_PREFIX}/datasets/${id}`,
    method: 'get'
  });
}

/** Create dataset */
export function createDataset(data: Api.Evaluation.DatasetCreate) {
  return request<Api.Evaluation.Dataset>({
    url: `${API_PREFIX}/datasets`,
    method: 'post',
    data
  });
}

/** Delete dataset */
export function deleteDataset(id: string) {
  return request<void>({
    url: `${API_PREFIX}/datasets/${id}`,
    method: 'delete'
  });
}

// ==================== Task APIs ====================

/** Get task list */
export function fetchTaskList(params?: { skip?: number; limit?: number; status?: string }) {
  return request<Api.Evaluation.TaskList>({
    url: `${API_PREFIX}/tasks`,
    method: 'get',
    params
  });
}

/** Get task by ID */
export function fetchTask(id: string) {
  return request<Api.Evaluation.Task>({
    url: `${API_PREFIX}/tasks/${id}`,
    method: 'get'
  });
}

/** Create task */
export function createTask(data: Api.Evaluation.TaskCreate) {
  return request<Api.Evaluation.Task>({
    url: `${API_PREFIX}/tasks`,
    method: 'post',
    data
  });
}

/** Start task */
export function startTask(id: string) {
  return request<Api.Evaluation.Task>({
    url: `${API_PREFIX}/tasks/${id}/start`,
    method: 'post'
  });
}

/** Stop task */
export function stopTask(id: string) {
  return request<Api.Evaluation.Task>({
    url: `${API_PREFIX}/tasks/${id}/stop`,
    method: 'post'
  });
}

/** Get task logs */
export function fetchTaskLogs(id: string, params?: { offset?: number; limit?: number }) {
  return request<Api.Evaluation.TaskLogs>({
    url: `${API_PREFIX}/tasks/${id}/logs`,
    method: 'get',
    params
  });
}

/** Delete task */
export function deleteTask(id: string) {
  return request<void>({
    url: `${API_PREFIX}/tasks/${id}`,
    method: 'delete'
  });
}

// ==================== Result APIs ====================

/** Get task results */
export function fetchTaskResults(taskId: string) {
  return request<Api.Evaluation.ResultList>({
    url: `${API_PREFIX}/results/task/${taskId}`,
    method: 'get'
  });
}

/** Get result by ID */
export function fetchResult(id: string) {
  return request<Api.Evaluation.Result>({
    url: `${API_PREFIX}/results/${id}`,
    method: 'get'
  });
}

/** Get result details */
export function fetchResultDetails(id: string, params?: { skip?: number; limit?: number }) {
  return request<Api.Evaluation.ResultDetails>({
    url: `${API_PREFIX}/results/${id}/details`,
    method: 'get',
    params
  });
}

/** Get leaderboard */
export function fetchLeaderboard(params?: { dataset?: string; limit?: number }) {
  return request<Api.Evaluation.LeaderboardEntry[]>({
    url: `${API_PREFIX}/results/leaderboard`,
    method: 'get',
    params
  });
}