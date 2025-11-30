const { DataTypes } = require('sequelize');
const sequelize = require('../config/db');

const ClinicalTrialUsa = sequelize.define(
  'ClinicalTrialUsa',
  {
    nct_number: {
      type: DataTypes.STRING(50),
      primaryKey: true,
      allowNull: false,
      comment: '临床试验唯一编号（如 NCT03140917）'
    },
    study_title: {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: '研究完整标题'
    },
    study_url: {
      type: DataTypes.STRING(255),
      allowNull: true,
      comment: '研究详情页 URL（如 https://clinicaltrials.gov/study/NCTxxx）'
    },
    acronym: {
      type: DataTypes.STRING(100),
      allowNull: true,
      comment: '研究缩写（无缩写则为空）'
    },
    study_status: {
      type: DataTypes.STRING(50),
      allowNull: true,
      comment: '研究状态（枚举值：COMPLETED/NOT_YET_RECRUITING 等）'
    },
    brief_summary: {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: '研究简要摘要（描述研究目的和核心设计）'
    },
    study_results: {
      type: DataTypes.STRING(100),
      allowNull: true,
      comment: '是否发布研究结果（枚举值：YES/NO）'
    },
    conditions: {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: '研究针对的疾病/条件（多值用"|"分隔，如 Hepatocellular Carcinoma|Liver Metastases）'
    },
    interventions: {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: '干预措施（多值用"|"分隔，如 DRUG:Sintilimab|PROCEDURE:TACE）'
    },
    // 关键修正：LONGTEXT → TEXT
    primary_outcome_measures: {
      type: DataTypes.TEXT, // 原 DataTypes.LONGTEXT（错误）
      allowNull: true,
      comment: '主要结局指标（格式：指标名,定义,测量时间，多值用"|"分隔）'
    },
    // 关键修正：LONGTEXT → TEXT
    secondary_outcome_measures: {
      type: DataTypes.TEXT, // 原 DataTypes.LONGTEXT（错误）
      allowNull: true,
      comment: '次要结局指标（格式同主要指标，无则为空）'
    },
    // 关键修正：LONGTEXT → TEXT
    other_outcome_measures: {
      type: DataTypes.TEXT, // 原 DataTypes.LONGTEXT（错误）
      allowNull: true,
      comment: '其他结局指标（无则为空）'
    },
    sponsor: {
      type: DataTypes.STRING(255),
      allowNull: true,
      comment: '研究申办方（如 Tongji Hospital）'
    },
    collaborators: {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: '合作机构（多值用"|"分隔，无则为空）'
    },
    sex: {
      type: DataTypes.STRING(20),
      allowNull: true,
      comment: '纳入性别范围（枚举值：ALL/Male/Female）'
    },
    age: {
      type: DataTypes.STRING(50),
      allowNull: true,
      comment: '纳入年龄范围（如 ADULT, OLDER_ADULT）'
    },
    phases: {
      type: DataTypes.STRING(50),
      allowNull: true,
      comment: '临床试验阶段（枚举值：PHASE2/PHASE3，无则为空）'
    },
    enrollment: {
      type: DataTypes.INTEGER,
      allowNull: true,
      comment: '预计/实际纳入人数（整数）'
    },
    funder_type: {
      type: DataTypes.STRING(50),
      allowNull: true,
      comment: '资助方类型（如 OTHER）'
    },
    study_type: {
      type: DataTypes.STRING(50),
      allowNull: true,
      comment: '研究类型（枚举值：OBSERVATIONAL/INTERVENTIONAL）'
    },
    study_design: {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: '研究设计详情（如 分配方式:RANDOMIZED|干预模型:PARALLEL）'
    },
    other_ids: {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: '其他研究编号（多值用"|"分隔，如 2016-0251|NCI-2016-01983）'
    },
    start_date: {
      type: DataTypes.STRING(20),
      allowNull: true,
      comment: '研究开始日期（支持格式：YYYY-MM 或 YYYY-MM-DD）'
    },
    primary_completion_date: {
      type: DataTypes.STRING(20),
      allowNull: true,
      comment: '主要完成日期（格式同开始日期）'
    },
    completion_date: {
      type: DataTypes.STRING(20),
      allowNull: true,
      comment: '研究完成日期（格式同开始日期）'
    },
    first_posted: {
      type: DataTypes.DATE,
      allowNull: true,
      comment: '研究首次发布日期（完整格式：YYYY-MM-DD）'
    },
    results_first_posted: {
      type: DataTypes.DATE,
      allowNull: true,
      comment: '结果首次发布日期（无则为空）'
    },
    last_update_posted: {
      type: DataTypes.DATE,
      allowNull: true,
      comment: '研究记录最后更新日期（完整格式：YYYY-MM-DD）'
    },
    // 关键修正：LONGTEXT → TEXT
    locations: {
      type: DataTypes.TEXT, // 原 DataTypes.LONGTEXT（错误）
      allowNull: true,
      comment: '研究实施地点（多值用"|"分隔，含机构名和地址）'
    },
    study_documents: {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: '研究文档（格式：文档名,URL，如 Study Protocol,https://xxx.pdf）'
    }
  },
  {
    tableName: 'clinicaltrial_usa',
    timestamps: false,
    freezeTableName: true,
    underscored: false,
    paranoid: false,
    hooks: {},
    instanceMethods: {},
    classMethods: {}
  }
);

module.exports = ClinicalTrialUsa;