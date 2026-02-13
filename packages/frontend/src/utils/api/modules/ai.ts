import apiClient from '../apiClient';

export const aiApi = {
  generateProtocol(messages: { role: string; content: string }[]) {
    return apiClient.post('/api/ai/generate', { messages }, { timeout: 60000 });
  },
};
