# Billboard Japan Hot 100 Web Scraper 🎵

![Billboard Japan Logo](https://imgur.com/a/MQVdcKI)

**Billboard Japan Hot 100**をスクレイピングして、楽曲チャートデータをCSVファイルに保存するPythonアプリケーションです。

## 🌟 特徴

- 📊 Billboard Japan Hot 100の最新チャートを取得
- 📅 特定の日付のチャートデータを取得可能
- 🖼️ アルバムアート画像とランキング変動ステータスの取得
- 📁 CSV形式でのデータ保存
- 🇯🇵 日本語完全対応

## 📋 取得データ項目

- 🖼️ アルバムアート画像URL
- 📈 ランキング変動ステータス（上昇/下降/維持/新規）
- 🎵 楽曲名
- 👤 アーティスト名
- 📊 前回順位
- 🏆 最高位
- 📅 チャートイン週数

## 🚀 使い方

### 1. 環境準備

```bash
# 必要なライブラリをインストール
pip install requests beautifulsoup4
```

### 2. スクレイピング実行

```bash
# 日本版スクレイパーを実行
python web_scraper_japan.py
```

実行すると以下の選択肢が表示されます：

```
=== Billboard Japan Hot 100 スクレイパー ===
1. 最新のチャートを取得
2. 特定の日付のチャートを取得
3. 期間指定で複数のチャートを取得
選択してください (1, 2, または 3):
```

#### 最新チャートの取得
```
1
画像とステータスデータを取得しますか？ (y/n): y
データをコンソールに表示しますか？ (y/n): y
```

#### 特定日付のチャート取得
```
2
年を入力してください (例: 2025): 2025
月を入力してください (例: 6): 6
日を入力してください (例: 9): 9
```

#### 期間指定で複数取得
```
3
開始年を入力してください (例: 2025): 2025
開始月を入力してください (例: 1): 1
終了年を入力してください (例: 2026): 2026
終了月を入力してください (例: 1): 1
待機時間（秒、推奨: 2-5秒）: 2
```

### 3. データの確認

#### 生成されるファイル

- **最新チャート**: `data/billboard_japan_hot100.csv`
- **特定日付**: `data/billboard_japan_hot100_YYYYMMDD.csv`
- **期間指定**: `data/billboard_japan_charts_YYYYMM_YYYYMM/` フォルダに保存

## 📊 CSVファイル形式

```csv
Image, Status, Song, Artist, Last Week, Peak Position, Weeks on Chart
"https://example.com/image.jpg","up","楽曲名","アーティスト名","5","1","10"
```

## 🔧 URL形式について

### 基本URL
```
https://www.billboard-japan.com/charts/detail?a=hot100
```

### 日付指定URL
```
https://www.billboard-japan.com/charts/detail?a=hot100&year=2025&month=06&day=09
```

## 📁 ファイル構成

```
billboard-hot-100-web-scraper/
├── web_scraper_japan.py      # 日本版スクレイパー
├── README_japan.md           # 日本版説明書
├── README.md                 # メイン説明書
├── LICENSE                   # ライセンスファイル
└── data/                     # データフォルダ
    ├── billboard_japan_hot100.csv
    ├── billboard_japan_hot100_YYYYMMDD.csv
    └── billboard_japan_charts_YYYYMM_YYYYMM/
        ├── billboard_japan_hot100_YYYYMMDD.csv
        └── combined_charts.csv
```

## 🆚 米国版との違い

| 項目 | 米国版 | 日本版 |
|------|--------|--------|
| **URL** | `billboard.com/charts/hot-100/` | `billboard-japan.com/charts/detail?a=hot100` |
| **HTML構造** | `ul.o-chart-results-list-row` | `table tbody tr` |
| **楽曲名取得** | `h3.c-title` | `p.musuc_title` |
| **アーティスト名** | `span.a-no-trucate` | `p.artist_name` |
| **日付指定** | URLパス形式 | クエリパラメータ形式 |
| **文字エンコーディング** | UTF-8 | UTF-8（日本語対応） |

## 🎯 使用例

### 最新チャートの取得
```python
from web_scraper_japan import get_japan_billboard_hot100

# 最新チャートを取得
get_japan_billboard_hot100()
```

### 特定日付のチャート取得
```python
# 2025年6月9日のチャートを取得
get_japan_billboard_hot100(2025, 6, 9)
```

## ⚠️ 注意事項

- スクレイピングは適切な間隔で実行してください
- サイトの利用規約を遵守してください
- 大量のリクエストはサーバーに負荷をかける可能性があります
- 商用利用の場合は事前に許可を取得してください

## 🐛 トラブルシューティング

### よくある問題

1. **文字化けが発生する**
   ```python
   response.encoding = 'utf-8'  # 既に対応済み
   ```

2. **データが取得できない**
   - サイトのHTML構造が変更された可能性があります
   - ネットワーク接続を確認してください

3. **画像が表示されない**
   - CSVファイルを直接開いて確認してください
   - 画像URLが有効か確認してください

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照

## 🤝 貢献

プルリクエストやイシューの報告を歓迎します！

## 📖 その他のドキュメント

- **[English README](README.md)** | 🇺🇸 **英語版ドキュメント**

---

**注意**: このツールは教育目的で作成されています。Billboard Japanの利用規約を遵守してご利用ください。 