import numpy as np
import pandas as pd
import os # import for clear output to not re-print table each time
import sys # to quit program 
from tabulate import tabulate
from itertools import product
import random
import matplotlib.pyplot as plt

# computer class to play against the trained software agent
class Computer:
    def convert_to_state(self,df):
        df_lst = []
        for i,j,k in df.values.tolist():
            df_lst.append(i)
            df_lst.append(j)
            df_lst.append(k)

        df_lst = [x if isinstance(x,str) else 'E' for x in df_lst]
        df_state = ''.join(df_lst)
        return df_state
    
    def get_qlearning_data(self,state):  
        if state in df_q_state.index:
            df_extract = df_q_state.loc[state,:].to_frame().reset_index()
            df_extract.rename(columns={'index': 'action'},inplace=True)
            state_lst = list(state)
            for i in range(len(df_extract.columns[1])):
                if state_lst[i] != 'E':
                    df_extract.drop(i,inplace=True)
                else:
                    pass
        else: 
            df_extract  = pd.DataFrame({'action': ['11','12','13','21','22','23','31','32','33'],
               state: [0.0]*9})
            state_lst = list(state)
            for i in range(len(df_extract.columns[1])):
                if state_lst[i] != 'E':
                    df_extract.drop(i,inplace=True)
                else:
                    pass
        return df_extract
    
    def select_action(self,extract_df,state):
        if extract_df[state].nunique() == 1:
            action = random.choice(extract_df.index)
        else:
            action = extract_df[state].idxmax()
        return action
    
    def convert_df(self,state,action_select):
        # convert state to list and update state based on action
        state_tolist = list(state)
        state_tolist[action_select] = 'X'
        
        #create new df based on new state while converting 'E' to np.nan
        new_df = pd.DataFrame({1: [np.nan if state_tolist[0]=='E' else state_tolist[0],
                                   np.nan if state_tolist[3]=='E' else state_tolist[3],
                                   np.nan if state_tolist[6]=='E'else state_tolist[6]],
           2: [np.nan if state_tolist[1]=='E' else state_tolist[1],
               np.nan if state_tolist[4]=='E' else state_tolist[4],
               np.nan if state_tolist[7]=='E'else state_tolist[7]],
           3: [np.nan if state_tolist[2]=='E' else state_tolist[2],
               np.nan if state_tolist[5]=='E' else state_tolist[5],
               np.nan if state_tolist[8]=='E'else state_tolist[8]],
            },columns=[1,2,3],index=[1,2,3])
        return new_df
    
    def check_status(self,df,condition,player):
        if (list(df[1].values) == (3 * [condition])) | (list(df[2].values) == (3 * [condition])) | (list(df[3].values) == (3 * [condition])): # wins by matching columns
            print(tabulate(df.fillna(' '), headers='keys', tablefmt='fancy_grid'))
            os.system( 'clear' )
            print(tabulate(df.fillna(' '), headers='keys', tablefmt='fancy_grid'))
            print ("{} wins".format(player))
            sys.exit()
        elif (list(df.iloc[0]) == (3 * [condition])) | (list(df.iloc[1]) == (3 * [condition])) | (list(df.iloc[2]) == (3 * [condition])): # wins by matching rows
            print(tabulate(df.fillna(' '), headers='keys', tablefmt='fancy_grid'))
            os.system( 'clear' )
            print(tabulate(df.fillna(' '), headers='keys', tablefmt='fancy_grid'))
            print ("{} wins".format(player))
            sys.exit()
        elif ([df.iloc[0, 0], df.iloc[1, 1], df.iloc[2, 2]] == (3 * [condition])) | ([df.iloc[0, 2], df.iloc[1, 1], df.iloc[2, 0]] == (3 * [condition])): # wins by matching columns
            print(tabulate(df.fillna(' '), headers='keys', tablefmt='fancy_grid'))
            os.system( 'clear' )
            print(tabulate(df.fillna(' '), headers='keys', tablefmt='fancy_grid'))
            print ("{} wins".format(player))
            sys.exit()
        elif pd.isnull(df).any().any()==False: # check if df contains NaNs
            os.system( 'clear' )
            print(tabulate(df.fillna(' '), headers='keys', tablefmt='fancy_grid'))
            print("It's a tie")
            sys.exit()
        else:
            status = 'continue'
        return status
    
    def get_available_actions(self,df):
        input_lst = []
        for i in range(len(df.values)):
            if (df.values[i][0] != 'X') and (df.values[i][0] != 'O'):
                input_lst.append(''.join([str(i+1),'1']))
            if (df.values[i][1] != 'X') and (df.values[i][1] != 'O'):
                input_lst.append(''.join([str(i+1),'2']))
            if (df.values[i][2] != 'X') and (df.values[i][2] != 'O'):
                input_lst.append(''.join([str(i+1),'3']))
            else:
                pass
        return input_lst

