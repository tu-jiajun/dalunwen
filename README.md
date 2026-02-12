# 临床试验方案数据挖掘平台 (Clinical Trial Protocol Data Mining Platform)

## 📖 项目简介

本项目是一个面向临床试验方案的数据挖掘平台，旨在帮助研究人员和管理人员高效地收集、管理和分析来自不同源（如中国临床试验注册中心 ChiCTR 和美国 ClinicalTrials.gov）的临床试验数据。平台提供了强大的仓库管理功能，支持多用户协作，并集成了数据清洗与分析的基础架构。

## 🏗️ 技术架构

本项目采用 Monorepo 架构（单仓多包），前后端分离开发。

### 前端 (Frontend)

- **核心框架**: Vue 3.5 + TypeScript
- **UI 组件库**: Element Plus 2.11.8
- **构建工具**: Vite
- **状态/路由**: Vue Router
- **HTTP 请求**: Axios

### 后端 (Backend)

- **运行环境**: Node.js
- **Web 框架**: Koa 2
- **数据库**: MySQL
- **ORM 框架**: Sequelize
- **认证机制**: JWT (JSON Web Token)

## 快速启动

```bash
npm install

cd packages/frontend
npm run dev

cd packages/backend
npm run dev
```

## 📂 项目结构

```
dalunwen/
├── packages/
│   ├── frontend/       # 前端项目源码
│   │   ├── src/        # 页面、组件、API等
│   │   └── ...
│   ├── backend/        # 后端项目源码
│   │   ├── controller/ # 控制器层
│   │   ├── service/    # 业务逻辑层
│   │   ├── model/      # 数据库模型定义
│   │   ├── config/     # 数据库及系统配置
│   │   └── ...
└── README.md           # 项目说明文档
```

## 🚀 快速开始

### 1. 环境准备

确保您的本地环境已安装以下软件：

- **Node.js**: 推荐 v16 或更高版本
- **MySQL**: 推荐 v8.0 或更高版本

### 2. 数据库配置

在启动后端之前，请先在 MySQL 中创建一个空的数据库。

```sql
CREATE DATABASE dalunwen CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 后端启动 (Backend)

进入后端目录并安装依赖：

```bash
cd packages/backend
npm install
```

在 `packages/backend` 目录下创建 `.env` 文件，并填入以下配置：

```ini
# 服务器端口
PORT=3000
# 环境 (development / production)
NODE_ENV=development

# 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_username    # 替换为您的 MySQL 用户名
MYSQL_PASSWORD=your_password # 替换为您的 MySQL 密码
MYSQL_DB=dalunwen           # 数据库名称
```

启动后端服务：

```bash
npm run dev
```

> 后端启动时会自动检测并初始化数据库表结构。

### 4. 前端启动 (Frontend)

进入前端目录并安装依赖：

```bash
cd packages/frontend
npm install
```

在 `packages/frontend` 目录下创建 `.env` 文件（如已有 `.env` 可根据需要修改）：

```ini
# API 基础路径
VITE_API_BASE_URL=http://localhost:3000
# 请求超时时间 (毫秒)
VITE_TIMEOUT=5000
```

启动前端开发服务器：

```bash
npm run dev
```

### 5. 访问项目

打开浏览器访问前端控制台输出的地址（通常为 `http://localhost:5173`）。

## ✨ 主要功能

- **多源数据集成**: 支持 ChiCTR 和 ClinicalTrials.gov 数据结构。
- **仓库管理**: 用户可以创建个人或团队的数据仓库 (Warehouse)。
- **数据挖掘与分析**: (开发中) 提供针对临床试验方案的深度挖掘工具。
- **用户权限管理**: 基于角色的访问控制和安全认证。

## 🛠️ 开发指南

- **API 工具**: 前端所有 API 调用封装在 `src/utils/api` 目录下。
- **数据库同步**: 后端在开发环境下 (`NODE_ENV=development`) 会自动同步 Sequelize 模型更改到数据库。
