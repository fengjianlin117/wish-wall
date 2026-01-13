# 许愿墙 (Wish Wall)

[English](README.md) | 简体中文

一个现代化的许愿墙应用，让用户可以分享和查看他人的美好愿望。

## 功能特性

- 📝 **发布愿望**: 用户可以轻松发布自己的美好愿望
- 💭 **浏览愿望**: 查看其他用户分享的有趣愿望
- ❤️ **互动功能**: 给喜欢的愿望点赞和评论
- 🏷️ **分类标签**: 通过标签对愿望进行分类和筛选
- 🔍 **搜索功能**: 快速查找特定的愿望
- 📱 **响应式设计**: 在桌面和移动设备上都能完美显示
- 🌙 **暗黑模式**: 支持浅色和深色主题

## 技术栈

### 前端
- **Vue 3**: 现代化的 JavaScript 框架
- **Vite**: 闪电般快速的构建工具
- **Axios**: HTTP 客户端库
- **CSS3**: 样式和动画

### 后端
- **Python 3.11**: 服务端编程语言
- **FastAPI**: 高性能 Web 框架
- **Docker**: 容器化部署

## 快速开始

### 前置要求

- Node.js (v16+)
- Python 3.11+
- Docker (可选)

### 本地开发

#### 前端

```bash
cd frontend
npm install
npm run dev
```

前端将在 `http://localhost:5173` 启动

#### 后端

```bash
cd backend
bash start.sh
```

后端将在 `http://localhost:8000` 启动

### Docker 部署

```bash
# 构建后端镜像
docker build -t wish-wall-backend ./backend

# 运行容器
docker run -p 8000:8000 wish-wall-backend
```

## 项目结构

```
wish-wall/
├── frontend/              # 前端应用
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── backend/               # 后端应用
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── start.sh
├── README.md             # 英文文档
├── README-CN.md          # 中文文档
├── CONTRIBUTING.md       # 贡献指南
├── LICENSE               # MIT 许可证
└── .gitignore
```

## 使用方法

1. **访问应用**: 打开浏览器，访问 `http://localhost:5173`
2. **发布愿望**: 点击 "新建愿望" 按钮
3. **填写信息**: 输入愿望内容、选择分类和标签
4. **提交**: 点击 "发布" 完成
5. **浏览**: 在主页浏览其他用户的愿望
6. **互动**: 点赞、评论或分享感兴趣的愿望

## API 端点

### 愿望相关

- `GET /api/wishes` - 获取所有愿望
- `GET /api/wishes/{id}` - 获取特定愿望
- `POST /api/wishes` - 创建新愿望
- `PUT /api/wishes/{id}` - 更新愿望
- `DELETE /api/wishes/{id}` - 删除愿望

### 评论相关

- `GET /api/wishes/{id}/comments` - 获取愿望的评论
- `POST /api/wishes/{id}/comments` - 添加评论
- `DELETE /api/comments/{id}` - 删除评论

## 贡献

欢迎提交 Issues 和 Pull Requests！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系方式

如有任何问题或建议，请通过以下方式联系：

- 提交 GitHub Issues
- 发送邮件至 [your-email@example.com]
- 访问我们的网站 [your-website.com]

## 致谢

感谢所有为 Wish Wall 做出贡献的开发者和设计师！

---

**祝您使用愉快！** ✨
