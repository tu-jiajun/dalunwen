const Router = require('koa-router');
const CTCtrl = require('../controller/ctController');

// 路由前缀：/api/ct
const router = new Router({ prefix: '/api/ct' });

/**
 * 分页查询接口：GET /api/ct/paged
 */
router.get('/paged', CTCtrl.getPagedClinicalTrial);

module.exports = router;
