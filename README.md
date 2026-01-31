# Hots - Tech Trend Tracker 🔥

[![Live Demo](https://img.shields.io/badge/demo-online-green.svg)](https://trael8mykr1f.vercel.app/)
![Tech Stack](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-blue)
![Tech Stack](https://img.shields.io/badge/Backend-FastAPI-green)
![Tech Stack](https://img.shields.io/badge/Database-Supabase-orange)

> **🌟 Live Demo:** [https://trael8mykr1f.vercel.app/](https://trael8mykr1f.vercel.app/)
> 
> *Note: The demo is hosted on Vercel. Feel free to register a test account (username/password only) to experience the full features including favorites.*

Hots is a modern full-stack web application designed to help developers stay updated with the latest technology trends. It aggregates trending GitHub projects, Computer Vision papers from ArXiv, and top stories from Hacker News into a single, clean interface.

## ✨ Features

- **GitHub Trending**: Real-time crawling of GitHub's trending page to find the hottest repositories across different languages.
- **Academic Papers**: Daily updates of the latest Computer Vision (CV) papers from ArXiv.
- **Tech News**: Top stories from Hacker News.
- **User System**: 
  - Simplified **Username/Password** authentication (No email required).
  - User Profiles.
- **Favorites**: Save your favorite projects and papers to your personal collection.
- **Responsive Design**: Built with Tailwind CSS for a mobile-friendly experience.

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Routing**: React Router DOM

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Database Client**: Supabase Python Client
- **Crawlers**: 
  - `httpx` (Async HTTP client)
  - `BeautifulSoup4` (HTML parsing)
  - `feedparser` (RSS/Atom parsing)
- **Validation**: Pydantic

### Database & Auth
- **Provider**: Supabase (PostgreSQL)
- **Auth**: Supabase Auth (Customized for Username-only login)
- **Storage**: Postgres Tables with Row Level Security (RLS)

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- A Supabase account

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/hots.git
cd hots
```

### 2. Supabase Configuration
1.  Create a new project on [Supabase](https://supabase.com).
2.  Go to **Project Settings -> API** and copy your `Project URL` and `anon public key`.
3.  Go to **Authentication -> Providers -> Email**:
    *   **Enable** "Enable Email provider".
    *   **Disable** "Confirm email".
4.  Run the migration scripts in your Supabase SQL Editor (found in `supabase/migrations/`) to set up the database schema:
    *   `20240131000000_init_schema.sql`
    *   `20240131000001_add_user_trigger.sql` (Optional, logic moved to backend)
    *   `20240131000002_remove_email_column.sql`
    *   `20240131000003_change_favorites_item_id_type.sql`

### 3. Backend Setup
1.  Navigate to the `api` directory:
    ```bash
    cd api
    ```
2.  Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file in the `api` directory (or root) with your Supabase credentials:
    ```env
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_service_role_key
    ```
    *Note: For the backend to bypass email restrictions and create users, you MUST use the `service_role_key` here, NOT the anon key.*

5.  Run the server:
    ```bash
    uvicorn main:app --reload
    # or
    python -m uvicorn main:app --port 8000
    ```

### 4. Frontend Setup
1.  Navigate to the root directory (where `package.json` is):
    ```bash
    cd ..
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```
4.  Open [http://localhost:5173](http://localhost:5173) in your browser.

## 🕷️ Crawlers
The backend includes built-in crawlers. To manually trigger a crawl:
```bash
# Powershell
Invoke-WebRequest -Method POST -Uri http://localhost:8000/api/admin/crawl
# Curl
curl -X POST http://localhost:8000/api/admin/crawl
```

## 📦 Deployment

### Frontend (Vercel/Netlify)
1.  Push your code to GitHub.
2.  Import the project into Vercel.
3.  Set the Build Command to `npm run build`.
4.  Set the Output Directory to `dist`.

### Backend (Render/Railway)
1.  Push your code to GitHub.
2.  Create a new Web Service on Render/Railway.
3.  Set the Root Directory to `api`.
4.  Set the Build Command to `pip install -r requirements.txt`.
5.  Set the Start Command to `uvicorn main:app --host 0.0.0.0 --port $PORT`.
6.  Add your `SUPABASE_URL` and `SUPABASE_KEY` to the environment variables.

## 📄 License


# Hots - 技术趋势追踪器 🔥

> **🌟 在线演示：** [https://trael8mykr1f.vercel.app/](https://trael8mykr1f.vercel.app/)
> *注：演示版托管于 Vercel。欢迎注册测试账号（仅需用户名/密码）以体验包括“收藏夹”在内的全部功能。*

Hots 是一个现代化的全栈 Web 应用，旨在帮助开发者紧跟最新的技术趋势。它将 **GitHub 热门项目**、**ArXiv 计算机视觉论文**以及 **Hacker News 头条新闻**整合到一个简洁的界面中。

## ✨ 功能特性

* **GitHub Trending**：实时抓取 GitHub 趋势榜，发现各种编程语言下最热门的仓库。
* **学术论文**：每日更新来自 ArXiv 的最新计算机视觉 (CV) 领域论文。
* **技术新闻**：获取 Hacker News 的热门文章。
* **用户系统**：
* 简化的**用户名/密码**认证（无需邮箱）。
* 用户个人资料页。


* **收藏夹**：将你感兴趣的项目和论文保存到个人收藏中。
* **响应式设计**：基于 Tailwind CSS 构建，提供良好的移动端适配体验。

## 🛠️ 技术栈

### 前端

* **框架**：React 18 + TypeScript
* **构建工具**：Vite
* **样式**：Tailwind CSS
* **图标**：Lucide React
* **路由**：React Router DOM

### 后端

* **框架**：FastAPI (Python 3.10+)
* **数据库客户端**：Supabase Python Client
* **爬虫相关**：
* `httpx` (异步 HTTP 客户端)
* `BeautifulSoup4` (HTML 解析)
* `feedparser` (RSS/Atom 解析)


* **校验**：Pydantic

### 数据库 & 认证

* **供应商**：Supabase (PostgreSQL)
* **身份认证**：Supabase Auth（经过自定义，支持仅用户名登录）
* **存储**：Postgres 表，并启用行级安全策略 (RLS)

## 🚀 快速上手

### 前置条件

* Node.js 18+
* Python 3.10+
* 一个 Supabase 账号

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/hots.git
cd hots

```

### 2. Supabase 配置

1. 在 [Supabase](https://supabase.com) 上创建一个新项目。
2. 前往 **Project Settings -> API**，复制你的 `Project URL` 和 `anon public key`。
3. 前往 **Authentication -> Providers -> Email**：
* **启用 (Enable)** "Enable Email provider"。
* **禁用 (Disable)** "Confirm email"。


4. 在 Supabase 的 SQL Editor 中运行以下迁移脚本（位于 `supabase/migrations/` 目录下）以建立数据库结构：
* `20240131000000_init_schema.sql`
* `20240131000001_add_user_trigger.sql`（可选，逻辑已移至后端）
* `20240131000002_remove_email_column.sql`
* `20240131000003_change_favorites_item_id_type.sql`



### 3. 后端设置

1. 进入 `api` 目录：
```bash
cd api

```


2. 创建虚拟环境并激活：
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

```


3. 安装依赖：
```bash
pip install -r requirements.txt

```


4. 在 `api` 目录（或根目录）创建 `.env` 文件，填入你的 Supabase 凭据：
```env
SUPABASE_URL=你的_supabase_url
SUPABASE_KEY=你的_supabase_service_role_key

```


*注：为了让后端绕过邮箱限制并创建用户，这里**必须**使用 `service_role_key`，而不是 anon key。*
5. 启动服务器：
```bash
uvicorn main:app --reload
# 或者
python -m uvicorn main:app --port 8000

```



### 4. 前端设置

1. 返回根目录（`package.json` 所在目录）：
```bash
cd ..

```


2. 安装依赖：
```bash
npm install

```


3. 启动开发服务器：
```bash
npm run dev

```


4. 在浏览器中打开 [http://localhost:5173](https://www.google.com/search?q=http://localhost:5173)。

## 🕷️ 爬虫说明

后端内置了爬虫程序。如需手动触发抓取，可以运行：

```bash
# Powershell
Invoke-WebRequest -Method POST -Uri http://localhost:8000/api/admin/crawl
# Curl
curl -X POST http://localhost:8000/api/admin/crawl

```

## 📦 部署

### 前端 (Vercel/Netlify)

1. 将代码推送到 GitHub。
2. 在 Vercel 中导入项目。
3. 设置构建命令 (Build Command) 为 `npm run build`。
4. 设置输出目录 (Output Directory) 为 `dist`。

### 后端 (Render/Railway)

1. 将代码推送到 GitHub。
2. 在 Render/Railway 上创建新的 Web Service。
3. 设置根目录 (Root Directory) 为 `api`。
4. 设置构建命令为 `pip install -r requirements.txt`。
5. 设置启动命令为 `uvicorn main:app --host 0.0.0.0 --port $PORT`。
6. 在环境变量中添加 `SUPABASE_URL` 和 `SUPABASE_KEY`。

## 📄 开源协议

本项目基于 MIT 协议进行许可。
