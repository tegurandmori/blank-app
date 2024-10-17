import streamlit as st
import pandas as pd

st.title("e-football Nakayoshilab league")

players = ["まつか","くま","がい","さとか","やまし","morning","鬼","teguramori","はまじ","おじ","zkonma","king","ざき","いと"]

# 初期化
if 'team_data' not in st.session_state:
    st.session_state['team_data'] = {'team_j1': [], 'team_j2': [], 'team_j3': []}
if 'result_data' not in st.session_state:
    columns = ["Matches", "Goal difference", "Points"]
    st.session_state['result_data'] = pd.DataFrame(0, index=players, columns=columns)

# チーム選択
team_j1 = st.multiselect('Select players for Team J1:', players, default=st.session_state['team_data']['team_j1'])
team_j2 = st.multiselect('Select players for Team J2:', players, default=st.session_state['team_data']['team_j2'])
team_j3 = st.multiselect('Select players for Team J3:', players, default=st.session_state['team_data']['team_j3'])

if st.button('Save Teams'):
    st.session_state['team_data'] = {"team_j1": team_j1, "team_j2": team_j2, "team_j3": team_j3}
    st.success('Teams saved!')

# 試合の記録
league = st.selectbox("あなたの所属リーグを教えてください", ["j1", "j2", "j3"])
team = st.session_state['team_data']
name = st.selectbox("あなたの名前を教えてください", team["team_" + league])
enemy = st.selectbox("相手の名前を教えてください", team["team_" + league])
point = st.number_input("何点得点しましたか？？", value=0)
depoint = st.number_input("何点失点しましたか？？", value=0)

if st.button('試合を記録する'):
    result_data = st.session_state['result_data']
    result_data["Matches"][name] += 1
    result_data["Matches"][enemy] += 1
    result_data["Goal difference"][name] += (point - depoint)
    result_data["Goal difference"][enemy] += (depoint - point)
    if (point - depoint) > 0:
        result_data["Points"][name] += 3
    elif (point - depoint) < 0:
        result_data["Points"][enemy] += 3
    elif (point - depoint) == 0:
        result_data["Points"][name] += 1
        result_data["Points"][enemy] += 1
    st.session_state['result_data'] = result_data
    st.success('Match recorded!')

# 結果の表示
j1, j2, j3 = st.columns(3)
df_j1 = st.session_state['result_data'][st.session_state['result_data'].index.isin(team_j1)]
df_j2 = st.session_state['result_data'][st.session_state['result_data'].index.isin(team_j2)]
df_j3 = st.session_state['result_data'][st.session_state['result_data'].index.isin(team_j3)]

with j1:
    st.header("J1 league")
    st.dataframe(df_j1)
with j2:
    st.header("J2 league")
    st.dataframe(df_j2)
with j3:
    st.header("J3 league")
    st.dataframe(df_j3)


# リセットボタン
if st.button('Reset All Data'):
    st.session_state['team_data'] = {'team_j1': [], 'team_j2': [], 'team_j3': []}
    st.session_state['result_data'] = pd.DataFrame(0, index=players, columns=columns)
    st.success('All data has been reset!')
