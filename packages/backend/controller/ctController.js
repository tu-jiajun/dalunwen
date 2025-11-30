const Joi = require('joi');
const ctService = require('../service/ctService');

/**
 * 分页查询控制器（处理请求 + 响应）
 * @param {Object} ctx - Koa 上下文（包含请求参数、响应对象）
 */
async function getPagedClinicalTrial(ctx) {
  try {
    const query = ctx.query;
    const querySchema = Joi.object({
      tableType: Joi.string()
        .valid('usa', 'china', 'all')
        .required()
        .messages({
          'string.valid': 'tableType 只能是 usa（美国临床试验）或 china（中国临床试验）',
          'any.required': 'tableType 为必填项'
        }),
      page: Joi.number()
        .integer()
        .min(1)
        .default(1)
        .messages({ 'number.integer': 'page 必须是正整数' }),
      pageSize: Joi.number()
        .integer()
        .min(1)
        .max(100)
        .default(10)
        .messages({
          'number.integer': 'pageSize 必须是正整数',
          'number.max': 'pageSize 最大为 100'
        }),
      studyStatus: Joi.string().allow('').default(''), // 可选筛选条件
      phases: Joi.string().allow('').default('') // 可选筛选条件
    });

    const { error, value } = querySchema.validate(query);
    if (error) {
      ctx.status = 400;
      ctx.body = { code: 400, message: error.details[0].message };
      return;
    }

    const pagedData = await ctService.getClinicalTrialPaged(value);

    ctx.status = 200;
    ctx.body = {
      code: 200,
      message: '临床试验分页查询成功',
      data: pagedData
    };
  } catch (err) {
    ctx.throw(500, err.message);
  }
}

module.exports = {
  getPagedClinicalTrial,
};