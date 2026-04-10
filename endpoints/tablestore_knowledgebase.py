import json
from typing import Mapping
from werkzeug import Request, Response
from dify_plugin import Endpoint
import tablestore


class TablestoreKnowledgebaseEndpoint(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        
        if settings.get("api_key"):
            auth_header = r.headers.get("Authorization", "")
            if auth_header != f"Bearer {settings.get('api_key')}":
                return Response(
                    response=json.dumps({"error": "Unauthorized"}, ensure_ascii=False),
                    status=403,
                    content_type="application/json"
                )
        
        if not r.is_json:
            return Response(
                response=json.dumps({"records": []}, ensure_ascii=False),
                status=200,
                content_type="application/json"
            )
        
        body = r.json
        knowledge_id = body.get("knowledge_id", "")
        query = body.get("query", "")
        retrieval_setting = body.get("retrieval_setting", {})
        top_k = retrieval_setting.get("top_k", 5)
        score_threshold = retrieval_setting.get("score_threshold", 0.0)
        
        if not query:
            return Response(
                response=json.dumps({"records": []}, ensure_ascii=False),
                status=200,
                content_type="application/json"
            )
        
        ots_endpoint = settings.get("ots_endpoint", "")
        ots_instance = settings.get("ots_instance_name", "")
        ots_ak = settings.get("ots_access_key_id", "")
        ots_sk = settings.get("ots_access_key_secret", "")
        
        if not all([ots_endpoint, ots_instance, ots_ak, ots_sk]):
            return Response(
                response=json.dumps({"error": "Missing OTS configuration"}, ensure_ascii=False),
                status=500,
                content_type="application/json"
            )
        
        try:
            client = tablestore.OTSClient(
                end_point=ots_endpoint,
                access_key_id=ots_ak,
                access_key_secret=ots_sk,
                instance_name=ots_instance
            )
            
            retrieve_request = {
                "knowledgeBaseName": knowledge_id,
                "retrievalQuery": {
                    "type": "TEXT",
                    "text": query
                },
                "retrievalConfiguration": {
                    "rerankingConfiguration": {
                        "numberOfResults": top_k
                    }
                }
            }
            
            response_data = client.retrieve(retrieve_request)

            if response_data.get("code") != "SUCCESS":
                error_msg = response_data.get("message", "Unknown error")
                return Response(
                    response=json.dumps({"error": f"Retrieve API error: {error_msg}"}, ensure_ascii=False),
                    status=500,
                    content_type="application/json"
                )
            
            results = []
            retrieval_results = response_data.get("data", {}).get("retrievalResults", [])
            
            for item in retrieval_results:
                score = item.get("score", 0.0)
                if score < score_threshold:
                    continue
                
                content = item.get("content", "")
                oss_key = item.get("ossKey", "")
                doc_id = item.get("docId", "")
                chunk_id = item.get("chunkId", 0)
                subspace = item.get("subspace", "")
                metadata = item.get("metadata", {}) or {}
                
                if oss_key:
                    title = oss_key.split("/")[-1] if "/" in oss_key else oss_key
                else:
                    title = doc_id or ""
                
                results.append({
                    "content": content,
                    "score": score,
                    "title": title,
                    "metadata": {
                        "ossKey": oss_key,
                        "docId": doc_id,
                        "chunkId": chunk_id,
                        "subspace": subspace,
                        **{k: v for k, v in metadata.items() if isinstance(v, (str, int, float, bool))}
                    }
                })
        
        except tablestore.OTSClientError as e:
            return Response(
                response=json.dumps({"error": f"OTS Client error: {str(e)}"}, ensure_ascii=False),
                status=500,
                content_type="application/json"
            )
        except tablestore.OTSServiceError as e:
            return Response(
                response=json.dumps({
                    "error": f"OTS Service error: {e.get_error_code()} - {e.get_error_message()}"
                }, ensure_ascii=False),
                status=500,
                content_type="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"error": str(e)}, ensure_ascii=False),
                status=500,
                content_type="application/json"
            )
        
        return Response(
            response=json.dumps({"records": results[:top_k]}, ensure_ascii=False),
            status=200,
            content_type="application/json"
        )
