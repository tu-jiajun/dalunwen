import apiClient from '../apiClient';

export const ctApi = {
  CTAll({page, size}: { page: number; size: number }) {
    return apiClient.get(`api/ct/paged?tableType=all&page=${page}&pageSize=${size}`);
  },
  CTUSA({page, size}: { page: number; size: number }) {
    return apiClient.get(`api/ct/paged?tableType=usa&page=${page}&pageSize=${size}`);
  },
  CTChina({page, size}: { page: number; size: number }) {
    return apiClient.get(`api/ct/paged?tableType=china&page=${page}&pageSize=${size}`);
  },
};