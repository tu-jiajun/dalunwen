import { authApi } from './modules/auth';
import { ctApi } from './modules/ct';
import { warehouseApi } from './modules/warehouse';
import { aiApi } from './modules/ai';

const api = {
  ...authApi,
  ...ctApi,
  ...warehouseApi,
  ...aiApi
};

export { authApi, ctApi, warehouseApi, aiApi };

export default api;