# Database Schema

## 数据库设计文档

### 概述

许愿墙使用PostgreSQL作为主要数据库，采用关系型数据模型。

## 数据表

### 1. users (用户表)

存储用户账户信息。

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    avatar_url TEXT,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

**字段说明**:
- `id`: 用户唯一标识
- `username`: 用户名（唯一）
- `email`: 邮箱地址（唯一）
- `password_hash`: 密码哈希值
- `avatar_url`: 头像URL
- `bio`: 个人简介
- `created_at`: 创建时间
- `updated_at`: 更新时间
- `is_active`: 账户是否激活

### 2. wishes (愿望表)

存储用户发布的愿望信息。

```sql
CREATE TABLE wishes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    deadline DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**字段说明**:
- `id`: 愿望唯一标识
- `user_id`: 发布者用户ID
- `title`: 愿望标题
- `description`: 愿望描述
- `category`: 分类（education, career, health, hobby等）
- `status`: 状态（active, completed, cancelled）
- `likes_count`: 点赞数
- `comments_count`: 评论数
- `deadline`: 完成截止日期
- `created_at`: 创建时间
- `updated_at`: 更新时间

### 3. comments (评论表)

存储用户对愿望的评论。

```sql
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    wish_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wish_id) REFERENCES wishes(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**字段说明**:
- `id`: 评论唯一标识
- `wish_id`: 所属愿望ID
- `user_id`: 评论者用户ID
- `content`: 评论内容
- `created_at`: 创建时间
- `updated_at`: 更新时间

### 4. likes (点赞表)

存储用户对愿望的点赞记录。

```sql
CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    wish_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(wish_id, user_id),
    FOREIGN KEY (wish_id) REFERENCES wishes(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**字段说明**:
- `id`: 点赞记录唯一标识
- `wish_id`: 被点赞的愿望ID
- `user_id`: 点赞者用户ID
- `created_at`: 点赞时间

### 5. categories (分类表)

存储愿望分类信息。

```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    icon_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**字段说明**:
- `id`: 分类唯一标识
- `name`: 分类名称
- `description`: 分类描述
- `icon_url`: 分类图标URL
- `created_at`: 创建时间

## 索引

```sql
-- 性能优化索引
CREATE INDEX idx_wishes_user_id ON wishes(user_id);
CREATE INDEX idx_wishes_category ON wishes(category);
CREATE INDEX idx_wishes_created_at ON wishes(created_at);
CREATE INDEX idx_comments_wish_id ON comments(wish_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_likes_wish_id ON likes(wish_id);
CREATE INDEX idx_likes_user_id ON likes(user_id);
```

## 关系图

```
users
  ├── wishes (1:N)
  ├── comments (1:N)
  └── likes (1:N)

wishes
  ├── comments (1:N)
  └── likes (1:N)

comments
  └── 关联到 wishes 和 users

likes
  └── 关联到 wishes 和 users
```

## 数据规范

### 字符编码
- 所有文本字段使用UTF-8编码
- 支持中文、英文、表情符等

### 时间戳
- 所有时间戳使用UTC时区
- 格式: TIMESTAMP

### 数据一致性
- 使用外键约束保证引用完整性
- 使用UNIQUE约束防止重复数据
- 使用DEFAULT约束设置默认值

## 备份策略

- 每日自动备份
- 备份文件存储在安全位置
- 定期测试恢复流程
