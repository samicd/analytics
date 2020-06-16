"""
1. Plot passes and shots leading up to the 2nd and 3rd goals
2. plot all the shots by player 9 of the home team. with different symbols for on/off target and goals
3. Plot all the positions of players at player 9's goal
4. calculate how far each player ran
"""
import LS_functions.Metrica_IO as mio
import LS_functions.Metrica_Viz as mviz
import numpy as np


# 1. Plot passes and shots leading up to the 2nd and 3rd goals
def question1():
    # set up initial path to data
    DATADIR = '/Users/Kafka/PycharmProjects/analytics/metrica/'
    game_id = 2  # let's look at sample match 2

    # read in the event data
    events = mio.read_event_data(DATADIR, game_id)
    # unit conversion
    events = mio.to_metric_coordinates(events)

    # Get all shots
    shots = events[events['Type'] == 'SHOT']

    # Get the shots that led to a goal
    all_goals = shots[shots['Subtype'].str.contains('-GOAL')].copy()

    # Add a column event 'Minute' to the data frame
    all_goals['Minute'] = all_goals['Start Time [s]'] / 60.

    # Plotting pitch
    fig, ax = mviz.plot_pitch()

    # point of shot
    ax.plot(events.loc[823]['Start X'], events.loc[823]['Start Y'], 'ro')
    # negative as it is for the away team and it make it easier to differentiate
    ax.plot(-events.loc[1118]['Start X'], -events.loc[1118]['Start Y'], 'bo')

    # Shot direction
    ax.annotate("", xy=events.loc[823][['End X', 'End Y']], xytext=events.loc[823][['Start X', 'Start Y']], alpha=0.6,
                arrowprops=dict(arrowstyle="->", color='r'))
    ax.annotate("", xy=-events.loc[1118][['End X', 'End Y']], xytext=-events.loc[1118][['Start X', 'Start Y']],
                alpha=0.6,
                arrowprops=dict(arrowstyle="->", color='b'))

    # plot passing move in run up to goal
    mviz.plot_events(events.loc[818:822], indicators=['Marker', 'Arrow'], annotate=True, figax=(fig, ax))
    mviz.plot_events(events.loc[1109:1111], indicators=['Marker', 'Arrow'], color='b', annotate=True, neg=True,
                     figax=(fig, ax))
    mviz.plot_events(events.loc[1115:1116], indicators=['Marker', 'Arrow'], color='b', annotate=True, neg=True,
                     figax=(fig, ax))

    fig.savefig('question1.pdf', dpi=100)
    fig.show()


# 2. plot all the shots by player 9 of the home team. with different symbols for on/off target and goals
def question2():
    # set up initial path to data
    DATADIR = '/Users/Kafka/PycharmProjects/analytics/metrica/'
    game_id = 2  # let's look at sample match 2

    # read in the event data
    events = mio.read_event_data(DATADIR, game_id)
    # unit conversion
    events = mio.to_metric_coordinates(events)

    # Get all shots
    shots = events[events['Type'] == 'SHOT']

    # Get the shots that led to a goal
    all_goals = shots[shots['Subtype'].str.contains('-GOAL')].copy()

    # Add a column event 'Minute' to the data frame
    all_goals['Minute'] = all_goals['Start Time [s]'] / 60.

    # Plotting pitch
    fig, ax = mviz.plot_pitch()

    for i in shots.index[shots['From'] == 'Player9'].tolist():
        if 'OFF' in events.loc[i]['Subtype']:
            arr = "-[, widthB=.4"
            clr = 'r'
        else:
            arr = "->"
            clr = 'b'

        ax.plot(events.loc[i]['Start X'], events.loc[i]['Start Y'], 'ro')

        # Shot direction
        ax.annotate("", xy=events.loc[i][['End X', 'End Y']], xytext=events.loc[i][['Start X', 'Start Y']], alpha=0.6,
                    arrowprops=dict(arrowstyle=arr, color=clr))

    fig.savefig('question2.pdf', dpi=100)
    fig.show()


# 3. Plot all the positions of players at player 9's goal
def question3():
    # set up initial path to data
    DATADIR = '/Users/Kafka/PycharmProjects/analytics/metrica/'
    game_id = 2  # let's look at sample match 2

    # read in the event data
    events = mio.read_event_data(DATADIR, game_id)
    # unit conversion
    events = mio.to_metric_coordinates(events)

    # Plot some player trajectories (players 11,1,2,3,4)
    fig, ax = mviz.plot_pitch()

    goal_event_id = 1118

    # READING IN TRACKING DATA
    tracking_home = mio.tracking_data(DATADIR, game_id, 'Home')
    tracking_away = mio.tracking_data(DATADIR, game_id, 'Away')

    # Convert positions from metrica units to meters
    tracking_home = mio.to_metric_coordinates(tracking_home)
    tracking_away = mio.to_metric_coordinates(tracking_away)

    # PLOT POISTIONS AT GOAL
    fig, ax = mviz.plot_events(events.loc[goal_event_id:goal_event_id], indicators=['Marker', 'Arrow'], annotate=True)
    goal_frame = events.loc[goal_event_id]['Start Frame']
    fig, ax = mviz.plot_frame(tracking_home.loc[goal_frame], tracking_away.loc[goal_frame], figax=(fig, ax))

    fig.savefig('question3.pdf', dpi=100)
    fig.show()


# 4. calculate how far each player ran
def question4():
    # set up initial path to data
    DATADIR = '/Users/Kafka/PycharmProjects/analytics/metrica/'
    game_id = 2  # let's look at sample match 2

    # READING IN TRACKING DATA
    tracking_home = mio.tracking_data(DATADIR, game_id, 'Home')
    tracking_away = mio.tracking_data(DATADIR, game_id, 'Away')

    # Convert positions from metrica units to meters
    tracking_home = mio.to_metric_coordinates(tracking_home)
    tracking_away = mio.to_metric_coordinates(tracking_away)

    home_tot_distance = tracking_home[tracking_home['Period'] == 1].diff().abs().sum() + tracking_home[
        tracking_home['Period'] == 2].diff().abs().sum()
    home_tot_distance = home_tot_distance.drop(['Period', 'Time [s]', 'ball_x', 'ball_y'])

    y = home_tot_distance[['_y' in s for s in home_tot_distance.index]]
    x = home_tot_distance[['_x' in s for s in home_tot_distance.index]]
    a = list(zip(x, y))
    a = [x + y for (x, y) in a]

    away_tot_distance = tracking_away[tracking_away['Period'] == 1].diff().abs().sum() + tracking_away[
        tracking_away['Period'] == 2].diff().abs().sum()


if __name__ == '__main__':
    question4()
