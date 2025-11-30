// model/UserWarehouse.js（注意文件名大小写统一为大驼峰）
const { DataTypes } = require('sequelize');
const  sequelize  = require('../config/db'); 
const User = require('./User');

const UserWarehouse = sequelize.define('UserWarehouse', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
    comment: '仓库ID'
  },
  user_id: {
    type: DataTypes.INTEGER,
    allowNull: false,
    comment: '归属用户ID（关联users表id）',
    validate: {
      notNull: { msg: '归属用户ID不能为空' },
      isInt: { msg: '归属用户ID必须为整数' }
    }
  },
  warehouse_name: {
    type: DataTypes.STRING(100),
    allowNull: false,
    trim: true,
    comment: '仓库名称（如「我的临床试验库」）',
    validate: {
      notNull: { msg: '仓库名称不能为空' },
      len: [1, 100, '仓库名称长度需在1-100个字符之间']
    }
  }
}, {
  tableName: 'user_warehouses',
  timestamps: true,
  underscored: true,
  indexes: [
    { name: 'idx_user_id', fields: ['user_id'] },
    { name: 'idx_warehouse_name', fields: ['warehouse_name'] }
  ],
  comment: '用户仓库表（基础版）'
});

// 仅保留「仓库属于用户」的关联，且加防重复判断
if (!UserWarehouse.associations?.user) {
  UserWarehouse.belongsTo(User, {
    foreignKey: 'user_id',
    as: 'user',
    onDelete: 'RESTRICT',
    onUpdate: 'CASCADE'
  });
}


module.exports = UserWarehouse;
