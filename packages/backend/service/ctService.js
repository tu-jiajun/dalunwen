const ClinicalTrialUsa = require('../model/ClinicalTrialUsa');
const ClinicalTrialChina = require('../model/ClinicalTrialChina');

/**
 * 单表分页查询（复用逻辑，带调试日志）
 * @param {Object} Model - 数据模型（USA/China）
 * @param {Object} params - 查询参数（含当前阶段的页码）
 * @returns {Object} 单表分页结果
 */
async function getSingleTablePaged(Model, params) {
  const { page = 1, pageSize = 10, studyStatus = '', phases = '' } = params;
  const currentPage = Math.max(Number(page), 1);
  const limit = Math.min(Number(pageSize), 100);
  const offset = (currentPage - 1) * limit;

  const where = {};
  if (studyStatus) where.study_status = studyStatus;
  if (phases) where.phases = phases;

  console.time(`${Model.name} findAndCountAll ==>`);
  console.log(`[${Model.name}] 查询条件：`, JSON.stringify(where));
  console.log(`[${Model.name}] 分页参数：page=${currentPage}，limit=${limit}，offset=${offset}`);
  const { count: total, rows: list } = await Model.findAndCountAll({
    where,
    limit,
    offset,
    order: [['last_update_posted', 'DESC']],
    raw: true,
    indexHints: [{ type: 'USE', values: ['idx_count_dummy'] }],
  });
  console.timeEnd(`${Model.name} findAndCountAll ==>`);
  console.log(`[${Model.name}] 符合条件总数：${total}，当前页数据量：${list.length}`);

  return { list, currentPage, limit, offset, total };
}

/**
 * all模式：先显示中国所有分页，再显示美国所有分页（分阶段分页）
 * @param {Object} params - 查询参数
 * @returns {Object} 综合分页结果
 */
async function getAllClinicalTrialPaged(params) {
  const { page = 1, pageSize = 10, studyStatus = '', phases = '' } = params;
  const currentPage = Math.max(Number(page), 1); // 确保页码≥1
  const limit = Math.min(Number(pageSize), 100); // 最大页大小限制

  // 筛选条件（中美共用）
  const where = {};
  if (studyStatus) where.study_status = studyStatus;
  if (phases) where.phases = phases;

  console.time('all -> phase paging ==>');
  console.log(`[all模式] 分页请求：page=${currentPage}，pageSize=${limit}，筛选条件=${JSON.stringify(where)}`);

  // 1. 并行查询中美两国的「总数」（仅查count，不查数据，速度极快）
  const [chinaCountResult, usaCountResult] = await Promise.all([
    ClinicalTrialChina.count({ where }), // 中国总数据量
    ClinicalTrialUsa.count({ where })    // 美国总数据量
  ]);
  const chinaTotal = chinaCountResult;
  const usaTotal = usaCountResult;
  const total = chinaTotal + usaTotal; // 中美总数据量

  // 2. 计算中美各自的总页数
  const chinaTotalPages = chinaTotal > 0 ? Math.ceil(chinaTotal / limit) : 0; // 中国总页数
  const usaTotalPages = usaTotal > 0 ? Math.ceil(usaTotal / limit) : 0;       // 美国总页数
  const totalPages = chinaTotalPages + usaTotalPages; // 综合总页数

  console.log(`[all模式] 分页阶段计算：`);
  console.log(`- 中国：总数=${chinaTotal}，总页数=${chinaTotalPages} 页`);
  console.log(`- 美国：总数=${usaTotal}，总页数=${usaTotalPages} 页`);
  console.log(`- 综合：总数=${total}，总页数=${totalPages} 页`);

  // 3. 判断当前页码归属阶段
  let pagedResult = { list: [], currentPage, pageSize: limit };

  // 阶段1：当前页属于中国分页（前chinaTotalPages页）
  if (currentPage <= chinaTotalPages && chinaTotalPages > 0) {
    console.log(`[all模式] 当前页属于「中国阶段」，查询中国第 ${currentPage} 页`);
    const chinaPaged = await getSingleTablePaged(ClinicalTrialChina, {
      ...params,
      page: currentPage, // 直接用当前页查询中国
      pageSize: limit,
      studyStatus,
      phases
    });
    pagedResult.list = chinaPaged.list;

  // 阶段2：当前页属于美国分页（chinaTotalPages+1 到 totalPages页）
  } else if (currentPage > chinaTotalPages && currentPage <= totalPages && usaTotalPages > 0) {
    const usaCurrentPage = currentPage - chinaTotalPages; // 美国的实际页码（偏移中国总页数）
    console.log(`[all模式] 当前页属于「美国阶段」，查询美国第 ${usaCurrentPage} 页（原页=${currentPage} - 中国总页数=${chinaTotalPages}）`);
    const usaPaged = await getSingleTablePaged(ClinicalTrialUsa, {
      ...params,
      page: usaCurrentPage, // 用偏移后的页码查询美国
      pageSize: limit,
      studyStatus,
      phases
    });
    pagedResult.list = usaPaged.list;

  // 阶段3：页码超出总页数（无更多数据）
  } else {
    console.log(`[all模式] 当前页 ${currentPage} 超出总页数 ${totalPages}，无更多数据`);
    pagedResult.list = [];
  }

  console.timeEnd('all -> phase paging ==>');
  console.log(`[all模式] 最终结果：当前页=${currentPage}，数据量=${pagedResult.list.length}`);

  // 4. 返回综合分页信息（总数、总页数为中美之和）
  return {
    ...pagedResult,
    total,
    totalPages
  };
}

/**
 * 主函数：分页查询分发（简洁无冗余）
 * @param {Object} params - 查询参数
 * @returns {Object} 最终分页结果
 */
async function getClinicalTrialPaged(params) {
  const { tableType } = params;

  if (!['usa', 'china', 'all'].includes(tableType)) {
    throw new Error('表类型错误，仅支持 usa、china 或 all');
  }

  switch (tableType) {
    case 'usa':
      return getSingleTablePaged(ClinicalTrialUsa, params);
    case 'china':
      return getSingleTablePaged(ClinicalTrialChina, params);
    case 'all':
      return getAllClinicalTrialPaged(params);
    default:
      throw new Error('无效的表类型');
  }
}

module.exports = {
  getClinicalTrialPaged,
};