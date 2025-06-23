#!/bin/bash

# Render用の起動スクリプト
echo "Starting Sentinel Asia EOR MCP Server..."

# 環境変数を設定
export PYTHONPATH="${PYTHONPATH}:."

# PythonのMCPサーバーを起動
python render_server.py 