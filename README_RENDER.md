# Sentinel Asia EOR MCP Server - Render Deployment

このドキュメントでは、Renderの無料プランでSentinel Asia EOR MCPサーバーをデプロイする方法を説明します。

## Renderでのデプロイ手順

### 1. GitHub リポジトリ作成

1. GitHubで新しいリポジトリを作成
2. 以下のファイルをプッシュ：
   - `mcp_server_http.py`
   - `requirements_render.txt`
   - `runtime.txt`
   - このREADME

### 2. Render設定

1. [Render](https://render.com)にサインアップ/ログイン
2. **New** → **Web Service** を選択
3. GitHubリポジトリを接続
4. 以下の設定を入力：

#### Basic Settings
- **Name**: `sentinel-asia-mcp-server`（任意）
- **Runtime**: `Python 3`
- **Region**: `Oregon (US West)`（無料プランの場合）
- **Branch**: `main`

#### Build & Deploy Settings
- **Build Command**: `pip install -r requirements_render.txt`
- **Start Command**: `python mcp_server_http.py`

#### Environment Variables
- 特に設定不要（デフォルトで `PORT` 環境変数が提供される）

### 3. デプロイ確認

デプロイが完了すると、RenderからURL（例：`https://sentinel-asia-mcp-server.onrender.com`）が提供されます。

## Claude設定（Renderホスト版）

Renderでホストした場合のMCP設定は異なります：

```json
{
  "mcpServers": {
    "sentinel-asia-eor-remote": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch", "https://your-render-url.onrender.com"],
      "env": {}
    }
  }
}
```

## 注意事項

### Renderの無料プランの制限

1. **スリープ**: 15分間非アクティブでスリープ状態になります
2. **コールドスタート**: スリープから復帰時に数秒かかります
3. **月間実行時間**: 750時間/月の制限があります
4. **メモリ**: 512MBのメモリ制限があります

### 推奨事項

- 本格的な利用には有料プランを検討してください
- APIレスポンス時間が重要な場合は、ローカル実行を推奨します
- 開発・テスト目的での利用に適しています

## トラブルシューティング

### デプロイエラー

1. **依存関係エラー**: `requirements_render.txt`の内容を確認
2. **ポートエラー**: `PORT`環境変数がRenderから自動設定されることを確認
3. **タイムアウト**: 初回デプロイは時間がかかる場合があります

### 動作確認

デプロイされたサービスが正常に動作するか確認：

```bash
curl https://your-render-url.onrender.com/health
```

## ローカル開発との比較

| 機能 | ローカル | Render無料 | Render有料 |
|------|----------|------------|------------|
| レスポンス時間 | 最速 | 遅い（コールドスタート） | 普通 |
| 可用性 | 不安定 | 制限あり | 高い |
| 設定の簡単さ | 複雑 | やや簡単 | やや簡単 |
| コスト | 無料 | 無料 | 有料 |

## 更新・メンテナンス

1. コードを更新したらGitHubにプッシュ
2. Renderが自動的に再デプロイを実行
3. デプロイ状況はRenderダッシュボードで確認可能 