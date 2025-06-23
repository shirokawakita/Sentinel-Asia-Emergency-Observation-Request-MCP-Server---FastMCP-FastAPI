# Sentinel Asia EOR MCP Server

Sentinel Asia緊急観測要請（EOR）APIのMCPサーバー実装

## 概要

このプロジェクトは、Sentinel AsiaのEOR（Emergency Observation Request）APIをModel Context Protocol (MCP)サーバーとして提供します。Render.comでホストされており、ClaudeデスクトップアプリやClaude Code、その他のMCPクライアントから災害情報を取得できます。

## デプロイされたサーバー

- **サーバーURL**: `https://sentinel-asia-emergency-observation.onrender.com`
- **SSEエンドポイント**: `https://sentinel-asia-emergency-observation.onrender.com/sse`

## セットアップ方法

### 方法1: プロキシサーバー経由（Claudeデスクトップアプリ推奨）

ClaudeデスクトップアプリはHTTP/SSEトランスポートを直接サポートしていないため、ローカルプロキシサーバーを使用します。

1. **必要なパッケージをインストール**:
   ```bash
   pip3 install fastmcp httpx pydantic
   ```

2. **Claude設定ファイルを編集**:
   - Linux: `~/.config/Claude/claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%/Claude/claude_desktop_config.json`

   以下の設定を追加：
   ```json
   {
     "mcpServers": {
       "sentinel-asia-eor": {
         "command": "python3",
         "args": [
           "/path/to/mcp_proxy_server.py"
         ],
         "env": {}
       }
     }
   }
   ```

3. **Claudeデスクトップアプリを再起動**

### 方法2: Claude Code経由

Claude CodeはSSEトランスポートをサポートしています：

```bash
claude mcp add --transport sse sentinel-asia-eor https://sentinel-asia-emergency-observation.onrender.com/sse
```

### 方法3: 他のMCPクライアント経由

Cursor、VS Code拡張機能、LibreChatなどの他のMCPクライアントでは、HTTP/SSEエンドポイントを直接使用できます：
- `https://sentinel-asia-emergency-observation.onrender.com/sse`

## 利用可能なツール

### 1. get_countries
利用可能な国のリストを取得

### 2. get_metadata  
サービスのメタデータ（説明、ライセンス、方法論）を取得

### 3. get_events
災害イベント情報を取得
- `countryiso3s`: 国コード（カンマ区切り、例：JPN,PHL,CHN）
- `start_date`: 開始日（YYYYMMDD形式）
- `end_date`: 終了日（YYYYMMDD形式）

### 4. get_products
指定されたEORの成果物情報を取得
- `url`: EOR詳細ページのURL

## 使用例

```
> 日本の最近の災害イベントを取得してください

> フィリピンと中国の2024年の災害情報を比較してください  

> 利用可能な国のリストを表示してください
```

## Renderでのデプロイ

このプロジェクトはRender.comでホストするように設定されています。

### デプロイに含まれるファイル

- `render_server.py`: Render用のメインサーバーファイル
- `requirements.txt`: Python依存関係
- `Procfile`: プロセス定義
- `start.sh`: 起動スクリプト（オプション）
- `runtime.txt`: Pythonバージョン指定

### Renderでの設定

1. GitHubリポジトリをRenderに接続
2. 以下の設定を使用：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python render_server.py`
   - **Environment**: Python 3

## API仕様

このMCPサーバーは以下の構造で動作：
- **MCPサーバー**: `https://sentinel-asia-emergency-observation.onrender.com`
  - `/sse`: SSE MCP接続エンドポイント（Claude Code等用）
  - `/health`: ヘルスチェック
- **データソースAPI**: `https://reder-test-o5k8.onrender.com`
  - `/get_countries`: 国リスト
  - `/get_metadata`: メタデータ
  - `/get_events`: イベント情報
  - `/get_products`: 成果物情報

## トラブルシューティング

### よくある問題

1. **"No module named 'fastmcp'" エラー**:
   ```bash
   pip3 install fastmcp httpx pydantic
   ```

2. **接続エラー**:
   - Renderサーバーが稼働しているか確認
   - インターネット接続を確認

3. **Claudeでツールが表示されない**:
   - Claudeデスクトップアプリを再起動
   - 設定ファイルのパスが正しいか確認

### デバッグ

プロキシサーバーのログを確認：
```bash
python3 mcp_proxy_server.py
```

## ライセンス

MIT License

## 🚀 **主な機能**

- **災害イベント検索**: 国別・日付別での災害イベント情報取得
- **国リスト取得**: アジア太平洋地域の対応国一覧
- **メタデータ取得**: サービス情報・ライセンス・注意事項
- **成果物取得**: EOR詳細ページから関連成果物情報を取得

## 🛠️ **MCPツール一覧**

### `get_countries()`
- アジア、中東、太平洋諸国の国名とISO3コードのリストを取得

### `get_metadata()`
- サービスの説明、ライセンス、方法論、注意事項を取得

### `get_events(countryiso3s?, start_date?, end_date?)`
- 災害イベント情報を取得
- **パラメータ**:
  - `countryiso3s`: カンマ区切りのISO3国コード（例：JPN,PHL,CHN）
  - `start_date`: 開始日（YYYYMMDD または YYYY-MM-DD 形式）
  - `end_date`: 終了日（YYYYMMDD または YYYY-MM-DD 形式）

### `get_products(url)`
- 指定されたEOR詳細ページから成果物情報を取得
- **パラメータ**:
  - `url`: EOR詳細ページのURL

## 🌐 **Renderでのデプロイ**

### デプロイ設定

**Build Command:**
```bash
pip install -r requirements_mcp.txt
```

**Start Command:**
```bash
python mcp_server_sse.py
```

### 環境変数
- `PORT`: Renderが自動設定（通常10000）

## 🔧 **Claude Desktopでの使用**

`claude_desktop_config.json`に以下を追加：

```json
{
  "mcpServers": {
    "sentinel-asia-eor": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch", "https://your-app.onrender.com/sse"],
      "env": {}
    }
  }
}
```

## 📚 **使用例**

### 日本の2024年災害イベントを検索
```
get_events(countryiso3s="JPN", start_date="20240101", end_date="20241231")
```

### フィリピンの最近の災害イベントを検索
```
get_events(countryiso3s="PHL", start_date="20241201")
```

### 利用可能な国一覧を取得
```
get_countries()
```

## 🔗 **関連リンク**

- [Sentinel Asia 公式サイト](https://sentinel-asia.org/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

## 📄 **ライセンス**

このプロジェクトはMITライセンスの下で公開されています。

## 🙏 **謝辞**

このプロジェクトは[Sentinel Asia](https://sentinel-asia.org/)のAPIを使用しています。災害監視・対応における貴重なデータを提供いただき、ありがとうございます。 