// service/ClinicalTrialWarehouseService.js
const ClinicalTrialWarehouse = require('../model/ClinicalTrialWarehouse');
const ClinicalUSA = require('../model/ClinicalTrialUsa');
const ClinicalChina = require('../model/ClinicalTrialChina');
const UserWarehouse = require('../model/userWarehouse');

/**
 * 服务层：将临床试验添加到仓库
 * @param {Object} trialData 临床试验数据
 * @param {Number} warehouseId 仓库ID
 * @returns {Promise<Object>} 添加的关联信息
 */
async function addTrialToWarehouse(trialData, warehouseId) {
  try {
    // 校验仓库是否存在
    const warehouse = await UserWarehouse.findByPk(warehouseId);
    if (!warehouse) {
      throw new Error('指定的仓库不存在');
    }

    // 校验临床试验数据
    if (!trialData.nct_number && !trialData.reg_number) {
      throw new Error('NCT编号或备案号至少需要提供一个');
    }

    // 检查是否已经存在相同的关联记录
    const existingRecord = await ClinicalTrialWarehouse.findOne({
      where: {
        warehouse_id: warehouseId,
        [trialData.nct_number ? 'nct_number' : 'reg_number']: 
          trialData.nct_number || trialData.reg_number
      }
    });

    if (existingRecord) {
      throw new Error('该临床试验已在指定仓库中');
    }

    // 创建关联记录
    const associationData = {
      warehouse_id: warehouseId,
      nct_number: trialData.nct_number || null,
      reg_number: trialData.reg_number || null,
      dynamic_extra_fields: trialData.dynamic_extra_fields || null
    };

    const association = await ClinicalTrialWarehouse.create(associationData);
    return association.toJSON();
  } catch (error) {
    console.error('【ClinicalTrialWarehouseService】添加临床试验到仓库失败：', error.message);
    throw error;
  }
}

/**
 * 服务层：从仓库中移除临床试验
 * @param {Number} warehouseId 仓库ID
 * @param {String} trialIdentifier NCT编号或备案号
 * @returns {Promise<Number>} 删除的记录数
 */
async function removeTrialFromWarehouse(warehouseId, trialIdentifier) {
  try {
    // 构建查询条件
    const whereCondition = {
      warehouse_id: warehouseId
    };

    // 根据标识符类型设置查询条件
    if (trialIdentifier.startsWith('NCT')) {
      whereCondition.nct_number = trialIdentifier;
    } else {
      whereCondition.reg_number = trialIdentifier;
    }

    // 删除关联记录
    const deletedRows = await ClinicalTrialWarehouse.destroy({
      where: whereCondition
    });

    return deletedRows;
  } catch (error) {
    console.error('【ClinicalTrialWarehouseService】从仓库移除临床试验失败：', error.message);
    throw error;
  }
}

/**
 * 服务层：获取仓库中的临床试验列表
 * @param {Number} warehouseId 仓库ID
 * @param {Object} query 分页参数
 * @returns {Promise<Object>} 临床试验列表+总数
 */
async function getTrialsInWarehouse(warehouseId, query = {}) {
  try {
    const { pageNum = 1, pageSize = 10 } = query;
    const offset = (pageNum - 1) * pageSize;

    // 查询关联记录，并关联临床试验详情
    const { count, rows } = await ClinicalTrialWarehouse.findAndCountAll({
      where: { warehouse_id: warehouseId },
      limit: pageSize,
      offset,
      order: [['created_at', 'DESC']],
      include: [
        {
          model: ClinicalUSA,
          as: 'clinicalUSA',
          required: false
        },
        {
          model: ClinicalChina,
          as: 'clinicalChina',
          required: false
        }
      ],
      distinct: true
    });

    return {
      list: rows,
      total: count,
      pageNum,
      pageSize
    };
  } catch (error) {
    console.error('【ClinicalTrialWarehouseService】查询仓库临床试验列表失败：', error.message);
    throw error;
  }
}

/**
 * 服务层：更新临床试验关联记录
 * @param {Number} id 记录ID
 * @param {Object} updateData 更新数据
 * @returns {Promise<Object>} 更新后的记录
 */
async function updateTrialInWarehouse(id, updateData) {
  try {
    // 查找要更新的记录
    const record = await ClinicalTrialWarehouse.findByPk(id);
    if (!record) {
      throw new Error('未找到指定的记录');
    }

    // 更新记录
    const updatedRecord = await record.update(updateData);
    return updatedRecord.toJSON();
  } catch (error) {
    console.error('【ClinicalTrialWarehouseService】更新临床试验关联记录失败：', error.message);
    throw error;
  }
}

/**
 * 服务层：根据ID获取临床试验关联记录详情
 * @param {Number} id 记录ID
 * @returns {Promise<Object>} 记录详情
 */
async function getTrialWarehouseById(id) {
  try {
    // 查找记录并关联临床试验详情
    const record = await ClinicalTrialWarehouse.findByPk(id, {
      include: [
        {
          model: ClinicalUSA,
          as: 'clinicalUSA',
          required: false
        },
        {
          model: ClinicalChina,
          as: 'clinicalChina',
          required: false
        }
      ]
    });
    
    return record ? record.toJSON() : null;
  } catch (error) {
    console.error('【ClinicalTrialWarehouseService】查询临床试验关联记录详情失败：', error.message);
    throw error;
  }
}

/**
 * 服务层：分页查询所有临床试验关联记录
 * @param {Object} query 查询参数
 * @returns {Promise<Object>} 记录列表+总数
 */
async function getAllTrialWarehouses(query = {}) {
  try {
    const { pageNum = 1, pageSize = 10, warehouseId } = query;
    const offset = (pageNum - 1) * pageSize;
    
    // 构建查询条件
    const whereCondition = {};
    if (warehouseId) {
      whereCondition.warehouse_id = warehouseId;
    }

    // 查询记录
    const { count, rows } = await ClinicalTrialWarehouse.findAndCountAll({
      where: whereCondition,
      limit: pageSize,
      offset,
      order: [['created_at', 'DESC']],
      include: [
        {
          model: ClinicalUSA,
          as: 'clinicalUSA',
          required: false
        },
        {
          model: ClinicalChina,
          as: 'clinicalChina',
          required: false
        }
      ],
      distinct: true
    });

    return {
      list: rows,
      total: count,
      pageNum,
      pageSize
    };
  } catch (error) {
    console.error('【ClinicalTrialWarehouseService】查询所有临床试验关联记录失败：', error.message);
    throw error;
  }
}

/**
 * 服务层：删除临床试验关联记录
 * @param {Number} id 记录ID
 * @returns {Promise<Number>} 删除的记录数
 */
async function deleteTrialWarehouse(id) {
  try {
    // 删除记录
    const deletedRows = await ClinicalTrialWarehouse.destroy({
      where: { id }
    });
    
    return deletedRows;
  } catch (error) {
    console.error('【ClinicalTrialWarehouseService】删除临床试验关联记录失败：', error.message);
    throw error;
  }
}

// 导出所有方法
module.exports = {
  addTrialToWarehouse,
  removeTrialFromWarehouse,
  getTrialsInWarehouse,
  updateTrialInWarehouse,
  getTrialWarehouseById,
  getAllTrialWarehouses,
  deleteTrialWarehouse
};