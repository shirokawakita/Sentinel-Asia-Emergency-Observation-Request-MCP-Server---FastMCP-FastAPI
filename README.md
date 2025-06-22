# Sentinel Asia EOR API Server

Sentinel Asia緊急観測要請（EOR: Emergency Observation Request）APIのクラウドサーバーです。FastAPIで実装され、Renderで無料ホスティング可能です。

## 🌐 デモ

- **API Documentation**: デプロイ後 `/docs` でSwagger UIにアクセス
- **元データソース**: [Sentinel Asia EOR API](https://reder-test-o5k8.onrender.com)

## 🚀 Renderでのデプロイ

### 1. このリポジトリをフォーク
### 2. Renderアカウント作成
1. [Render](https://render.com)にサインアップ
2. "New" → "Web Service"
3. GitHubリポジトリを接続

### 3. デプロイ設定
```
Build Command: pip install -r requirements_render.txt
Start Command: python render_web_server.py
```

### 4. 環境変数
特に設定不要（PORTは自動設定）

## 📚 API エンドポイント

デプロイ完了後、以下のエンドポイントが利用可能：

- `GET /countries` - 利用可能国リスト
- `GET /metadata` - サービスメタデータ
- `GET /events` - 災害イベント検索
- `GET /products` - 成果物情報取得
- `GET /docs` - APIドキュメント（Swagger UI）

## 💻 ローカル開発

```bash
# 依存関係インストール
pip install -r requirements_render.txt

# サーバー起動
python render_web_server.py

# アクセス
http://localhost:8000/docs
```

## 🌏 対象地域

アジア・太平洋・中東地域の緊急観測要請情報を提供：
- 日本、フィリピン、中国、インド、インドネシア、イラン等
- 自然災害（地震、津波、洪水、台風等）の衛星観測データ

## 📄 ライセンス

このプロジェクトはMITライセンスです。取得されるデータはSentinel Asiaの利用規約に従います。

## 🔗 関連リンク

- [Sentinel Asia EOR API](https://github.com/shirokawakita/reder_test)
- [Sentinel Asia 公式サイト](https://sentinel.tksc.jaxa.jp/)

---

**注意**: 無料プランでは15分で自動スリープします。本格利用には有料プランを推奨します。 