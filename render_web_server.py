#!/usr/bin/env python3
"""
Sentinel Asia EOR API Web Server for Render
MCPの機能をRESTful APIとして提供するWebサーバー
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn
import os
from typing import Dict, List, Optional, Any
from pydantic import BaseModel

# API設定
API_BASE_URL = "https://reder-test-o5k8.onrender.com"

# FastAPIアプリの初期化
app = FastAPI(
    title="Sentinel Asia EOR API Server",
    description="Sentinel Asia緊急観測要請（EOR）APIのWebサーバー",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            raise HTTPException(
                status_code=e.response.status_code,
                detail=error_messages.get(e.response.status_code, '不明なエラー')
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"リクエストエラー: {str(e)}")

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "Sentinel Asia EOR API Server",
        "version": "1.0.0",
        "documentation": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {"status": "healthy", "service": "Sentinel Asia EOR API Server"}

@app.get("/countries")
async def get_countries():
    """
    利用可能な国リストを取得します。
    アジア、中東、太平洋諸国の国名とISO3コードを返します。
    """
    try:
        return await make_api_request("get_countries")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metadata")
async def get_metadata():
    """
    サービスのメタデータを取得します。
    """
    try:
        return await make_api_request("get_metadata")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events")
async def get_events(
    countryiso3s: Optional[str] = Query(None, description="カンマ区切りのISO3国コード（例：JPN,PHL,CHN）"),
    start_date: Optional[str] = Query(None, description="開始日（YYYYMMDD または YYYY-MM-DD 形式）"),
    end_date: Optional[str] = Query(None, description="終了日（YYYYMMDD または YYYY-MM-DD 形式）")
):
    """
    災害イベント（EOR）情報を取得します。
    """
    try:
        params = {}
        if countryiso3s:
            params["countryiso3s"] = countryiso3s
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        return await make_api_request("get_events", params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products")
async def get_products(
    url: str = Query(..., description="EOR詳細ページのURL")
):
    """
    指定されたEORの成果物（プロダクト）情報を取得します。
    """
    try:
        params = {"url": url}
        return await make_api_request("get_products", params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Renderの環境変数からポートを取得（デフォルトは8000）
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 