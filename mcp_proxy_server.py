#!/usr/bin/env python3
"""
MCP Proxy Server for Sentinel Asia API
RenderでホストされているAPIにアクセスするためのstdio MCPプロキシサーバー
"""

import asyncio
import httpx
import sys
from typing import Dict, List, Optional, Any
from fastmcp import FastMCP
from pydantic import BaseModel, Field

# API設定
API_BASE_URL = "https://reder-test-o5k8.onrender.com"

# MCPサーバーの初期化
mcp = FastMCP("Sentinel Asia EOR API Proxy Server")

async def make_api_request(
    endpoint: str, 
    params: Optional[Dict[str, str]] = None
) -> Any:
    """RenderのAPIにリクエストを送信する関数"""
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
    # デバッグ出力
    print("Starting Sentinel Asia EOR MCP Proxy Server...", file=sys.stderr)
    
    try:
        # stdio transport でMCPサーバーを起動
        mcp.run()
    except Exception as e:
        print(f"Error starting MCP proxy server: {e}", file=sys.stderr)
        sys.exit(1) 