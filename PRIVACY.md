## 隐私说明

### 概述

本插件（Tablestore RAG 外部知识库）是 Dify 与阿里云表格存储 RAG 服务之间的连接器，仅负责转发检索请求和结果，**不持久化存储任何数据**。

### 处理的数据

插件在运行过程中会经手以下类型的数据：

1. **阿里云凭证（Access Key ID / Access Key Secret）**
   由 Dify 的安全凭证存储系统管理和保存，插件仅在发起请求时读取使用。

2. **OTS 连接配置**
   表格存储 Endpoint URL 和实例名称，通过 Dify 端点设置进行配置。

3. **查询数据**
   - 从 Dify 发送到表格存储 RAG 的查询文本和知识库标识
   - 检索参数（top_k、score_threshold）
   - 表格存储 RAG 返回的检索结果（仅在内存中短暂存在）

   以上数据仅在请求处理期间使用，插件不会对其进行持久化存储。

### 数据传输

所有数据通过阿里云表格存储 SDK 传输，该 SDK 使用私有 Protobuf 协议，基于 HTTPS 加密通信。

### 数据存储

插件本身不持久化存储任何数据。所有持久化数据的存储由以下服务负责：

- **Dify**：管理凭证、查询记录、检索结果等
- **阿里云表格存储**：管理已索引的文档内容和知识库数据

### 第三方服务

本插件依赖以下第三方服务：

- 阿里云表格存储 (https://www.alibabacloud.com/product/table-store)
- Dify (https://dify.ai)

用户应参阅上述服务的隐私政策，了解其数据处理方式：

- 阿里云隐私政策 (https://www.alibabacloud.com/trust-center/privacy)
- Dify 隐私政策 (https://dify.ai/privacy)
