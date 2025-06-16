import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import time
import os
import csv

def get_available_chart_dates(year, month):
    """
    指定された年月で利用可能なチャート日付を取得する
    """
    base_url = "https://www.billboard-japan.com/charts/get_chartdays"
    url = f"{base_url}?a=hot100&year={year}&month={month:02d}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        # レスポンスからselect要素を解析して日付を抽出
        soup = BeautifulSoup(response.text, "html.parser")
        options = soup.select("option")
        dates = []
        for option in options:
            value = option.get("value")
            if value and len(value) == 8:  # YYYYMMDD形式
                dates.append(value)
        return dates
    except Exception as e:
        print(f"日付取得エラー ({year}/{month:02d}): {e}")
        return []

def get_japan_billboard_hot100(year=None, month=None, day=None, silent=False):
    """
    日本版Billboard Hot 100をスクレイピングする関数
    
    Args:
        year (int): 年 (例: 2025)
        month (int): 月 (例: 6)
        day (int): 日 (例: 9)
        silent (bool): サイレントモード（ユーザー入力をスキップ）
    """
    
    # ベースURL
    base_url = "https://www.billboard-japan.com/charts/detail?a=hot100"
    
    # 日時が指定されている場合はURLに追加
    if year and month and day:
        url = f"{base_url}&year={year}&month={month:02d}&day={day:02d}"
        if not silent:
            print(f"指定された日時のチャートを取得中: {year}/{month:02d}/{day:02d}")
    else:
        url = base_url
        if not silent:
            print("最新のチャートを取得中...")
    
    if not silent:
        print(f"URL: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'  # 日本語文字化け対策
    except requests.RequestException as e:
        if not silent:
            print(f"エラー: ページの取得に失敗しました - {e}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # サイレントモードでない場合のみユーザー入力
    if not silent:
        print("Billboard Japan Hot 100 スクレイパーへようこそ！")
        
        # ユーザー入力
        while True:
            image_data = input("画像とステータスデータを取得しますか？ (y/n): ")
            if image_data.lower() in {"yes", 'y', 'はい'}:
                image_data = True
                break
            elif image_data.lower() in {"no", 'n', 'いいえ'}:
                image_data = False
                break
            else:
                print("y または n で答えてください。")

        while True:
            print_data = input("データをコンソールに表示しますか？ (y/n): ")
            if print_data.lower() in {"yes", 'y', 'はい'}:
                print_data = True
                print("\n今週のHOT 100楽曲を表示中...")
                break
            elif print_data.lower() in {"no", 'n', 'いいえ'}:
                print_data = False
                print("\n今週のHOT 100楽曲をスクレイピング中...")
                break
            else:
                print("y または n で答えてください。")
    else:
        # サイレントモードのデフォルト設定
        image_data = True
        print_data = False

    # CSVファイル名（日時指定がある場合は含める）
    if year and month and day:
        filename = f"data/billboard_japan_hot100_{year}{month:02d}{day:02d}.csv"
    else:
        filename = "data/billboard_japan_hot100.csv"
    
    # CSVファイルを開く
    try:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            # ヘッダー行を書き込み
            headers = "Image, Status, " if image_data else ''
            headers += "Song, Artist, Last Week, Peak Position, Weeks on Chart\n"
            f.write(headers)
            
            # 日本版のHTML構造に合わせてスクレイピング
            # テーブルの行を取得（ヘッダー行を除く）
            chart_rows = soup.select("table tbody tr")
            
            if not chart_rows:
                if not silent:
                    print("チャートデータが見つかりませんでした。")
                return None
            
            songs_found = 0
            
            for i, row in enumerate(chart_rows):
                try:
                    # 順位を取得
                    rank_cell = row.select_one("td.rank_td span")
                    if not rank_cell:
                        continue
                    
                    rank = rank_cell.text.strip()
                    
                    # 楽曲名を取得
                    song_element = row.select_one("p.musuc_title")
                    if not song_element:
                        continue
                    song = song_element.text.strip()
                    
                    # アーティスト名を取得
                    artist_element = row.select_one("p.artist_name")
                    if not artist_element:
                        continue
                    # リンクがある場合はリンクテキストを、ない場合は直接テキストを取得
                    artist_link = artist_element.select_one("a")
                    if artist_link:
                        artist = artist_link.text.strip()
                    else:
                        artist = artist_element.text.strip()
                    
                    # 前回順位、最高位、チャートイン数を取得
                    times_cell = row.select_one("td.times_td")
                    weeks_on_chart = times_cell.text.strip() if times_cell else "N/A"
                    
                    # 前回順位を取得（スマホ版の情報から）
                    last_week_element = row.select_one(".rank_detail .last")
                    if last_week_element:
                        last_week_text = last_week_element.text.strip()
                        last_week = last_week_text.replace("前回：", "").strip()
                        if last_week == "-":
                            last_week = "NEW"
                    else:
                        last_week = "N/A"
                    
                    # 最高位は日本版では直接表示されていないため、現在の順位を使用
                    peak_position = rank
                    
                    # 画像とステータス情報を取得
                    image_url = "N/A"
                    status_svg = "N/A"
                    
                    if image_data:
                        # 画像URL取得
                        img_element = row.select_one("img")
                        if img_element and img_element.get("src"):
                            image_url = img_element["src"]
                            # 相対URLの場合は絶対URLに変換
                            if image_url.startswith("/"):
                                image_url = "https://www.billboard-japan.com" + image_url
                        
                        # ステータス取得（上昇/下降/維持/新規）
                        status_element = row.select_one("td.rank_td span.up, td.rank_td span.down, td.rank_td span.cont, td.rank_td span.new")
                        if status_element:
                            if "up" in status_element.get("class", []):
                                status_svg = "up"
                            elif "down" in status_element.get("class", []):
                                status_svg = "down"
                            elif "cont" in status_element.get("class", []):
                                status_svg = "right"
                            elif "new" in status_element.get("class", []):
                                status_svg = "<span>NEW</span>"
                    
                    # コンソール出力
                    if print_data:
                        print(f"\n順位: #{rank}")
                        print(f"楽曲: {song}")
                        print(f"アーティスト: {artist}")
                        print(f"前回: {last_week}")
                        print(f"最高位: {peak_position}")
                        print(f"チャートイン数: {weeks_on_chart}")
                    
                    # CSVに書き込み
                    if image_data:
                        f.write(f'"{image_url}","{status_svg}",')
                    f.write(f'"{song}","{artist}",{last_week},{peak_position},"{weeks_on_chart}"\n')
                    
                    songs_found += 1
                    
                except Exception as e:
                    if not silent:
                        print(f"行 {i+1} の処理中にエラーが発生しました: {e}")
                    continue
        
        if not silent:
            print(f"\nスクレイピング完了！")
            print(f"取得した楽曲数: {songs_found}")
            print(f"データは {filename} に保存されました")
        return filename
        
    except Exception as e:
        if not silent:
            print(f"ファイル書き込みエラー: {e}")
        return None

def get_multiple_charts(start_year, start_month, end_year, end_month, delay=2):
    """
    複数の期間のチャートを一括取得する
    
    Args:
        start_year (int): 開始年
        start_month (int): 開始月
        end_year (int): 終了年
        end_month (int): 終了月
        delay (int): リクエスト間の待機時間（秒）
    """
    
    print(f"=== 期間指定スクレイピング ===")
    print(f"期間: {start_year}/{start_month:02d} 〜 {end_year}/{end_month:02d}")
    print(f"リクエスト間隔: {delay}秒")
    print()
    
    # 結果を保存するディレクトリを作成
    output_dir = f"data/billboard_japan_charts_{start_year}{start_month:02d}_{end_year}{end_month:02d}"
    os.makedirs(output_dir, exist_ok=True)
    
    # 統合CSVファイルの準備
    combined_filename = os.path.join(output_dir, "combined_charts.csv")
    
    successful_downloads = 0
    failed_downloads = 0
    all_chart_data = []
    
    # 期間内の各月を処理
    current_year = start_year
    current_month = start_month
    
    while (current_year < end_year) or (current_year == end_year and current_month <= end_month):
        print(f"📅 {current_year}/{current_month:02d} の利用可能な日付を取得中...")
        
        # その月の利用可能な日付を取得
        available_dates = get_available_chart_dates(current_year, current_month)
        
        if not available_dates:
            print(f"   ⚠️  {current_year}/{current_month:02d} にはチャートデータがありません")
            failed_downloads += 1
        else:
            print(f"   ✅ {len(available_dates)}個のチャートが見つかりました")
            
            # 各日付のチャートを取得
            for date_str in available_dates:
                year = int(date_str[:4])
                month = int(date_str[4:6])
                day = int(date_str[6:8])
                
                print(f"   📊 {year}/{month:02d}/{day:02d} のチャートを取得中...", end=" ")
                
                try:
                    filename = get_japan_billboard_hot100(year, month, day, silent=True)
                    
                    if filename and os.path.exists(filename):
                        # ファイルを出力ディレクトリに移動
                        new_path = os.path.join(output_dir, os.path.basename(filename))
                        os.rename(filename, new_path)
                        
                        # 統合用にデータを読み込み
                        try:
                            with open(new_path, 'r', encoding='utf-8') as f:
                                reader = csv.reader(f)
                                rows = list(reader)
                                if len(rows) > 1:  # ヘッダー以外にデータがある場合
                                    # 各行に日付情報を追加
                                    for i, row in enumerate(rows):
                                        if i == 0:  # ヘッダー行
                                            row.insert(0, "Chart_Date")
                                        else:  # データ行
                                            row.insert(0, f"{year}-{month:02d}-{day:02d}")
                                    all_chart_data.extend(rows)
                        except Exception as e:
                            print(f"データ読み込みエラー: {e}")
                        
                        print("✅ 完了")
                        successful_downloads += 1
                    else:
                        print("❌ 失敗")
                        failed_downloads += 1
                        
                except Exception as e:
                    print(f"❌ エラー: {e}")
                    failed_downloads += 1
                
                # リクエスト間隔を空ける
                if delay > 0:
                    time.sleep(delay)
        
        # 次の月へ
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1
    
    # 統合CSVファイルを作成
    if all_chart_data:
        print(f"\n📝 統合CSVファイルを作成中...")
        try:
            with open(combined_filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                
                # ヘッダーを一度だけ書き込み
                if all_chart_data:
                    writer.writerow(all_chart_data[0])
                
                # データ行を書き込み（ヘッダーをスキップ）
                for i, row in enumerate(all_chart_data[1:], 1):
                    if len(row) > 1:  # 空行をスキップ
                        writer.writerow(row)
            
            print(f"   ✅ 統合ファイル作成完了: {combined_filename}")
        except Exception as e:
            print(f"   ❌ 統合ファイル作成エラー: {e}")
    
    # 結果サマリー
    print(f"\n=== スクレイピング結果 ===")
    print(f"✅ 成功: {successful_downloads}件")
    print(f"❌ 失敗: {failed_downloads}件")
    print(f"📁 出力ディレクトリ: {output_dir}")
    
    if successful_downloads > 0:
        print(f"📊 統合CSVファイル: {combined_filename}")
    
    return output_dir

def main():
    print("=== Billboard Japan Hot 100 スクレイパー ===")
    print("1. 最新のチャートを取得")
    print("2. 特定の日付のチャートを取得")
    print("3. 期間指定で複数のチャートを取得")
    
    choice = input("選択してください (1, 2, または 3): ").strip()
    
    if choice == "1":
        get_japan_billboard_hot100()
    elif choice == "2":
        try:
            year = int(input("年を入力してください (例: 2025): "))
            month = int(input("月を入力してください (例: 6): "))
            day = int(input("日を入力してください (例: 9): "))
            get_japan_billboard_hot100(year, month, day)
        except ValueError:
            print("無効な入力です。数字を入力してください。")
    elif choice == "3":
        try:
            print("\n=== 期間指定設定 ===")
            start_year = int(input("開始年を入力してください (例: 2025): "))
            start_month = int(input("開始月を入力してください (例: 1): "))
            end_year = int(input("終了年を入力してください (例: 2026): "))
            end_month = int(input("終了月を入力してください (例: 1): "))
            
            # 待機時間の設定
            print("\nリクエスト間隔を設定してください（サーバー負荷軽減のため）:")
            delay = int(input("待機時間（秒、推奨: 2-5秒）: ") or "2")
            
            # 確認
            print(f"\n設定確認:")
            print(f"期間: {start_year}/{start_month:02d} 〜 {end_year}/{end_month:02d}")
            print(f"待機時間: {delay}秒")
            
            confirm = input("この設定で実行しますか？ (y/n): ")
            if confirm.lower() in {"yes", 'y', 'はい'}:
                get_multiple_charts(start_year, start_month, end_year, end_month, delay)
            else:
                print("キャンセルしました。")
                
        except ValueError:
            print("無効な入力です。数字を入力してください。")
    else:
        print("無効な選択です。")

if __name__ == "__main__":
    main() 