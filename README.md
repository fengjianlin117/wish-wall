# 许愿墙 (Wish Wall)

一个现代化的许愿墙应用，让用户可以分享和实现他们的梦想和愿望。

## 项目概述

许愿墙是一个全栈Web应用，提供一个交互式平台，用户可以：
- 发布和分享他们的愿望
- 浏览其他用户的愿望
- 为他人的愿望点赞和评论
- 跟踪愿望的完成状态

## 技术栈

### 前端
- **框架**: Vue 3
- **构建工具**: Vite
- **语言**: TypeScript
- **样式**: CSS/SCSS

### 后端
- **框架**: Python Flask/FastAPI
- **数据库**: PostgreSQL
- **缓存**: Redis

## 项目结构

```
wish-wall/
├── frontend/          # Vue 3 前端应用
├── backend/           # Python 后端服务
├── docs/              # 项目文档
├── docker-compose.yml # Docker 编排配置
└── README.md          # 项目说明
```

## 快速开始

### 前置要求
- Node.js 16+
- Python 3.9+
- Docker & Docker Compose（可选）

### 开发环境设置

#### 前端
```bash
cd frontend
npm install
npm run dev
```

#### 后端
```bash
cd backend
pip install -r requirements.txt
python app.py
```

#### 使用 Docker
```bash
docker-compose up
```

## 文件说明

- `frontend/` - 前端应用代码
- `backend/` - 后端服务代码
- `docs/` - API 文档和数据库设计
- `docker-compose.yml` - Docker 服务编排

## 许可证

MIT License
