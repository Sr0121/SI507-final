import session
import webAPI
import suggestion

credit_file_path = "./data/tmdb_5000_credits.csv"
movie_file_path = "./data/tmdb_5000_movies.csv"

if __name__ == '__main__':
    webAPI.load_cache()
    session.init_database(credit_file_path, movie_file_path)
    graph = suggestion.load_graph(credit_file_path)
    print(webAPI.fetch_data("John Carter"))
    print(suggestion.find_closest_staff(graph, "Sam Worthington"))

