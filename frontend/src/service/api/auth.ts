import { localStg } from '@/utils/storage';
import { request } from '../request';

const API_PREFIX = '/api/v1';

/**
 * Login
 *
 * @param userName User name
 * @param password Password
 */
export function fetchLogin(userName: string, password: string) {
  return request<Api.Auth.LoginToken>({
    url: `${API_PREFIX}/auth/login`,
    method: 'post',
    data: {
      userName,
      password
    }
  });
}

/** Get user info */
export function fetchGetUserInfo() {
  // 从 localStg 获取 token（会自动解析 JSON）
  const token = localStg.get('token');
  return request<Api.Auth.UserInfo>({
    url: `${API_PREFIX}/auth/getUserInfo`,
    method: 'get',
    params: { token }
  });
}

/**
 * Refresh token
 *
 * @param refreshToken Refresh token
 */
export function fetchRefreshToken(refreshToken: string) {
  return request<Api.Auth.LoginToken>({
    url: `${API_PREFIX}/auth/refreshToken`,
    method: 'post',
    data: {
      refreshToken
    }
  });
}

/**
 * return custom backend error
 *
 * @param code error code
 * @param msg error message
 */
export function fetchCustomBackendError(code: string, msg: string) {
  return request({ url: `${API_PREFIX}/auth/error`, params: { code, msg } });
}
