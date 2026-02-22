import apiClient from '../apiClient';

export const aiApi = {
  generateProtocol(messages: { role: string; content: string }[]) {
    return apiClient.post('/api/ai/generate', { messages });
  },
  matchPatient(data: { age: number; gender: string; condition: string; isRecruiting: boolean; registry: 'usa' | 'china' }) {
    return apiClient.post('/api/match/patient', data, { timeout: 30 * 60 * 1000 });
  },
  matchTrial(data: { registry: 'usa' | 'china'; trialId?: string; trialText?: string; isRecruiting: boolean }) {
    return apiClient.post('/api/match/trial', data, { timeout: 30 * 60 * 1000 });
  }
};
