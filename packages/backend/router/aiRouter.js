const Router = require('koa-router');
const aiController = require('../controller/aiController');

const router = new Router({ prefix: '/api/ai' });

// Generate clinical trial protocol
router.post('/generate', aiController.generateProtocol);

module.exports = router;
