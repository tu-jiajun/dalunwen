// config/initDatabase.js
const sequelize = require('./db');
const User = require('../model/User');
const UserWarehouse = require('../model/UserWarehouse');
const ClinicalTrialWarehouse = require('../model/ClinicalTrialWarehouse');

function initAssociations() {
  const models = { User, UserWarehouse, ClinicalTrialWarehouse };
  Object.keys(models).forEach(key => {
    if (models[key].associate) {
      models[key].associate(models);
    }
  });
  console.log('✅ 模型关联初始化完成');
}

async function initDatabase() {
  try {
    // 第一步：先验证数据库连接，再初始化关联
    await sequelize.authenticate();
    console.log('✅ 数据库连接成功');

    // 第二步：初始化关联（此时模型已加载完成，无重复）
    initAssociations();

    // 第三步：同步模型（仅开发环境）
    if (process.env.NODE_ENV === 'development') {
      await Promise.all([
        User.sync({ force: false }),
        UserWarehouse.sync({ force: false }),
        ClinicalTrialWarehouse.sync({ force: false }),
      ]);
    }
    console.log('✅ 所有表结构检测完成：不存在的表已创建，现有表无修改');

  } catch (error) {
    console.error('❌ 数据库初始化失败：', error.message);
    process.exit(1);
  }
}

initDatabase();
module.exports = initDatabase;