import numpy as np
import pandas as pd
import time



#-----------------------#
#     Main Function     #
#-----------------------#

# @param: None
# @return: None
def main():
    startTime = time.time()

    # Load .csv
    season = pd.read_csv('../../data/team_season_all.csv')
    playoff = pd.read_csv('../../data/team_playoff_all.csv')

    # Merge seasona and playoff
    df_all = pd.concat([season, playoff], ignore_index=True)

    # Remove NaN
    df_all = cleanDataFrame(df_all)
    df_all = dropNanScore(df_all)

    # Add opponent label
    df_all = addOpponentCol(df_all)

    # Binary encode W/L and Home/Away
    df_all['W/L'] = df_all['W/L'].map({'W':1, 'L':0})
    df_all['Home/Away'] = df_all['Home/Away'].map({'Home':1, 'Away':0})

    # Pair teams and opponents
    df_team, df_oppo, invalid_idx = pairGamePlayers(df_all)

    # Check games' validity
    df_team, df_oppo, invalid_idx = checkGameValidity(df_team, df_oppo)

    # Rename column: Attributes_A and Attributes_B for team and opponent, respectively
    df_team = df_team.rename(columns=lambda x: x + '_A')
    df_oppo = df_oppo.rename(columns=lambda x: x + '_B')

    # Concatenate by column
    df_output = pd.concat([df_team, df_oppo], axis=1)

    # Save .csv
    df_output.to_csv('./nba_preprocessed.csv', encoding='utf-8', index=False)

    print("Execution time =", time.time() - startTime)



#-----------------------#
#     Sub-Functions     #
#-----------------------#

# @param df: pandas.DataFrame
# @return pandas.DataFrame
# NaN cleaner (Numerical)
def cleanDataFrame(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].reset_index(drop=True)

# @param df: pandas.DataFrame
# @return pandas.DataFrame
# Drop objects which are NaN in Score's label (String)
def dropNanScore(df):
    index = []
    for idx, score in enumerate(df['Score']):
        if score[:3] == 'NAN' or score[:3] == 'NaN':
            index.append(idx)
    print("Number of objects dropped =", len(index))
    return df.drop(df.index[index]).reset_index(drop=True)

# @param df: pandas.DataFrame
# @return df: pandas.DataFrame
# Add opponent label to a game
def addOpponentCol(df):
    opponent = [None] * len(df['Score'])
    for idx, score in enumerate(df['Score']):
        opponent[idx] = score[:3]
    df['Opponent'] = opponent
    return df

# @param df: pandas.DataFrame
# @return df_team, df_oppo: pandas.DataFrame
# Pair two teams in a single game by searching 'Date' and 'Opponent' labels.
def pairGamePlayers(df):
    startTime = time.time()
    invalid_idx = []
    duplicate = 0
    not_found = 0
    # Declare empty dataframe w/ columns from existing dataframe
    df_team = pd.DataFrame(columns = list(df)) # Team attributes
    df_oppo = pd.DataFrame(columns = list(df)) # Opponent attributes
    df_dupl = pd.DataFrame(columns = list(df)) # Duplicated dataframe
    for idx, date, team in zip(df.index.tolist(), df['Date'], df['Team']):
        df_oppo_searched = df.loc[lambda df: df.Date == date, :].loc[lambda df: df.Opponent == team, :]
        if len(df_oppo_searched.index.tolist()) > 1:
            duplicate += 1
            df_dupl = pd.concat([df_dupl, df_oppo_searched], ignore_index=True)
            df_oppo_searched = df_oppo_searched.iloc[0:1, :]
        if not df_oppo_searched.empty:
            df_team = pd.concat([df_team, df.iloc[idx:idx+1, :]], ignore_index=True)
            df_oppo = pd.concat([df_oppo, df_oppo_searched], ignore_index=True)
        else:
            invalid_idx.append(idx)
            not_found += 1

    print("Duplicate found =", duplicate)
    print("Opponent not found =", not_found)
    print("Team length = ", len(df_team.index.tolist()))
    print("Oppo length = ", len(df_oppo.index.tolist()))
    print("Execution time =", time.time() - startTime)
    return df_team, df_oppo, invalid_idx

# @param df_team, df_oppo: pandas.DataFrame
# @return df_team, df_oppo: pandas.DataFrame
# Check game validity after pairGamePlayers(df) which pairs two teams in a single game.
def checkGameValidity(df_team, df_oppo):
    startTime = time.time()
    err = 0
    invalid_idx = []
    print("Team length = ", len(df_team.index.tolist()))
    print("Oppo length = ", len(df_oppo.index.tolist()))
    for idx in df_team.index.tolist():
        if df_team.loc[idx]['Date'] != df_oppo.loc[idx]['Date'] or \
        df_team.loc[idx]['Opponent'] != df_oppo.loc[idx]['Team'] or \
        df_team.loc[idx]['W/L'] == df_oppo.loc[idx]['W/L'] or \
        df_team.loc[idx]['Home/Away'] == df_oppo.loc[idx]['Home/Away']:
            err += 1
            invalid_idx.append(idx)

    df_team = df_team.drop(df_team.index[invalid_idx]).reset_index(drop=True)
    df_oppo = df_oppo.drop(df_oppo.index[invalid_idx]).reset_index(drop=True)

    print("Number of invalid games =", err, "@", [x for x in invalid_idx])
    print("Execution time =", time.time() - startTime)
    return df_team, df_oppo, invalid_idx



#-----------------------#
#       Execution       #
#-----------------------#

if __name__ == '__main__':
    main()
