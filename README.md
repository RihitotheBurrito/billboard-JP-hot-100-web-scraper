# Billboard JAPAN Hot 100 Web Scraper  
![Billboard Logo](https://i.imgur.com/DohqNsv.jpeg)

📖 **[日本語版README](README_japan.md)** | 🇯🇵 **Japanese Documentation**

## Credits
This project is based on [billboard-hot-100-web-scraper](https://github.com/jsubroto/billboard-hot-100-web-scraper) by Jaimes Subroto.

**Original work:** Copyright (c) 2018 Jaimes Subroto  
**Modified work:** Copyright (c) 2025 RihitotheBurrito

## Description

Python application which web scrapes **Billboard Japan Hot 100** using **BeautifulSoup**. 

The web scraped song informations are stored to CSV files in the `data/` folder.

    filename = 'data/billboard_japan_hot100.csv'

## Features Added

- 🇯🇵 **Japanese Billboard Hot 100 support** - Added `web_scraper_japan.py` for Billboard Japan
- 📁 **Data organization** - All CSV files are stored in the `data/` folder
- 📅 **Date-specific charts** - Ability to scrape charts from specific dates
- 🗂️ **Bulk downloading** - Download multiple charts from a date range
- 🇯🇵 **Japanese language support** - Full support for Japanese characters and interface

## Usage

### 1. Install Requirements

```bash
pip install requests beautifulsoup4
```

### 2. Run the Scraper

```bash
python web_scraper_japan.py
```

The scraper will present you with options:

```
=== Billboard Japan Hot 100 スクレイパー ===
1. 最新のチャートを取得
2. 特定の日付のチャートを取得
3. 期間指定で複数のチャートを取得
選択してください (1, 2, または 3):
```

#### Latest Chart
```
1
画像とステータスデータを取得しますか？ (y/n): y
データをコンソールに表示しますか？ (y/n): y
```

#### Specific Date Chart
```
2
年を入力してください (例: 2025): 2025
月を入力してください (例: 6): 6
日を入力してください (例: 9): 9
```

#### Bulk Download
```
3
開始年を入力してください (例: 2025): 2025
開始月を入力してください (例: 1): 1
終了年を入力してください (例: 2026): 2026
終了月を入力してください (例: 1): 1
待機時間（秒、推奨: 2-5秒）: 2
```

## Output Files

### Generated CSV headers:
- Image URL
- Status SVG (up/down/right/new)
- Song name
- Artist name
- Last week position
- Peak position
- Weeks on chart

### File Structure:
```
data/
├── billboard_japan_hot100.csv                    # Latest chart
├── billboard_japan_hot100_YYYYMMDD.csv          # Specific date charts
└── billboard_japan_charts_YYYYMM_YYYYMM/        # Bulk download results
    ├── billboard_japan_hot100_YYYYMMDD.csv
    ├── billboard_japan_hot100_YYYYMMDD.csv
    └── combined_charts.csv                       # All charts combined
```

## License

MIT License - see [LICENSE](LICENSE) for full details.

## Original Repository

https://github.com/jsubroto/billboard-hot-100-web-scraper
