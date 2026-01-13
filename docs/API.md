# Wish Wall API Documentation

## API 概述

许愿墙API是一个RESTful API，提供用户、愿望、评论等资源的管理接口。

### 基础信息

- **Base URL**: `http://localhost:5000/api`
- **API Version**: v1
- **Content-Type**: `application/json`
- **Character Encoding**: UTF-8

## 认证

所有需要认证的端点都需要在请求头中包含 JWT Token：

```
Authorization: Bearer <your_jwt_token>
```

## 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

## 端点

### 健康检查

#### GET /health

检查API服务是否正常运行。

**示例响应**:
```json
{
  "status": "healthy",
  "message": "Wish Wall API is running"
}
```

### 用户管理 (Users)

#### POST /users

创建新用户。

**请求体**:
```json
{
  "username": "user123",
  "email": "user@example.com",
  "password": "password123"
}
```

**示例响应**:
```json
{
  "id": 1,
  "username": "user123",
  "email": "user@example.com",
  "created_at": "2026-01-13T13:14:11Z"
}
```

#### GET /users/{user_id}

获取用户信息。

#### PUT /users/{user_id}

更新用户信息（需要认证）。

### 愿望管理 (Wishes)

#### GET /wishes

获取所有愿望列表（支持分页）。

**查询参数**:
- `page`: 页码（默认: 1）
- `limit`: 每页条数（默认: 10）
- `sort`: 排序方式（latest, popular）

#### POST /wishes

创建新愿望（需要认证）。

**请求体**:
```json
{
  "title": "学习编程",
  "description": "我想成为一个优秀的开发者",
  "category": "education",
  "deadline": "2026-12-31"
}
```

#### GET /wishes/{wish_id}

获取愿望详情。

#### PUT /wishes/{wish_id}

更新愿望（需要认证，仅作者）。

#### DELETE /wishes/{wish_id}

删除愿望（需要认证，仅作者）。

### 评论管理 (Comments)

#### GET /wishes/{wish_id}/comments

获取愿望的评论列表。

#### POST /wishes/{wish_id}/comments

为愿望添加评论（需要认证）。

#### DELETE /comments/{comment_id}

删除评论（需要认证，仅评论作者）。

### 点赞管理 (Likes)

#### POST /wishes/{wish_id}/like

为愿望点赞（需要认证）。

#### DELETE /wishes/{wish_id}/like

取消点赞（需要认证）。

## 错误处理

所有错误响应都采用以下格式：

```json
{
  "status": "error",
  "code": "ERROR_CODE",
  "message": "Error message in Chinese"
}
```

## 速率限制

- 认证用户: 1000 请求/小时
- 匿名用户: 100 请求/小时

## 更新日志

### v0.1.0 (2026-01-13)

- 初始版本
- 基础CRUD操作
