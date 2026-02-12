import apiClient from '../apiClient';

export const warehouseApi = {
  getWarehouseByUserId(userId: string) {
    return apiClient.get(`api/warehouse/list?userId=${userId}`);
  },
  createWarehouse(data: { user_id: number; warehouse_name: string }) {
    return apiClient.post(`api/warehouse`, data);
  },
  updateWarehouse(id: number, data: { warehouse_name: string }) {
    return apiClient.put(`api/warehouse/${id}`, data);
  },
  deleteWarehouse(rowId: number) {
    return apiClient.delete(`api/warehouse/${rowId}`);
  },
  addTrialToWarehouse(warehouseId: number, trialData: any) {
    return apiClient.post(`api/warehouse/${warehouseId}/trials`, trialData);
  },
};