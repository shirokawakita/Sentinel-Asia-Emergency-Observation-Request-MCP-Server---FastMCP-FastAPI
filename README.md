# Sentinel Asia Emergency Observation Request MCP Server

**Sentinel Asia緊急観測要請（EOR）APIのModel Context Protocol（MCP）サーバー**

このプロジェクトは、[Sentinel Asia](https://sentinel-asia.org/)の緊急観測要請（Emergency Observation Request, EOR）APIをModel Context Protocol (MCP)経由でアクセスできるようにするサーバーです。

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