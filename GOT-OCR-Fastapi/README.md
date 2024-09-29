
# GOT-OCR-FastAPI

这是一个使用FastAPI构建的OCR服务项目，提供了图像识别的API接口以及客户端调用示例。

## 目录结构

```
GOT-OCR-FastAPI
├── app
│   └── client.py  # 客户端脚本
├── poetry.lock
├── pyproject.toml
└── start_app.py   # 启动FastAPI应用的脚本
```

## 快速开始

### 前提条件

- Python 3.x
- [Poetry](https://python-poetry.org/) 用于依赖管理

### 安装与启动服务

1. 克隆或下载此仓库至本地目录。

2. 切换到项目目录：

   ```shell
   cd GOT-OCR-Fastapi
   ```

3. 使用Poetry创建虚拟环境并安装依赖：

   ```shell
   poetry shell
   poetry install
   ```

4. 启动FastAPI应用服务器：

   ```shell
   python start_app.py
   ```

   此命令会启动FastAPI服务器，默认监听在 `http://127.0.0.1:8000/`。

5. 转到 `app` 目录并运行客户端脚本来测试API：

   ```shell
   cd app
   python client.py
   ```

   `client.py` 脚本应该包含了发送请求到FastAPI服务器以及处理响应的方法。

## 项目结构

- `start_app.py`: 包含启动FastAPI应用的逻辑。
- `client.py`: 包含客户端代码，用于向FastAPI应用发送请求。
- `pyproject.toml`: Poetry配置文件，定义了项目的元数据和依赖关系。
- `poetry.lock`: 锁定文件，保证每次安装的依赖版本一致。
