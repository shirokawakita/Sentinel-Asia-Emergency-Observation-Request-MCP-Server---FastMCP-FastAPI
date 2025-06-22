# Sentinel Asia EOR MCP Server

Sentinel Asia緊急観測要請（EOR: Emergency Observation Request）の**真のMCPサーバー**です。FastMCPを使用してSSE（Server-Sent Events）トランスポートで実装されており、Claude DesktopからMCPプロトコル経由で直接アクセス可能です。

## 🌐 MCPサーバー

- **プロトコル**: MCP over SSE（Server-Sent Events）
- **元データソース**: [Sentinel Asia EOR API](https://reder-test-o5k8.onrender.com)
- **Claude連携**: 直接MCP接続可能

## 🚀 Renderでのデプロイ

### 1. このリポジトリをフォーク
### 2. Renderアカウント作成
1. [Render](https://render.com)にサインアップ
2. "New" → "Web Service"
3. GitHubリポジトリを接続

### 3. デプロイ設定（MCP版）
```
Build Command: pip install -r requirements_mcp.txt
Start Command: python mcp_server_sse.py
```

### 4. 環境変数
特に設定不要（PORTは自動設定）

## 🔧 Claude Desktop設定

デプロイ完了後、ClaudeのMCP設定に追加：

```json
{
  "mcpServers": {
    "sentinel-asia-eor": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch", "https://your-app.onrender.com"],
      "env": {}
    }
  }
}
```

**your-app.onrender.com** を実際のRender URLに置き換えてください。

## 🛠️ 利用可能なMCPツール

Claude Desktopから以下のツールが利用可能：

- **`get_countries`** - 利用可能国リスト取得
- **`get_metadata`** - サービスメタデータ取得  
- **`get_events`** - 災害イベント検索・フィルタリング
- **`get_products`** - 成果物情報取得

### ツール使用例

```
# Claude Desktop内で直接利用
"日本の2024年の災害イベントを検索して"
→ get_events(countryiso3s="JPN", start_date="20240101") が実行

"利用可能な国を教えて"  
→ get_countries() が実行
```

## 💻 ローカル開発

```bash
# 依存関係インストール
pip install -r requirements_mcp.txt

# MCPサーバー起動（stdio）
python mcp_server_sse.py

# テスト（別ターミナル）
npx @modelcontextprotocol/inspector
```

## 🌏 対象地域

アジア・太平洋・中東地域の緊急観測要請情報：
- 日本、フィリピン、中国、インド、インドネシア、イラン等
- 自然災害（地震、津波、洪水、台風等）の衛星観測データ
- 各EORの詳細情報とKMZファイルアクセス

## 🔄 MCPプロトコルの利点

- **自動ツール認識**: Claudeが自動的にツールを理解
- **型安全**: Pydanticベースの厳密な型チェック
- **非同期処理**: 高速なAPI呼び出し
- **エラーハンドリング**: 適切なエラー処理とメッセージ

## 📄 ライセンス

このプロジェクトはMITライセンスです。取得されるデータはSentinel Asiaの利用規約に従います。

## 🔗 関連リンク

- [Sentinel Asia EOR API](https://github.com/shirokawakita/reder_test)
- [Sentinel Asia 公式サイト](https://sentinel.tksc.jaxa.jp/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)

---

**注意**: 
- 無料プランでは15分で自動スリープします
- 本格利用には有料プランを推奨
- MCPサーバーの初回起動時はコールドスタートにより数秒かかります 