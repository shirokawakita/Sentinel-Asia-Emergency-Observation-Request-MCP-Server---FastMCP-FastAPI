#!/usr/bin/env python3
"""
MCP Server for Sentinel Asia Emergency Observation Request (EOR) API - SSE Version
Sentinel Asia緊急観測要請（EOR）APIのMCPサーバー - SSE版（Render対応）
"""

import asyncio
import httpx
import os
import uvicorn
from typing import Dict, List, Optional, Any
from fastmcp import FastMCP
from pydantic import BaseModel, Field

# API設定
API_BASE_URL = "https://reder-test-o5k8.onrender.com"

# レスポンスモデル
class CountryInfo(BaseModel):
    name: str
    iso3: str

class MetadataResponse(BaseModel):
    description: str
    licence: str
    methodology: str
    caveats: str

class EventInfo(BaseModel):
    name: str
    description: Optional[str] = None
    disaster_type: Optional[str] = None
    country: Optional[str] = None
    country_iso3: Optional[str] = None
    occurrence_date: Optional[str] = None
    sa_activation_date: Optional[str] = None
    requester: Optional[str] = None
    escalation_to_charter: Optional[str] = None
    glide_number: Optional[str] = None
    url: str

class ProductInfo(BaseModel):
    date: Optional[str] = None
    title: Optional[str] = None
    download_url: str
    view_url: Optional[str] = None
    file_type: Optional[str] = None

# MCPサーバーの初期化
mcp = FastMCP("Sentinel Asia EOR API Server")

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

@mcp.tool()
async def get_countries() -> List[Dict[str, str]]:
    """
    利用可能な国リストを取得します。
    アジア、中東、太平洋諸国の国名とISO3コードを返します。
    
    Returns:
        国名とISO3コードのリスト
    """
    return await make_api_request("get_countries")

@mcp.tool()
async def get_metadata() -> Dict[str, str]:
    """
    サービスのメタデータを取得します。
    
    Returns:
        サービスの説明、ライセンス、方法論、注意事項
    """
    return await make_api_request("get_metadata")

@mcp.tool()
async def get_events(
    countryiso3s: Optional[str] = Field(None, description="カンマ区切りのISO3国コード（例：JPN,PHL,CHN）"),
    start_date: Optional[str] = Field(None, description="開始日（YYYYMMDD または YYYY-MM-DD 形式）"),
    end_date: Optional[str] = Field(None, description="終了日（YYYYMMDD または YYYY-MM-DD 形式）")
) -> List[Dict[str, Any]]:
    """
    災害イベント（EOR）情報を取得します。
    
    Args:
        countryiso3s: フィルタする国のISO3コード（カンマ区切り）
        start_date: 開始日（YYYYMMDD または YYYY-MM-DD 形式）
        end_date: 終了日（YYYYMMDD または YYYY-MM-DD 形式）
    
    Returns:
        災害イベント情報のリスト（名前、災害タイプ、発生日、国、要請者、GLIDE番号など）
    """
    params = {}
    if countryiso3s:
        params["countryiso3s"] = countryiso3s
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    
    return await make_api_request("get_events", params)

@mcp.tool()
async def get_products(
    url: str = Field(description="EOR詳細ページのURL")
) -> List[Dict[str, Any]]:
    """
    指定されたEORの成果物（プロダクト）情報を取得します。
    
    Args:
        url: EOR詳細ページのURL
    
    Returns:
        成果物のリスト（日付、タイトル、ダウンロードURL、ファイルタイプなど）
    """
    params = {"url": url}
    return await make_api_request("get_products", params)

if __name__ == "__main__":
    # Render用の環境変数設定
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"  # Render用に0.0.0.0にバインド
    
    print(f"Starting Sentinel Asia EOR MCP Server with SSE transport...")
    print(f"Server will bind to {host}:{port}")
    
    # FastMCPのSSEアプリを取得してuvicornで直接起動
    try:
        # FastMCPの内部SSEアプリを取得
        app = mcp._create_sse_app()
        
        # uvicornで直接起動（host設定を確実に適用）
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )
    except Exception as e:
        print(f"Error starting server with direct uvicorn: {e}")
        print("Trying alternative method...")
        
        # 代替方法：環境変数を設定してからFastMCPを起動
        os.environ["HOST"] = host
        os.environ["PORT"] = str(port)
        mcp.run(transport="sse") 