// router/ClinicalTrialWarehouseRouter.js
const Router = require('koa-router');
const clinicalTrialWarehouseController = require('../controller/clinicalTrialWarehouseController');

const router = new Router({ prefix: '/api/warehouse' });

// 将临床试验添加到仓库
router.post('/:warehouseId/trials', clinicalTrialWarehouseController.addTrialToWarehouse);

// 从仓库中移除临床试验
router.delete('/:warehouseId/trials', clinicalTrialWarehouseController.removeTrialFromWarehouse);

// 获取仓库中的临床试验列表
router.get('/:warehouseId/trials', clinicalTrialWarehouseController.getTrialsInWarehouse);

// 更新临床试验关联记录
router.put('/trials/:id', clinicalTrialWarehouseController.updateTrialInWarehouse);

// 根据ID获取临床试验关联记录详情
router.get('/trials/:id', clinicalTrialWarehouseController.getTrialWarehouseById);

// 分页查询所有临床试验关联记录
router.get('/trials', clinicalTrialWarehouseController.getAllTrialWarehouses);

// 删除临床试验关联记录
router.delete('/trials/:id', clinicalTrialWarehouseController.deleteTrialWarehouse);

module.exports = router;