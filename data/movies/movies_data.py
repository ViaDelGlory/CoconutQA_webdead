from utils.data_generator import DataGenerator

def get_movie_data():
    return {
        "name": DataGenerator.generate_name_movie(),
        "imageUrl": DataGenerator.generate_url(),
        "price": DataGenerator.generate_fake_price(),
        "description": DataGenerator.generate_description(),
        "location": DataGenerator.generate_locations(),
        "published": DataGenerator.generate_boolean(),
        "genreId": DataGenerator.generate_id()
    }
