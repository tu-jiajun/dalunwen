// service/UserWarehouseService.js
const UserWarehouse = require('../model/userWarehouse');
const { Op } = require('sequelize'); // Sequelize操作符，用于条件查询

/**
 * 服务层：新增用户仓库
 * @param {Object} warehouseData 仓库数据（user_id, warehouse_name）
 * @returns {Promise<Object>} 新增的仓库信息
 */
async function createWarehouse(warehouseData) {
  try {
    // 校验必填参数
    if (!warehouseData.user_id || !warehouseData.warehouse_name) {
      throw new Error('用户ID和仓库名称不能为空');
    }
    // 创建仓库（Sequelize的create方法）
    const warehouse = await UserWarehouse.create({
      user_id: warehouseData.user_id,
      warehouse_name: warehouseData.warehouse_name,
      // createdAt/updatedAt由Sequelize自动生成
    });
    return warehouse.toJSON(); // 转为JSON格式返回
  } catch (error) {
    console.error('【UserWarehouseService】创建仓库失败：', error.message);
    throw error; // 抛出错误，由Controller层统一处理
  }
}

/**
 * 服务层：根据ID查询仓库
 * @param {Number} id 仓库ID
 * @param {Boolean} withUser 是否关联查询用户信息
 * @returns {Promise<Object|null>} 仓库信息
 */
async function getWarehouseById(id, withUser = false) {
  try {
    const options = {
      where: { id },
      raw: true // 返回纯JSON，而非Sequelize实例
    };
    // 关联查询用户信息（可选）
    if (withUser) {
      const User = require('../model/User');
      options.include = [{
        model: User,
        as: 'user', // 对应模型中定义的关联别名
        attributes: ['id', 'username'] // 仅返回用户ID和用户名，避免敏感信息
      }];
    }
    const warehouse = await UserWarehouse.findOne(options);
    return warehouse;
  } catch (error) {
    console.error('【UserWarehouseService】查询仓库失败：', error.message);
    throw error;
  }
}

/**
 * 服务层：根据用户ID查询仓库列表
 * @param {Number} userId 用户ID
 * @param {Object} query 分页/筛选参数（pageNum, pageSize, warehouseName）
 * @returns {Promise<Object>} 列表+总数
 */
async function getWarehouseListByUserId(userId, query = {}) {
  try {
    const { pageNum = 1, pageSize = 10, warehouseName = '' } = query;
    const offset = (pageNum - 1) * pageSize; // 分页偏移量

    // 构建查询条件
    const where = { user_id: userId };
    if (warehouseName) {
      where.warehouse_name = { [Op.like]: `%${warehouseName}%` }; // 模糊查询
    }

    // 分页查询
    const { count, rows } = await UserWarehouse.findAndCountAll({
      where,
      limit: pageSize,
      offset,
      order: [['created_at', 'DESC']], // 按创建时间降序
      raw: true
    });

    return {
      list: rows,
      total: count,
      pageNum,
      pageSize
    };
  } catch (error) {
    console.error('【UserWarehouseService】查询仓库列表失败：', error.message);
    throw error;
  }
}

/**
 * 服务层：更新仓库信息
 * @param {Number} id 仓库ID
 * @param {Object} updateData 要更新的字段（warehouse_name）
 * @returns {Promise<Number>} 影响的行数
 */
async function updateWarehouse(id, updateData) {
  try {
    if (!updateData.warehouse_name) {
      throw new Error('仓库名称不能为空');
    }
    // Sequelize的update方法，返回[影响行数]
    const [affectedRows] = await UserWarehouse.update(
      { warehouse_name: updateData.warehouse_name, updated_at: new Date() },
      { where: { id } }
    );
    return affectedRows;
  } catch (error) {
    console.error('【UserWarehouseService】更新仓库失败：', error.message);
    throw error;
  }
}

/**
 * 服务层：删除仓库（物理删除，如需软删除可修改where条件）
 * @param {Number} id 仓库ID
 * @returns {Promise<Number>} 影响的行数
 */
async function deleteWarehouse(id) {
  try {
    const affectedRows = await UserWarehouse.destroy({ where: { id } });
    return affectedRows;
  } catch (error) {
    console.error('【UserWarehouseService】删除仓库失败：', error.message);
    throw error;
  }
}

// 导出所有方法
module.exports = {
  createWarehouse,
  getWarehouseById,
  getWarehouseListByUserId,
  updateWarehouse,
  deleteWarehouse
};