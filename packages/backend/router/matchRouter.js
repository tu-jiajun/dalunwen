const Router = require('koa-router');
const matchController = require('../controller/matchController');

const router = new Router({ prefix: '/api/match' });

// Patient matching
router.post('/patient', matchController.matchPatient);
router.post('/trial', matchController.matchTrial);

module.exports = router;
