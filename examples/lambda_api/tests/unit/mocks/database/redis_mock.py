import fakeredis


def get_connection(config=None, retry=False):
    host = config.REDIS_HOST
    port = config.REDIS_PORT
    # connection = redis.Redis(
    #     host=host,
    #     port=port
    # )
    server = fakeredis.FakeServer()
    connection = fakeredis.FakeStrictRedis(server=server)
    test = connection.set('connection', 'true')
    return connection
