import requests
import pandas as pd
import colorama

colorama.init()

# Function to get ratings for a TV show
def get_ratings(show_name):
  # Make a request to the TV Maze API to get the show's ID
  r = requests.get(f'http://api.tvmaze.com/singlesearch/shows?q={show_name}')
  show_id = r.json()['id']
  
  # Make a request to the TV Maze API to get a list of episodes for the show
  r = requests.get(f'http://api.tvmaze.com/shows/{show_id}/episodes')
  episodes = r.json()
  
  # Create a list of dictionaries with information for each episode
  episode_data = []
  for episode in episodes:
    data = {
      'Season': episode['season'],
      'Episode': episode['number'],
      'Name': episode['name'],
      'Rating': episode['rating']['average']
    }
    episode_data.append(data)
  
  # Create a Pandas DataFrame from the list of dictionaries
  df = pd.DataFrame(episode_data)
  
  # Group the DataFrame by season
  df_grouped = df.groupby('Season')
  
  # Color code the ratings column based on the rating value
  def color_rating(val):
    if val >= 9.0:
      color = colorama.Fore.GREEN
    elif val >= 8.0:
      color = colorama.Fore.LIGHTGREEN_EX
    elif val >= 6.0:
      color = colorama.Fore.YELLOW
    else:
      color = colorama.Fore.RED
    return f'{color}{val}{colorama.Style.RESET_ALL}'
  
  # Iterate through the groups and display each one
  for name, group in df_grouped:
    print(f'Season {name}:')
    group['Rating'] = group['Rating'].apply(color_rating)
    print(group)
    print()

# Read the show name from the user
show_name = input('Enter the name of a TV show: ')

# Get and display the ratings for the show
get_ratings(show_name)

