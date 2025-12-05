import { authApi } from './modules/auth';
import { ctApi } from './modules/ct';
import { warehouseApi } from './modules/warehouse';

const api = {
  ...authApi,
  ...ctApi,
  ...warehouseApi
};

export { authApi, ctApi, warehouseApi };

export default api;