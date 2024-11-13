from pymongo import MongoClient

class Config:
    SECRET_KEY = 'akmak2470'
    MONGODB_USERNAME = 'akmak_1'
    MONGODB_PASSWORD = 'xxWarWtqO5vVRgso'
    MONGODB_CLUSTER = 'cluster0.glb67p5.mongodb.net'
    MONGODB_DBNAME = 'DataBase'

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'

def get_db():
    config = Config()
    uri = f"mongodb+srv://{config.MONGODB_USERNAME}:{config.MONGODB_PASSWORD}@{config.MONGODB_CLUSTER}/{config.MONGODB_DBNAME}?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client[config.MONGODB_DBNAME]
    return db
