// controller/ClinicalTrialWarehouseController.js
const clinicalTrialWarehouseService = require('../service/clinicalTrialWarehouseService');

/**
 * 控制器：将临床试验添加到仓库
 * @param {Object} ctx Koa上下文
 */
async function addTrialToWarehouse(ctx) {
  try {
    const { warehouseId } = ctx.params;
    const trialData = ctx.request.body;

    // 参数校验
    if (!warehouseId) {
      ctx.status = 400;
      ctx.body = {
        code: 400,
        msg: '仓库ID不能为空',
        data: null
      };
      return;
    }

    const result = await clinicalTrialWarehouseService.addTrialToWarehouse(trialData, Number(warehouseId));
    
    ctx.status = 200;
    ctx.body = {
      code: 200,
      msg: '添加成功',
      data: result
    };
  } catch (error) {
    ctx.status = 500;
    ctx.body = {
      code: 500,
      msg: `添加失败：${error.message}`,
      data: null
    };
  }
}

/**
 * 控制器：从仓库中移除临床试验
 * @param {Object} ctx Koa上下文
 */
async function removeTrialFromWarehouse(ctx) {
  try {
    const { warehouseId } = ctx.params;
    const { trialIdentifier } = ctx.query;

    // 参数校验
    if (!warehouseId) {
      ctx.status = 400;
      ctx.body = {
        code: 400,
        msg: '仓库ID不能为空',
        data: null
      };
      return;
    }

    if (!trialIdentifier) {
      ctx.status = 400;
      ctx.body = {
        code: 400,
        msg: '试验标识符不能为空',
        data: null
      };
      return;
    }

    const deletedRows = await clinicalTrialWarehouseService.removeTrialFromWarehouse(Number(warehouseId), trialIdentifier);
    
    if (deletedRows === 0) {
      ctx.status = 404;
      ctx.body = {
        code: 404,
        msg: '未找到对应的试验记录',
        data: null
      };
      return;
    }

    ctx.status = 200;
    ctx.body = {
      code: 200,
      msg: '移除成功',
      data: { deletedRows }
    };
  } catch (error) {
    ctx.status = 500;
    ctx.body = {
      code: 500,
      msg: `移除失败：${error.message}`,
      data: null
    };
  }
}

/**
 * 控制器：获取仓库中的临床试验列表
 * @param {Object} ctx Koa上下文
 */
async function getTrialsInWarehouse(ctx) {
  try {
    const { warehouseId } = ctx.params;
    const { pageNum, pageSize } = ctx.query;

    // 参数校验
    if (!warehouseId) {
      ctx.status = 400;
      ctx.body = {
        code: 400,
        msg: '仓库ID不能为空',
        data: null
      };
      return;
    }

    const query = {};
    if (pageNum) query.pageNum = parseInt(pageNum);
    if (pageSize) query.pageSize = parseInt(pageSize);

    const result = await clinicalTrialWarehouseService.getTrialsInWarehouse(Number(warehouseId), query);
    
    ctx.status = 200;
    ctx.body = {
      code: 200,
      msg: '查询成功',
      data: result
    };
  } catch (error) {
    ctx.status = 500;
    ctx.body = {
      code: 500,
      msg: `查询失败：${error.message}`,
      data: null
    };
  }
}

/**
 * 控制器：更新临床试验关联记录
 * @param {Object} ctx Koa上下文
 */
async function updateTrialInWarehouse(ctx) {
  try {
    const { id } = ctx.params;
    const updateData = ctx.request.body;

    // 参数校验
    if (!id) {
      ctx.status = 400;
      ctx.body = {
        code: 400,
        msg: '记录ID不能为空',
        data: null
      };
      return;
    }

    const result = await clinicalTrialWarehouseService.updateTrialInWarehouse(Number(id), updateData);
    
    ctx.status = 200;
    ctx.body = {
      code: 200,
      msg: '更新成功',
      data: result
    };
  } catch (error) {
    ctx.status = 500;
    ctx.body = {
      code: 500,
      msg: `更新失败：${error.message}`,
      data: null
    };
  }
}

/**
 * 控制器：根据ID获取临床试验关联记录详情
 * @param {Object} ctx Koa上下文
 */
async function getTrialWarehouseById(ctx) {
  try {
    const { id } = ctx.params;

    // 参数校验
    if (!id) {
      ctx.status = 400;
      ctx.body = {
        code: 400,
        msg: '记录ID不能为空',
        data: null
      };
      return;
    }

    const result = await clinicalTrialWarehouseService.getTrialWarehouseById(Number(id));
    
    if (!result) {
      ctx.status = 404;
      ctx.body = {
        code: 404,
        msg: '未找到对应的记录',
        data: null
      };
      return;
    }

    ctx.status = 200;
    ctx.body = {
      code: 200,
      msg: '查询成功',
      data: result
    };
  } catch (error) {
    ctx.status = 500;
    ctx.body = {
      code: 500,
      msg: `查询失败：${error.message}`,
      data: null
    };
  }
}

/**
 * 控制器：分页查询所有临床试验关联记录
 * @param {Object} ctx Koa上下文
 */
async function getAllTrialWarehouses(ctx) {
  try {
    const { pageNum, pageSize, warehouseId } = ctx.query;

    const query = {};
    if (pageNum) query.pageNum = parseInt(pageNum);
    if (pageSize) query.pageSize = parseInt(pageSize);
    if (warehouseId) query.warehouseId = parseInt(warehouseId);

    const result = await clinicalTrialWarehouseService.getAllTrialWarehouses(query);
    
    ctx.status = 200;
    ctx.body = {
      code: 200,
      msg: '查询成功',
      data: result
    };
  } catch (error) {
    ctx.status = 500;
    ctx.body = {
      code: 500,
      msg: `查询失败：${error.message}`,
      data: null
    };
  }
}

/**
 * 控制器：删除临床试验关联记录
 * @param {Object} ctx Koa上下文
 */
async function deleteTrialWarehouse(ctx) {
  try {
    const { id } = ctx.params;

    // 参数校验
    if (!id) {
      ctx.status = 400;
      ctx.body = {
        code: 400,
        msg: '记录ID不能为空',
        data: null
      };
      return;
    }

    const deletedRows = await clinicalTrialWarehouseService.deleteTrialWarehouse(Number(id));
    
    if (deletedRows === 0) {
      ctx.status = 404;
      ctx.body = {
        code: 404,
        msg: '未找到对应的记录',
        data: null
      };
      return;
    }

    ctx.status = 200;
    ctx.body = {
      code: 200,
      msg: '删除成功',
      data: { deletedRows }
    };
  } catch (error) {
    ctx.status = 500;
    ctx.body = {
      code: 500,
      msg: `删除失败：${error.message}`,
      data: null
    };
  }
}

// 导出所有控制器方法
module.exports = {
  addTrialToWarehouse,
  removeTrialFromWarehouse,
  getTrialsInWarehouse,
  updateTrialInWarehouse,
  getTrialWarehouseById,
  getAllTrialWarehouses,
  deleteTrialWarehouse
};