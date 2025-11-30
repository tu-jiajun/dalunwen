const { DataTypes } = require('sequelize');
const sequelize = require('../config/db'); // 引入 Sequelize 连接实例

/**
 * 中国临床试验 Model（仅表结构映射，无任何数据修改逻辑）
 * 核心约束：
 * 1. 严格对齐数据库表字段（名称、类型、注释、非空约束一致）
 * 2. 禁用自动时间字段、表名复数化，避免意外修改表结构
 * 3. 不添加任何增删改相关 hooks 或自定义方法
 * 4. 仅依赖 Sequelize 内置查询方法，不提供数据修改能力
 */
const ClinicalTrialChina = sequelize.define(
  'ClinicalTrialChina', // Model 逻辑名称（仅用于 Sequelize 内部引用）
  {
    // 主键字段（表中唯一非空字段）
    reg_number: {
      type: DataTypes.STRING(50), // 对应表中 varchar(50)
      primaryKey: true, // 标记为主键
      allowNull: false, // 表中定义为 NOT NULL，显式声明
      comment: '研究唯一编号（如 ChiCTR2500110623）'
    },
    // 普通字段（按表结构顺序严格映射）
    study_title: {
      type: DataTypes.TEXT, // 对应表中 text 类型
      allowNull: true,
      comment: '研究标题'
    },
    study_url: {
      type: DataTypes.STRING(255), // 对应表中 varchar(255)
      allowNull: true,
      comment: '研究详情页 URL'
    },
    study_status: {
      type: DataTypes.STRING(50), // 对应表中 varchar(50)
      allowNull: true,
      comment: '研究状态（如 Pending、Completed 等）'
    },
    brief_summary: {
      type: DataTypes.TEXT, // 对应表中 text
      allowNull: true,
      comment: '研究简要摘要'
    },
    conditions: {
      type: DataTypes.TEXT, // 对应表中 text
      allowNull: true,
      comment: '研究针对的疾病/条件'
    },
    primary_outcome_measures: {
      type: DataTypes.TEXT, // 对应表中 text
      allowNull: true,
      comment: '主要结局指标'
    },
    secondary_outcome_measures: {
      type: DataTypes.TEXT, // 对应表中 text
      allowNull: true,
      comment: '次要结局指标'
    },
    sponsor: {
      type: DataTypes.TEXT, // 对应表中 text（支持长文本申办方信息）
      allowNull: true,
      comment: '研究申办方'
    },
    sex: {
      type: DataTypes.STRING(20), // 对应表中 varchar(20)
      allowNull: true,
      comment: '研究对象性别范围（如 Both、Male 等）'
    },
    age: {
      type: DataTypes.STRING(50), // 对应表中 varchar(50)
      allowNull: true,
      comment: '研究对象年龄范围'
    },
    phases: {
      type: DataTypes.STRING(100), // 对应表中 varchar(100)（支持多阶段拼接）
      allowNull: true,
      comment: '临床试验阶段'
    },
    enrollment: {
      type: DataTypes.INTEGER, // 对应表中 int
      allowNull: true,
      comment: '研究纳入人数'
    },
    study_type: {
      type: DataTypes.STRING(50), // 对应表中 varchar(50)
      allowNull: true,
      comment: '研究类型（如 Observational study 等）'
    },
    study_design: {
      type: DataTypes.TEXT, // 对应表中 text
      allowNull: true,
      comment: '研究设计详情'
    },
    start_date: {
      type: DataTypes.DATE, // 对应表中 date 类型（完整 YYYY-MM-DD）
      allowNull: true,
      comment: '研究开始日期'
    },
    completion_date: {
      type: DataTypes.DATE, // 对应表中 date
      allowNull: true,
      comment: '研究完成日期'
    },
    first_posted: {
      type: DataTypes.DATE, // 对应表中 date
      allowNull: true,
      comment: '研究首次发布日期'
    },
    last_update_posted: {
      type: DataTypes.DATE, // 对应表中 date
      allowNull: true,
      comment: '研究最后更新日期'
    },
    locations: {
      type: DataTypes.TEXT, // 对应表中 text
      allowNull: true,
      comment: '研究实施地点'
    },
    study_design_detail: {
      type: DataTypes.TEXT, // 对应表中 text
      allowNull: true,
      comment: '研究设计补充说明'
    },
    sources_of_funding: {
      type: DataTypes.TEXT, // 对应表中 text
      allowNull: true,
      comment: '资金来源'
    }
  },
  {
    // Model 核心配置（确保与数据库表一致，禁止修改操作）
    tableName: 'clinicaltrial_china', // 强制绑定数据库表名
    timestamps: false, // 关闭自动生成 `createdAt`/`updatedAt` 字段（表中无）
    freezeTableName: true, // 禁止 Sequelize 复数化表名（关键约束）
    underscored: false, // 字段名不自动转为下划线（表中字段已规范命名）
    paranoid: false, // 关闭软删除（表中无 `deletedAt` 字段）
    // 禁用所有修改相关 hooks，避免意外触发数据修改
    hooks: {},
    // 不添加任何自定义实例方法（仅用 Sequelize 内置查询方法）
    instanceMethods: {},
    // 不添加任何自定义类方法（避免隐含修改逻辑）
    classMethods: {}
  }
);

/**
 * 暴露 Model 供 Service 层调用
 * 支持的查询方法：findAndCountAll（分页）、findOne（单条）、findByPk（按主键查）等
 * 禁止 Service 层调用：create、update、destroy、upsert 等修改类方法
 */
module.exports = ClinicalTrialChina;