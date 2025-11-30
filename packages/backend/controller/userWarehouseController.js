// controller/UserWarehouseController.js
const userWarehouseService = require('../service/UserWarehouseService');

// 新增仓库（适配 Koa）
async function createWarehouse(ctx) {
  try {
    const warehouseData = ctx.request.body; // Koa 获取请求体
    const result = await userWarehouseService.createWarehouse(warehouseData);
    ctx.status = 200;
    ctx.body = {
      code: 200,
      msg: '创建仓库成功',
      data: result
    };
  } catch (error) {
    ctx.status = 500;
    ctx.body = {
      code: 500,
      msg: `创建仓库失败：${error.message}`,
      data: null
    };
  }
}

// 根据ID查询仓库（适配 Koa）
async function getWarehouseById(ctx) {
  try {
    const { id } = ctx.params; // Koa 获取路径参数
    const withUser = ctx.query.withUser === 'true'; // Koa 获取查询参数
    const result = await userWarehouseService.getWarehouseById(Number(id), withUser);
    if (!result) {
      ctx.status = 404;
      ctx.body = { code: 404, msg: '仓库不存在', data: null };
      return;
    }
    ctx.status = 200;
    ctx.body = { code: 200, msg: '查询成功', data: result };
  } catch (error) {
    ctx.status = 500;
    ctx.body = { code: 500, msg: `查询失败：${error.message}`, data: null };
  }
}

// 查询用户仓库列表（适配 Koa）
async function getWarehouseListByUserId(ctx) {
  try {
    const { userId } = ctx.query;
    console.log('userId ==>', userId)
    if (!userId) {
      ctx.status = 400;
      ctx.body = { code: 400, msg: '用户ID不能为空', data: null };
      return;
    }
    const result = await userWarehouseService.getWarehouseListByUserId(Number(userId), ctx.query);
    ctx.status = 200;
    ctx.body = { code: 200, msg: '查询列表成功', data: result };
  } catch (error) {
    ctx.status = 500;
    ctx.body = { code: 500, msg: `查询列表失败：${error.message}`, data: null };
  }
}

// 更新仓库（适配 Koa）
async function updateWarehouse(ctx) {
  try {
    const { id } = ctx.params;
    const updateData = ctx.request.body;
    const affectedRows = await userWarehouseService.updateWarehouse(Number(id), updateData);
    if (affectedRows === 0) {
      ctx.status = 404;
      ctx.body = { code: 404, msg: '仓库不存在或未修改', data: null };
      return;
    }
    ctx.status = 200;
    ctx.body = { code: 200, msg: '更新成功', data: { affectedRows } };
  } catch (error) {
    ctx.status = 500;
    ctx.body = { code: 500, msg: `更新失败：${error.message}`, data: null };
  }
}

// 删除仓库（适配 Koa）
async function deleteWarehouse(ctx) {
  try {
    const { id } = ctx.params;
    const affectedRows = await userWarehouseService.deleteWarehouse(Number(id));
    if (affectedRows === 0) {
      ctx.status = 404;
      ctx.body = { code: 404, msg: '仓库不存在', data: null };
      return;
    }
    ctx.status = 200;
    ctx.body = { code: 200, msg: '删除成功', data: { affectedRows } };
  } catch (error) {
    ctx.status = 500;
    ctx.body = { code: 500, msg: `删除失败：${error.message}`, data: null };
  }
}

module.exports = {
  createWarehouse,
  getWarehouseById,
  getWarehouseListByUserId,
  updateWarehouse,
  deleteWarehouse
};