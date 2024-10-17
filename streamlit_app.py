import streamlit as st
import pandas as pd
import os


csv_file = "test.csv"
result_file = "result.csv"

st.title("e-football Nakayoshilab league")

players = ["まつか","くま","がい","さとか","やまし","morning","鬼","teguramori","はまじ","おじ","zkonma","king","ざき","いと"]

if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    team_j1 = df[df['team'] == 'j1']['player'].tolist()
    team_j2 = df[df['team'] == 'j2']['player'].tolist()
    team_j3 = df[df['team'] == 'j3']['player'].tolist()
else:
    team_j1, team_j2, team_j3 = [], [], []

team = {}

team_j1 = st.multiselect('Select players for Team J1:', players, default=team_j1)
team_j2 = st.multiselect('Select players for Team J2:', players, default=team_j2)
team_j3 = st.multiselect('Select players for Team J3:', players, default=team_j3)

team["team_j1"] = team_j1
team["team_j2"] = team_j2
team["team_j3"] = team_j3

if st.button('Save Teams'):
    team_data = {'player': team_j1 + team_j2 + team_j3,
                 'team': ['j1']*len(team_j1) + ['j2']*len(team_j2) + ['j3']*len(team_j3)}
    df = pd.DataFrame(team_data)
    df.to_csv(csv_file, index=False)
    st.success('Teams saved!')


j1, j2, j3 = st.columns(3)

if os.path.exists(result_file):
    df = pd.read_csv(result_file)
    df = df.set_index("Unnamed: 0")
else:
    columns = ["Matches","Goal difference","Points"]
    df = pd.DataFrame(0, index=players, columns = columns)


league = st.selectbox("あなたの所属リーグを教えてください",["j1","j2","j3"])
list = ("team_" + str(league))
name = st.selectbox("あなたの名前を教えてください",team[list])
enemy = st.selectbox("相手の名前を教えてください",team[list])
point = st.number_input("何点得点しましたか？？", value=0)
depoint = st.number_input("何点失点しましたか？？", value=0)

if st.button('試合を記録する'):
    df["Matches"][name] += 1
    df["Matches"][enemy] += 1
    df["Goal difference"][name] += (point - depoint)
    df["Goal difference"][enemy] += (depoint - point)
    if (point - depoint) > 0:
        df["Points"][name] += 3
    elif (point - depoint) < 0:
        df["Points"][name] += 3
    elif (point - depoint) == 0:
        df["Points"][name] += 1
        df["Points"][enemy] += 1
    else:
        st.erro("Error")

    print(df)
    df.to_csv(result_file, index=True)
    st.success('matches saved!')

df_j1 = df[df.index.isin(team_j1)]
df_j2 = df[df.index.isin(team_j2)]
df_j3 = df[df.index.isin(team_j3)]

with j1:
    st.header("J1 league")
    st.write("This is J1 league")
    st.dataframe(df_j1)


    #st.write(f'You selected: {selected_option}')

with j2:
    st.header("J2 league")
    st.write("This is J2 league")
    st.dataframe(df_j2)
    #st.write("The team are:",j1_list)
    #st.write(f'You selected: {selected_option}')

with j3:
    st.header("J3 league")
    st.write("This is J3 league")
    st.dataframe(df_j3)
    #st.write("The team are:",j1_list)
    #st.write(f'You selected: {selected_option}')

