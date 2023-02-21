import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt

CATEGORY_ID = {
    '1': 'Film & Animation',
    '2': 'Autos & Vehicles',
    '10': 'Music',
    '15': 'Pets & Animals',
    '17': 'Sports',
    '18': 'Short Movies',
    '19': 'Travel & Events',
    '20': 'Gaming',
    '21': 'Videoblogging',
    '22': 'People & Blogs',
    '23': 'Comedy',
    '24': 'Entertainment',
    '25': 'News & Politics',
    '26': 'Howto & Style',
    '27': 'Education',
    '28': 'Science & Technology',
    '29': 'Nonprofits & Activism',
    '30': 'Movies',
    '31': 'Anime/Animation',
    '32': 'Action/Adventure',
    '33': 'Classics',
    '34': 'Comedy',
    '35': 'Documentary',
    '36': 'Drama',
    '37': 'Family',
    '38': 'Foreign',
    '39': 'Horror',
    '40': 'Sci-Fi/Fantasy',
    '41': 'Thriller',
    '42': 'Shorts',
    '43': 'Shows',
    '44': 'Trailers',
}


def create_plot(df: pd.DataFrame, country: str):
    """Create a horizontal bar chart with the top 10 categories in the dataframe"""
    category = df['category_id'].tolist()
    channelName = df['channel_title'].tolist()
    category_counter = Counter(channelName)
    category_counter2 = Counter(category)

    category = [ cat[0] for cat in category_counter2.most_common(10)]
    category_iid = [CATEGORY_ID[str(cat)] for cat in category]
    channelName = [cat[0] for cat in category_counter.most_common(10)]
    category_count = [cat[1] for cat in category_counter.most_common(10)]
    create_horizontal_bar_chart(channelName, category_count, country, title=f'Top 10 channels in {country}',xlabel='Number of videos', color='blue')
    create_horizontal_bar_chart(category_iid, category, country, title=f'Top 10 category in {country}',xlabel='Number of videos', color='red')


def create_plot_dataframe_vs_category_id(df: pd.DataFrame, country: str, versus: str, per: int, x_label: str, color: str, title: str):
    """Create a horizontal bar chart vs category_id"""
    dict = {}
    for x, y in zip(df['category_id'], df[versus]):
        if x in dict:
            dict[x] += y
        else:
            dict[x] = y
    dictDf = pd.DataFrame.from_dict(dict, orient='index', columns=[versus])
    y_axis_value = [CATEGORY_ID[str(cat)] for cat in dictDf.index.tolist()]
    x_axis_value = [versus/per for versus in dictDf[versus].tolist()]
    create_horizontal_bar_chart(y_axis_value, x_axis_value, country, title=title, xlabel=x_label, color=color)


def create_horizontal_bar_chart(y_plot: list, x_plot: list, country: str, title: str, xlabel: str, color: str):
    """Create a horizontal bar chart with the top 10 categories in the dataframe"""
    plt.style.use('fivethirtyeight')
    plt.barh(y_plot, x_plot, color=color)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()


# Read the csv files
dfDE = pd.read_csv('DEvideos.csv')
dfCA = pd.read_csv('CAvideos.csv')
dfFR = pd.read_csv('FRvideos.csv')
dfUS = pd.read_csv('USvideos.csv')
dfGB = pd.read_csv('GBvideos.csv')
dfIN = pd.read_csv('INvideos.csv')

# Create a dictionary of dataframes
dataframes = {'Germany': dfDE, 'Canada': dfCA,
              'France': dfFR, 'USA': dfUS, 'UK': dfGB, 'India': dfIN}

# Create a plot for each dataframe
for k,v in dataframes.items():
    create_plot(v,k)

# Create a plot for each dataframe (views vs category_id)
for k, v in dataframes.items():
    create_plot_dataframe_vs_category_id(
        v, k, 'views', 1000, x_label='Views (in millions)', color='yellow', title=f'Top 10 categories with most views in {k}')
    
# Create a plot for each dataframe (likes vs category_id)
for k, v in dataframes.items():
    create_plot_dataframe_vs_category_id(
        v, k, 'likes', 1000, x_label='Likes (in thousands)', color='red', title=f'Likes per Category in {k}')

# Create a plot for each dataframe (dislikes vs category_id)
for k, v in dataframes.items():
    create_plot_dataframe_vs_category_id(v, k, 'dislikes', 1000, x_label='Dislikes (in thousands)',
                                         color='green', title=f'Dislikes per category in {k}')

for k, v in dataframes.items():
    c = Counter()
    for tag in v['tags']:
        c.update(tag.replace('"','').split('|'))
    tags = [tag for tag, count_tag in c.most_common(10)]
    tags_count = [count_tag for tag, count_tag in c.most_common(10)]
    create_horizontal_bar_chart(tags, tags_count, k, title=f'Top 10 tags in {k}', xlabel='Number of videos', color='teal')

