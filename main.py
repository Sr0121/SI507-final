from session import Sess
import webAPI
import suggestion
import warnings


warnings.filterwarnings("ignore")  # ignore warnings

# csv file paths
credit_file_path = "./data/tmdb_5000_credits.csv"
movie_file_path = "./data/tmdb_5000_movies.csv"

# init database, graph and the webAPI cache
webAPI.load_cache()
sess = Sess()
sess.init_database(credit_file_path, movie_file_path)
graph = suggestion.load_graph(credit_file_path)


def print_list(items):
    cnt = 1
    res_map = {}
    for item in items:
        print("%d. %s" % (cnt, item))
        res_map[cnt] = item
        cnt += 1
    return res_map


def find_all_genres():
    _ = print_list(sess.find_all_genres())


def find_movies():
    print("What genre of movies you are looking for? (seperated by \",\" or leave blank to find all)")
    genre_list = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), input().split(","))))

    print("What characters are you looking for in the movies? (seperated by \",\" or leave blank to find all)")
    character_list = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), input().split(","))))

    print("What casts or crews are you looking for in the movies? (seperated by \",\" or leave blank to find all)")
    people_list = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), input().split(","))))

    res_map = print_list(sess.find_movies(genre_list, character_list, people_list))

    if len(people_list) == 1:
        print("Similar Actors:")
        print_list(suggestion.find_closest_people(graph, people_list[0], limit=5))

    if len(res_map) == 0:
        print("No matches!")
        return

    choice = input("Enter a number of movie for more detail info, "
                   "or enter any other characters to return to the main menu: ")
    if choice.isnumeric():
        if int(choice) in res_map:
            print(webAPI.fetch_data(res_map[int(choice)].title))


def get_movie_info():
    print("Please enter the title of the movie:")
    title = input()
    print(webAPI.fetch_data(title))


def find_similar_actors():
    print("Please enter the name of the actor: ")
    name = input()
    print("Similar Actors:")
    print_list(suggestion.find_closest_people(graph, name, limit=10))


if __name__ == '__main__':
    print("Hello!")
    while True:
        print("""
------------------------------------------------------
What do you want to do? Enter a number for selection.
1. List all genres in the database
2. Search movie title
3. Find similar actors
4. Get detail movie information
Otherwise: exit""")
        choice = input()
        choiceMap = {
            "1": find_all_genres,
            "2": find_movies,
            "3": find_similar_actors,
            "4": get_movie_info
        }
        if choice not in choiceMap:
            break
        choiceMap[choice]()
    print("Bye~")
    del sess