# tic tac toe game instructions to play against another human
def instructions():
    os.system( 'clear' ) # clears terminal so that df is not printed each time
    print('Instructions: each player enters location of X (player 1) or O (player 2) using a 2 digit integer, e.g. 12 for row 1 column 2')
    print(tabulate(df.fillna(' '), headers='keys', tablefmt='fancy_grid'))
    
# multiplayer game    
def play_game_multiplayer():
    count = 0 # we will be increment the count to signal when end of game has been reached
    input_lst = ['11', '12', '13', '21', '22', '23', '31', '32', '33'] 
    
    while count <= 9: # ends game when table is complete   
        # switches between player 1 and 2
        if (count % 2) == 0:
            player = ('Player 1','X')
        else:
            player = ('Player 2','O')
        
        while True:
        # gets player input
            player_input = str(input('{}({}): enter a 2-digit number representing a row and column: '.format(player[0],player[1]))) # input is a string

            if player_input in input_lst:
                # processes player input
                player_input.split()

                if player[0]=='Player 1':
                    df.iloc[int(player_input[0])-1,int(player_input[1])- 1] = 'X'
                else:
                    df.iloc[int(player_input[0])-1,int(player_input[1])- 1] = 'O'

                os.system( 'clear' )
                print(tabulate(df.fillna(' '), headers='keys', tablefmt='fancy_grid'))
                
                #updates the input_lst so that overwrite error do not happen 
                remove_number = player_input[0] + player_input[1]
                input_lst.remove(remove_number)
                break
            else:
                print('Invalid input. You can enter any number from the following list:' , ', '.join(input_lst))
                
        # checks if player won
        if (list(df[1].values) == (3 * [player[1]])) | (list(df[2].values) == (3 * [player[1]])) | (list(df[3].values) == (3 * [player[1]])): # wins by matching columns
            print ("{} wins".format(player[0]))
            sys.exit()
        if (list(df.iloc[0]) == (3 * [player[1]])) | (list(df.iloc[1]) == (3 * [player[1]])) | (list(df.iloc[2]) == (3 * [player[1]])): # wins by matching rows
            print ("{} wins".format(player[0]))
            sys.exit()
        if ([df.iloc[0, 0], df.iloc[1, 1], df.iloc[2, 2]] == (3 * [player[1]])) | ([df.iloc[0, 2], df.iloc[1, 1], df.iloc[2, 0]] == (3 * [player[1]])): # wins by matching columns
            print ("{} wins".format(player[0]))
            sys.exit()
        
        count += 1
        # checks if end of game is reached and no one won
        if count == 9: 
            print("It's a tie")
            sys.exit()

os.system( 'clear' )
game_choice = input('To play against the computer, enter 1. For multiplayer, enter 2: ')
df_q_state = pd.read_csv('q_learning_df.csv',index_col=0) # load q-learning matrix
comp = Computer() # create computer/software agent object
df = pd.DataFrame(index = range(1,4), columns = range(1,4)) # creating empty df for the tic tac toe board

while True:
    if game_choice == '1':
        while True:
            # computer plays
            state = comp.convert_to_state(df) # convert df to state (9-letter string)
            extract_df = comp.get_qlearning_data(state) # get applicable state from q-learning matrix
            action_select = comp.select_action(extract_df,state) # select action based on the q-learning matrix
            df = comp.convert_df(state,action_select) # action -->new state -->new df

            # check winner after computer plays
            game_status = comp.check_status(df,'X','Computer')
            
            # display table
            os.system( 'clear' )
            print(tabulate(df.fillna(' '), headers='keys', tablefmt='fancy_grid'))
            skip = False

            # human plays
            while True:
                # get the input_lst (available input per the df)
                input_lst = comp.get_available_actions(df)
                if skip:
                    pass
                else:
                    # gets player input
                    player_input = str(input('{}({}): enter a 2-digit number representing a row and column: '.format('Human','O'))) # input is a string
                if player_input in input_lst:
                    # processes player input
                    player_input.split()
                    df.iloc[int(player_input[0])-1,int(player_input[1])- 1] = 'O'
                    os.system( 'clear' )
                    print(tabulate(df.fillna(' '), headers='keys', tablefmt='fancy_grid'))
                    #updates the input_lst so that overwrite error do not happen 
                    remove_number = player_input[0] + player_input[1]
                    input_lst.remove(remove_number)
                    break
                else:
                    print('Invalid input. Available options:',','.join(input_lst))
                    player_input = str(input('{}({}): enter a 2-digit number representing a row and column: '.format('Human','O'))) # input is a string
                    skip = True
                    
            # check winner after human plays
            game_status = comp.check_status(df,'O','Human')

    elif game_choice == '2':
        instructions()
        play_game_multiplayer()
    else:
        game_choice = input('Invalid input. Enter Ctrl+C to exit, or enter 1 or 2 to play: ')
