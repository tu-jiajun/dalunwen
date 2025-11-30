const { DataTypes } = require('sequelize');
const sequelize = require('../config/db');
const UserWarehouse = require('./UserWarehouse'); // 引入用户仓库模型
const ClinicalUSA = require('./ClinicalTrialUsa');
const ClinicalChina = require('./ClinicalTrialChina');

// 定义临床试验仓库关联模型（对应 clinical_trial_warehouse 表）
const ClinicalTrialWarehouse = sequelize.define('ClinicalTrialWarehouse', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
    comment: '主键ID'
  },
  warehouse_id: {
    type: DataTypes.INTEGER,
    allowNull: false,
    comment: '关联用户仓库表ID（user_warehouses.id）',
    validate: {
      notNull: { msg: '关联仓库ID不能为空' },
      isInt: { msg: '关联仓库ID必须为整数' }
    }
  },
  nct_number: {
    type: DataTypes.STRING(50),
    allowNull: true,
    trim: true,
    comment: '关联美国临床试验表NCT号（clinicaltrila_usa.nct_number）'
  },
  reg_number: {
    type: DataTypes.STRING(50),
    allowNull: true,
    trim: true,
    comment: '关联中国临床试验备案号（clinical_china.reg_number）'
  },
  dynamic_extra_fields: {
    type: DataTypes.JSON, // 适配JSON字段，存储动态扩展属性
    allowNull: true,
    comment: '动态额外字段（JSON格式，存储非核心/临时扩展属性）'
  },
  // createdAt/updatedAt 由 timestamps: true 自动生成
}, {
  tableName: 'clinical_trial_warehouse', // 手动指定表名
  timestamps: true,
  underscored: true,
  indexes: [
    // 配置索引，对齐建表语句
    {
      name: 'idx_warehouse_id',
      fields: ['warehouse_id']
    },
    {
      name: 'idx_nct_number',
      fields: ['nct_number']
    },
    {
      name: 'idx_reg_number',
      fields: ['reg_number']
    },
    // 联合唯一索引（避免同一仓库重复关联同一个NCT/备案号）
    {
      name: 'uk_warehouse_nct',
      fields: ['warehouse_id', 'nct_number'],
      unique: true
    },
    {
      name: 'uk_warehouse_reg',
      fields: ['warehouse_id', 'reg_number'],
      unique: true
    }
  ],
  comment: '临床试验仓库关联表（含动态扩展字段）'
});

// 建立关联关系
// 1. 临床试验关联记录属于某个用户仓库（多对一）
ClinicalTrialWarehouse.belongsTo(UserWarehouse, {
  foreignKey: 'warehouse_id',
  as: 'warehouse', // 关联别名，查询时 include: ['warehouse'] 关联仓库信息
  onDelete: 'RESTRICT',
  onUpdate: 'CASCADE'
});
// 2. 一个用户仓库包含多个临床试验关联记录（一对多）
UserWarehouse.hasMany(ClinicalTrialWarehouse, {
  foreignKey: 'warehouse_id',
  as: 'clinicalTrials', // 关联别名，查仓库时 include: ['clinicalTrials'] 查其所有临床试验
  onDelete: 'RESTRICT',
  onUpdate: 'CASCADE'
});

// 关联美国临床试验表
ClinicalTrialWarehouse.belongsTo(ClinicalUSA, {
  foreignKey: 'nct_number',
  as: 'clinicalUSA',
  targetKey: 'nct_number', // 目标表的主键/唯一键
  onDelete: 'SET NULL',
  onUpdate: 'CASCADE'
});
// 关联中国临床试验表
ClinicalTrialWarehouse.belongsTo(ClinicalChina, {
  foreignKey: 'reg_number',
  as: 'clinicalChina',
  targetKey: 'reg_number',
  onDelete: 'SET NULL',
  onUpdate: 'CASCADE'
});

// 同步模型到数据库（开发环境）
if (process.env.NODE_ENV === 'development') {
  ClinicalTrialWarehouse.sync({ force: false });
}

module.exports = ClinicalTrialWarehouse;