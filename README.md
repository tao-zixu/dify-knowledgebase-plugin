## Tablestore RAG Knowledge Base


### Overview

Integrate Alibaba Cloud Tablestore RAG service as a Dify external knowledge base. With this plugin, you can directly use Tablestore's enterprise-grade RAG capabilities in Dify applications, including vector search, full-text search, hybrid search, reranking, and more.

### Prerequisites

- An Alibaba Cloud account with Tablestore service enabled
- A Tablestore instance with a RAG knowledge base created
- Tablestore Endpoint URL (e.g., `http://ots-{instance-name}.aliyuncs.com`)
- Tablestore instance name
- Alibaba Cloud Access Key ID and Access Key Secret
- Knowledge base name from the OTS RAG platform (`knowledgeBaseName`)

### Configure Endpoint

After installing the plugin, configure the following parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| Tablestore Endpoint | Endpoint URL of the Tablestore instance | `http://ots-{instance-name}.aliyuncs.com` |
| Tablestore Instance Name | Name of the Tablestore instance | `your-instance` |
| Access Key ID | Alibaba Cloud Access Key ID | `****` |
| Access Key Secret | Alibaba Cloud Access Key Secret | `****` |
| Endpoint Protection Key | Optional. Access key to protect the endpoint | `your-secret` |

### Add External Knowledge Base API in Dify

1. After configuring the endpoint, the plugin will generate an endpoint URL in the format: `POST http://xxxx/e/xxxxx/retrieval`
2. Go to Dify **Knowledge Base** > **External Knowledge Base API** > **Add External Knowledge Base API**
3. Fill in the following:
   - **Name**: A custom name of your choice
   - **API Endpoint**: Use the generated URL, but make two modifications:
     - **Remove** the trailing `/retrieval` (Dify will automatically append this path)
     - If you deployed Dify locally with Docker, **replace `localhost` with `host.docker.internal`**
   - **API Key**: Enter the endpoint protection key configured above (enter any value if not set)

> **Note**:
> 1. You MUST remove the trailing `/retrieval` from the URL. Dify will automatically append this path when making requests.
> 2. If Dify is deployed locally via Docker, you MUST replace `localhost` in the URL with `host.docker.internal`, as the Docker container cannot access the host network through `localhost`.
> 3. If you did not set an Endpoint Protection Key, you can enter any value for the API Key. Keep the endpoint URL confidential to prevent unauthorized access.

### Create and Use Knowledge Base

1. Create a new knowledge base > Select **Connect External Knowledge Base**
2. Select the external knowledge base API you just added
3. For **External Knowledge Base ID**, enter the knowledge base name from the OTS RAG platform (`knowledgeBaseName`)

### Parameter Description

- `top_k`: Passed to the OTS RAG backend, controls the number of retrieval results returned
- `score_threshold`: Filtered on the plugin side, results below this score will be discarded
- Retrieval strategy (vector search / full-text search / hybrid search, reranking, etc.) is determined by the OTS RAG platform configuration, not controlled by this plugin
