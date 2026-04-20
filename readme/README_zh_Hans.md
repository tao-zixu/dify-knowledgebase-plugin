## Tablestore RAG 外部知识库


### 概述

将阿里云表格存储（Tablestore）RAG 服务作为 Dify 外部知识库接入。通过本插件，您可以在 Dify 应用中直接使用表格存储提供的企业级 RAG 能力，包括向量检索、全文检索、混合检索、重排序等。

### 前置条件

- 已开通阿里云表格存储服务的阿里云账号
- 已创建表格存储实例，并在实例中创建了 RAG 知识库
- 表格存储 Endpoint URL（例如 `https://instanceName.RegionID.ots.aliyuncs.com`）
- 表格存储实例名称
- 阿里云 Access Key ID 和 Access Key Secret
- OTS RAG 平台中的知识库名称（`knowledgeBaseName`）

### 配置端点

安装插件后，需要配置以下参数：

| 配置项 | 说明 | 示例 |
|--------|------|------|
| Tablestore Endpoint | 表格存储实例的 Endpoint URL | `https://instanceName.RegionID.ots.aliyuncs.com` |
| Tablestore Instance Name | 表格存储实例名称 | `your-instance` |
| Access Key ID | 阿里云 Access Key ID | `****` |
| Access Key Secret | 阿里云 Access Key Secret | `****` |
| Endpoint Protection Key | 可选。用于保护端点的访问密钥 | `your-secret` |

### 在 Dify 中添加外部知识库 API

1. 配置端点后，插件会生成一个端点 URL，格式如：`POST http://xxxx/e/xxxxx/retrieval`
2. 进入 Dify **知识库** > **外部知识库 API** > **添加外部知识库 API**
3. 填写以下信息：
   - **名称**：自定义名称
   - **API Endpoint**：使用生成的 URL，但需要做两处修改：
     - **去掉**末尾的 `/retrieval`（Dify 会自动追加该路径）
     - 如果使用 Docker 本地部署 Dify，**将 `localhost` 替换为 `host.docker.internal`**
   - **API Key**：填写上面配置的端点保护密钥（如未设置则填任意值）

> **注意**：
> 1. 必须删除 URL 末尾的 `/retrieval`，Dify 在调用时会自动追加该路径。
> 2. 如果 Dify 通过 Docker 部署在本地，需要将 URL 中的 `localhost` 替换为 `host.docker.internal`，否则 Docker 容器内无法访问宿主机网络。
> 3. API Key 如未在端点配置中设置保护密钥，可填写任意值。请妥善保管端点 URL，避免泄露。

### 创建知识库并使用

1. 新建知识库 > 选择 **连接外部知识库**
2. 选择刚刚添加的外部知识库 API
3. **外部知识库 ID** 填写 OTS RAG 平台中的知识库名称（`knowledgeBaseName`）

### 参数说明

- `top_k`：传递给 OTS RAG 后端，控制返回的检索结果数量
- `score_threshold`：在插件端进行过滤，低于该分数的结果将被丢弃
- 检索策略（向量检索 / 全文检索 / 混合检索、重排序等）由 OTS RAG 平台配置决定，不由本插件控制
