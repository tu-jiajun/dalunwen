// routes/userWarehouseRoutes.js
const Router = require('koa-router');
const userWarehouseController = require('../controller/userWarehouseController');

const router = new Router({ prefix: '/api/warehouse' });

router.post('/', userWarehouseController.createWarehouse);
router.get('/list', userWarehouseController.getWarehouseListByUserId);
router.get('/:id', userWarehouseController.getWarehouseById);
router.put('/:id', userWarehouseController.updateWarehouse);
router.delete('/:id', userWarehouseController.deleteWarehouse);

module.exports = router;
