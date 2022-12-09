"""
AWS Lambda Module Mock for test resources
Version: 1.0.0
"""
class FakeLambdaContextIdentity(object):
    def __init__(self, cognito_identity_id, cognito_identity_pool_id):
        self.cognito_identity_id = cognito_identity_id
        self.cognito_identity_pool_id = cognito_identity_pool_id


class FakeLambdaContext(object):
    def __init__(self):
        self.function_name = 'test_name'
        self.function_version = 'version'
        self.invoked_function_arn = 'arn'
        self.memory_limit_in_mb = 256
        self.aws_request_id = 'id'
        self.log_group_name = 'log_group_name'
        self.log_stream_name = 'log_stream_name'
        self.identity = FakeLambdaContextIdentity('id', 'id_pool')
        # client_context is set by the mobile SDK and wont be set for chalice
        self.client_context = None

    def get_remaining_time_in_millis(self):
        return 500

    def serialize(self):
        serialized = {}
        serialized.update(vars(self))
        serialized['identity'] = vars(self.identity)
        return serialized
