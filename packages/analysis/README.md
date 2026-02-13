# Clinical Trial Analysis Service

这是一个基于 Python 的数据挖掘和分析服务，作为 `dalunwen` 项目的一部分。

## 🛠️ 技术栈

- **Python**: 3.8+
- **Web 框架**: FastAPI
- **数据处理**: Pandas, NumPy
- **机器学习**: Scikit-learn
- **数据库连接**: SQLAlchemy

## 🚀 快速开始

### 1. 创建虚拟环境

建议使用 `venv` 或 `conda` 创建独立的虚拟环境。

```bash
# 进入目录
cd packages/analysis

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS / Linux
source venv/bin/activate
# Windows
# venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
# or
./venv/bin/pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件：

```ini
PORT=8000
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DB=dalunwen
```

### 4. 启动服务

```bash
python main.py
# or
./venv/bin/python main.py
# 或者
uvicorn main:app --reload
```

服务将在 `http://localhost:8000` 启动。
API 文档位于 `http://localhost:8000/docs`。
