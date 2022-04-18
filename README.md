# SI507-final
UMich SI 507 Final Project

In this project, we are trying to build a program to help people search for the movie information. Users can use this program to search movies by genre, character, crew and cast, and can choose the movie to see the detail of it. In addition, if the user searches by cast name, the program will display some names associated with that name as the suggestions.

* Required Packages: sqlalchemy, pandas, requests
* Required Database: SQLite
* Demo Video Link: https://youtu.be/IqUsTg-wc3c


## Interaction
We are using the command line to do the interaction and presentation. The whole interaction flow would be a little similar to the project 1. All selection needs user to enter the corresponding number to choose. 

Since most of the data in the csv files comes from before 2016, we encourage users to use the movie information before 2016 to query.

The main menu has four options: list all genres, search movie title, find similar actors and get detail information about a certain movie. 

### List all genres
It will list all types of genres in the database, which lets the user know what movie genres can be used to search.

### Search movie title
If the user choice this option, user needs to enter the types of genres, the names of characters and the names of the casts or the crews. Different entries of the same type are separated by commas. Then the program will return a list of movies that satisfy the searching requirement and the user can enter a number to get the detail information of the corresponding movie.

If the user only use one name of a cast or a crew to search, the program will also return the names of actors who are similar to him. 

### Find similar actors
User needs to enter a name of a cast or a crew than the program will also return the names of casts and crews who are similar to him based on the BFS algorithm.

### Get detail information
If the user choice this option, he then needs to enter a title of a certain movie, then the program will display the detail information about this movie.


## Data Structure
In this project, we are going to make some suggestions when user inputs an actor name or asking names for suggestions. We believe people who are in the same movie would be related. When we create the network, we connect each person to all the films he was involved in. Then we are going to use BFS to search the closest people as the suggestions.

We use a dict structure to save the graph. The key of the dict is the name of a person or a film. If the key is a person's name, then the value of it is a list of movies that the person took part in. If the key is a movie's name, then the value is a list of actors' name who participate this movie. 

```python
    graph[people1] = [movie1, movie2, movie3, ...]
    graph[movie1] = [people1, people2, people3, ...]
```

We read the each line of the file, parse the crew data and the cast data. For each actor's name, we append the movie name to the value of it and we append it to the value of the movie name. Finally we save the graph to a json file, next time it can be loaded directly from the json file. Here is the code that implements the graph construction. 

```python
def build_graph(credit_file_path):
    graph = collections.defaultdict(list)
    credit_data = pd.read_csv(credit_file_path)
    for _, row in credit_data.iterrows():
        casts = json.loads(row["cast"])
        for cast in casts:
            graph[row["title"]].append(cast["name"])
            graph[cast["name"]].append(row["title"])
        crews = json.loads(row["crew"])
        for crew in crews:
            graph[row["title"]].append(crew["name"])
            graph[crew["name"]].append(row["title"])

    with open(graph_path, "w") as f:
        json.dump(graph, f)
```


