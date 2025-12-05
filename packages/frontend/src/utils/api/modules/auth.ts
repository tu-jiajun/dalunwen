import apiClient from '../apiClient';

export const authApi = {
  login(username: string, password: string) {
    return apiClient.post('/api/users/login', { username, password });
  },
  register(username: string, password: string) {
    return apiClient.post('/api/users/register', { username, password });
  },
};