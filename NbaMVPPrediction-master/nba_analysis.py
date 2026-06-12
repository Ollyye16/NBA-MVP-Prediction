import requests
import pyodbc
from bs4 import BeautifulSoup
from flask import Flask, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

# 設置字體
font = FontProperties(fname=r"C:\Windows\Fonts\msjh.ttc", size=12)  # 替換成 "Microsoft JhengHei" 字體的路徑
plt.rcParams['font.family'] = font.get_name()

# 調整圖表大小
plt.figure(figsize=(10, 6))  # 設定圖表的寬度和高度，根據需要進行調整

url = "http://www.espn.com/nba/history/awards/_/id/33"
response = requests.get(url)
html_content = response.content

app = Flask(__name__)

# SQL Server 連接設定
server = '223.138.134.15.database.windows.net'
database = 'MVP'
username = 'youyou'
password = '123456'
driver = '{ODBC Driver 17 for SQL Server}'

# 設定資料庫連接
conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
conn = pyodbc.connect(conn_str)

soup = BeautifulSoup(html_content, "html.parser")

table = soup.find("table", class_="tablehead")
rows = table.find_all("tr")[3:26]  # 提取第 2022 到 2000 的資料

for row in rows:
    cells = row.find_all("td")
    year = cells[0].text.strip()
    player = cells[1].text.strip()
    position = cells[2].text.strip()
    team = cells[3].text.strip()
    fg_percentage = cells[4].text.strip()
    ppg = cells[5].text.strip()
    rpg = cells[6].text.strip()
    apg = cells[7].text.strip()
    blkpg = cells[8].text.strip()

    print("年份:", year)
    print("球員:", player)
    print("位置:", position)
    print("球隊:", team)
    print("命中率:", fg_percentage)
    print("場均得分:", ppg)
    print("場均籃板:", rpg)
    print("場均助攻:", apg)
    print("場均阻攻:", blkpg)
    print("---")

# 建立與資料庫的連接
cursor = conn.cursor()

# 創建表格（如果需要）
create_table_query = '''
CREATE TABLE IF NOT EXISTS player_data (
    year INT,
    player TEXT,
    position TEXT,
    team TEXT,
    fg_percentage TEXT,
    ppg TEXT,
    rpg TEXT,
    apg TEXT,
    blkpg TEXT
)
'''
cursor.execute(create_table_query)
conn.commit()

# 插入數據
insert_query = '''
INSERT INTO player_data (year, player, position, team, fg_percentage, ppg, rpg, apg, blkpg)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
'''

for row in rows:
    cells = row.find_all("td")
    year = cells[0].text.strip()
    player = cells[1].text.strip()
    position = cells[2].text.strip()
    team = cells[3].text.strip()
    fg_percentage = cells[4].text.strip()
    ppg = cells[5].text.strip()
    rpg = cells[6].text.strip()
    apg = cells[7].text.strip()
    blkpg = cells[8].text.strip()

    # 執行插入數據的操作
    cursor.execute(insert_query, (year, player, position, team, fg_percentage, ppg, rpg, apg, blkpg))
    conn.commit()

# 關閉連接
conn.close()

print("數據存儲完成。")

# 定義 API 路由
@app.route('/api/players', methods=['GET'])
def get_players():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM player_data')
    players = cursor.fetchall()
    player_list = []
    for player in players:
        player_dict = {
            '年份': player[0],
            '球員': player[1],
            '位置': player[2],
            '球隊': player[3],
            '命中率': player[4],
            '場均得分': player[5],
            '場均籃板': player[6],
            '場均助攻': player[7],
            '場均阻攻': player[8]
        }
        player_list.append(player_dict)
    conn.close()
    return jsonify(player_list)

# 定義 API 路由，返回數據分析結果
@app.route('/api/analysis', methods=['GET'])
def get_analysis():
    conn = pyodbc.connect(conn_str)
    df = pd.read_sql_query('SELECT * FROM player_data', conn)
    conn.close()

    # 數據分析命中率:
    sns.lmplot(data=df, x='year', y='fg_percentage', lowess=True)
    plt.title('命中率與歷年MVP之間的關係', fontproperties=font)
    plt.xlabel('年份', fontproperties=font)
    plt.ylabel('命中率', fontproperties=font)
    plt.show()
    
    # 數據分析場均得分:
    sns.lmplot(data=df, x='year', y='ppg', lowess=True)
    plt.title('場均得分與歷年MVP之間的關係', fontproperties=font)
    plt.xlabel('年份', fontproperties=font)
    plt.ylabel('場均得分', fontproperties=font)
    plt.show()
    
    # 數據分析場均籃板:
    sns.lmplot(data=df, x='year', y='rpg', lowess=True)
    plt.title('場均籃板與歷年MVP之間的關係', fontproperties=font)
    plt.xlabel('年份', fontproperties=font)
    plt.ylabel('場均籃板', fontproperties=font)
    plt.show()
    
    # 數據分析場均助攻:
    sns.lmplot(data=df, x='year', y='apg', lowess=True)
    plt.title('場均助攻與歷年MVP之間的關係', fontproperties=font)
    plt.xlabel('年份', fontproperties=font)
    plt.ylabel('場均助攻', fontproperties=font)
    plt.show()
    
    # 數據分析場均阻攻:
    sns.lmplot(data=df, x='year', y='blkpg', lowess=True)
    plt.title('場均阻攻與歷年MVP之間的關係', fontproperties=font)
    plt.xlabel('年份', fontproperties=font)
    plt.ylabel('場均阻攻', fontproperties=font)
    plt.show()

    return "數據分析完成。"

if __name__ == '__main__':
    app.run()
