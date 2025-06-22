#!/usr/bin/env python3
"""
Pure MCP Server for Sentinel Asia Emergency Observation Request (EOR) API
Sentinel Asia緊急観測要請（EOR）APIの純粋MCPサーバー（Render確実対応版）
"""

import asyncio
import json
import httpx
import os
import uvicorn
from typing import Dict, List, Optional, Any, Union
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel

# API設定
API_BASE_URL = "https://reder-test-o5k8.onrender.com"

# FastAPIアプリケーションの初期化
app = FastAPI(
    title="Sentinel Asia EOR MCP Server",
    description="Model Context Protocol Server for Sentinel Asia Emergency Observation Request API",
    version="1.0.0"
)

# MCP Response Models
class MCPError(BaseModel):
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Union[str, int]
    method: str
    params: Optional[Dict[str, Any]] = None

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: Union[str, int]
    result: Optional[Any] = None
    error: Optional[MCPError] = None

async def make_api_request(
    endpoint: str, 
    params: Optional[Dict[str, str]] = None
) -> Any:
    """APIリクエストを実行する共通関数"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{API_BASE_URL}/{endpoint}",
                params=params or {},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_messages = {
                400: "無効なリクエストパラメータです",
                404: "データが見つかりません",
                500: "サーバー内部エラーです"
            }
            raise Exception(f"API Error {e.response.status_code}: {error_messages.get(e.response.status_code, '不明なエラー')}")
        except Exception as e:
            raise Exception(f"リクエストエラー: {str(e)}")

# MCPツール定義
TOOLS = {
    "get_countries": {
        "name": "get_countries",
        "description": "利用可能な国リストを取得します。アジア、中東、太平洋諸国の国名とISO3コードを返します。",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    "get_metadata": {
        "name": "get_metadata", 
        "description": "サービスのメタデータを取得します。",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    "get_events": {
        "name": "get_events",
        "description": "災害イベント（EOR）情報を取得します。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "countryiso3s": {
                    "type": "string",
                    "description": "カンマ区切りのISO3国コード（例：JPN,PHL,CHN）"
                },
                "start_date": {
                    "type": "string", 
                    "description": "開始日（YYYYMMDD または YYYY-MM-DD 形式）"
                },
                "end_date": {
                    "type": "string",
                    "description": "終了日（YYYYMMDD または YYYY-MM-DD 形式）"
                }
            },
            "required": []
        }
    },
    "get_products": {
        "name": "get_products",
        "description": "指定されたEORの成果物（プロダクト）情報を取得します。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "EOR詳細ページのURL"
                }
            },
            "required": ["url"]
        }
    }
}

async def handle_mcp_request(request: MCPRequest) -> MCPResponse:
    """MCPリクエストを処理"""
    try:
        if request.method == "initialize":
            return MCPResponse(
                id=request.id,
                result={
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "Sentinel Asia EOR API Server",
                        "version": "1.0.0"
                    }
                }
            )
        
        elif request.method == "tools/list":
            return MCPResponse(
                id=request.id,
                result={"tools": list(TOOLS.values())}
            )
        
        elif request.method == "tools/call":
            params = request.params or {}
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "get_countries":
                result = await make_api_request("get_countries")
                return MCPResponse(id=request.id, result={"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]})
            
            elif tool_name == "get_metadata":
                result = await make_api_request("get_metadata")
                return MCPResponse(id=request.id, result={"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]})
            
            elif tool_name == "get_events":
                api_params = {}
                if arguments.get("countryiso3s"):
                    api_params["countryiso3s"] = arguments["countryiso3s"]
                if arguments.get("start_date"):
                    api_params["start_date"] = arguments["start_date"]
                if arguments.get("end_date"):
                    api_params["end_date"] = arguments["end_date"]
                
                result = await make_api_request("get_events", api_params)
                return MCPResponse(id=request.id, result={"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]})
            
            elif tool_name == "get_products":
                if not arguments.get("url"):
                    return MCPResponse(
                        id=request.id,
                        error=MCPError(code=-32602, message="URL parameter is required")
                    )
                
                result = await make_api_request("get_products", {"url": arguments["url"]})
                return MCPResponse(id=request.id, result={"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]})
            
            else:
                return MCPResponse(
                    id=request.id,
                    error=MCPError(code=-32601, message=f"Unknown tool: {tool_name}")
                )
        
        else:
            return MCPResponse(
                id=request.id,
                error=MCPError(code=-32601, message=f"Unknown method: {request.method}")
            )
    
    except Exception as e:
        return MCPResponse(
            id=request.id,
            error=MCPError(code=-32603, message=str(e))
        )

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "Sentinel Asia EOR MCP Server",
        "status": "running",
        "protocol": "MCP",
        "endpoints": {
            "health": "/health",
            "mcp": "/sse"
        }
    }

@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy", "service": "Sentinel Asia EOR MCP Server"}

@app.post("/sse")
async def mcp_sse_endpoint(request: Request):
    """MCP SSEエンドポイント"""
    async def event_generator():
        try:
            body = await request.json()
            mcp_request = MCPRequest(**body)
            response = await handle_mcp_request(mcp_request)
            yield {"data": response.model_dump_json()}
        except Exception as e:
            error_response = MCPResponse(
                id=0,
                error=MCPError(code=-32700, message=f"Parse error: {str(e)}")
            )
            yield {"data": error_response.model_dump_json()}
    
    return EventSourceResponse(event_generator())

if __name__ == "__main__":
    # Render用の環境変数設定
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"Starting Sentinel Asia EOR Pure MCP Server...")
    print(f"Server will bind to {host}:{port}")
    print(f"MCP endpoint: http://{host}:{port}/sse")
    
    # uvicornでアプリを起動
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    ) 