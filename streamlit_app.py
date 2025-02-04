import streamlit as st
import pandas as pd
import sqlite3

# SQLiteデータベースに接続（なければ自動作成されます）
conn = sqlite3.connect('lab_league.db')
c = conn.cursor()

# プレイヤーリスト
players = ["まつか", "くま", "がい", "さとか", "やまし", "morning", "鬼", "teguramori", "はまじ", "おじ", "zkonma", "king", "ざき", "いと"]

# チームテーブルが存在しない場合は作成(team)
c.execute('''CREATE TABLE IF NOT EXISTS teams (
    player TEXT,
    team TEXT
)''')

# 結果テーブルが存在しない場合は作成(result)
c.execute('''CREATE TABLE IF NOT EXISTS results (
    player TEXT,
    matches INTEGER,
    goal_difference INTEGER,
    points INTEGER
)''')

# 結果データの初期化（初回のみ）
for player in players:
    c.execute('INSERT OR IGNORE INTO results (player, matches, goal_difference, points) VALUES (?, 0, 0, 0)', (player,))
conn.commit()

# チームデータの読み込み
team_j1 = [row[0] for row in c.execute("SELECT player FROM teams WHERE team='j1'").fetchall()]
team_j2 = [row[0] for row in c.execute("SELECT player FROM teams WHERE team='j2'").fetchall()]
team_j3 = [row[0] for row in c.execute("SELECT player FROM teams WHERE team='j3'").fetchall()]

st.title("Lab league")

# チーム選択
team_j1 = st.multiselect('Select players for Team J1:', players, default=team_j1)
team_j2 = st.multiselect('Select players for Team J2:', players, default=team_j2)
team_j3 = st.multiselect('Select players for Team J3:', players, default=team_j3)

if st.button('チームを保存'):
    # チームデータを保存
    c.execute("DELETE FROM teams")  # 既存のチームデータを削除
    for player in team_j1:
        c.execute("INSERT INTO teams (player, team) VALUES (?, 'j1')", (player,))
    for player in team_j2:
        c.execute("INSERT INTO teams (player, team) VALUES (?, 'j2')", (player,))
    for player in team_j3:
        c.execute("INSERT INTO teams (player, team) VALUES (?, 'j3')", (player,))
    conn.commit()
    st.success('チームが保存されました！')

# 結果データの読み込み
df = pd.read_sql_query("SELECT * FROM results", conn, index_col="player")


# 試合の記録
league = st.selectbox("あなたの所属リーグを教えてください", ["j1", "j2", "j3"])
team = {"team_j1": team_j1, "team_j2": team_j2, "team_j3": team_j3}
name = st.selectbox("あなたの名前を教えてください", team["team_" + league])
enemy = st.selectbox("相手の名前を教えてください", team["team_" + league])
point = st.number_input("何点得点しましたか？？", value=0)
depoint = st.number_input("何点失点しましたか？？", value=0)

df = df[0:len(players)]
print(df)

if st.button('試合を記録する'):
    try:
        # データを更新する前に、選手がデータフレームに存在するか確認
        if name not in df.index or enemy not in df.index:
            st.error("選択された選手がデータベースに存在しません。")
        else:
            # 試合の結果を記録
            df.at[name, "matches"] += 1
            df.at[enemy, "matches"] += 1
            df.at[name, "goal_difference"] += (point - depoint)
            df.at[enemy, "goal_difference"] += (depoint - point)

            if (point - depoint) > 0:
                df.at[name, "points"] += 3
            elif (point - depoint) < 0:
                df.at[enemy, "points"] += 3
            else:
                df.at[name, "points"] += 1
                df.at[enemy, "points"] += 1

            # データベースに保存
            with conn:
                # データを更新する前に型を確認・変換
                for player in players:
                    matches = int(df.at[player, "matches"])
                    goal_difference = int(df.at[player, "goal_difference"])
                    points = int(df.at[player, "points"])

                    c.execute("UPDATE results SET matches=?, goal_difference=?, points=? WHERE player=?",
                            (matches, goal_difference, points, player))

            st.success('試合が記録されました！')

    except sqlite3.Error as e:
        st.error(f"SQLiteエラー: {e}")
    except KeyError as e:
        st.error(f"KeyError: {e}. プレイヤー名を確認してください。")

# 各リーグの結果表示
df_j1 = df[df.index.isin(team_j1)].astype(str)  # データ型を明示的に文字列に変換
df_j2 = df[df.index.isin(team_j2)].astype(str)
df_j3 = df[df.index.isin(team_j3)].astype(str)
df_j1 = df_j1.sort_values(["points","goal_difference"], ascending=False)
df_j2 = df_j2.sort_values(["points","goal_difference"], ascending=False)
df_j3 = df_j3.sort_values(["points","goal_difference"], ascending=False)

league_list = {"j1":0,"j2":1,"j3":2}

#j1, j2, j3 = st.columns(3)


st.header("J1 league")
st.dataframe(df_j1)


st.header("J2 league")
st.dataframe(df_j2)


st.header("J3 league")
st.dataframe(df_j3)

# リセットボタン
if st.button('データをリセット'):
    c.execute("DELETE FROM teams")  # チームデータを削除
    c.execute("DELETE FROM results")  # 結果データを削除
    for player in players:
        c.execute('INSERT INTO results (player, matches, goal_difference, points) VALUES (?, 0, 0, 0)', (player,))
    conn.commit()
    st.success('すべてのデータがリセットされました！')

# SQLite接続を閉じる
conn.close()
