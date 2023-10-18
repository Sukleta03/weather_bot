from decouple import Config


config = Config('.env')

bot_token = config('BOT_TOKEN')
pg_host = config('PG_HOST')
pg_name = config('PG_NAME')
pg_password = config('PG_PASSWORD')
pg_port = config('PG_PORT')
pg_user = config('PG_USER')
pg_data = config('PG_DATA')
redis_host = config('REDIS_HOST')
redis_password = config('REDIS_PASSWORD')
redis_port = config('REDIS_PORT')