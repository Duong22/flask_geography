from .movie import MoviesApi

def initialize_routes(api):
    api.add_resource(MoviesApi, '/api/movies')