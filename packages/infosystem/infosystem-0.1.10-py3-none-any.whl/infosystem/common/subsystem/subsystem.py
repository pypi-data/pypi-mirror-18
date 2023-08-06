import flask


class Subsystem(flask.Blueprint):

    def __init__(self, entity):
        self.entity = entity
        self.capabilities = {}

    def set_policy(self, capability, policy):
        self.capabilities['capability'] = policy

    def register_routes(self):
        if hasattr(self.manager, 'create'):
            self.add_url_rule(self.collection_url,
                              view_func=self.create, methods=['POST'])
        if hasattr(self.manager, 'get'):
            self.add_url_rule(self.entity_url,
                              view_func=self.get, methods=['GET'])
        if hasattr(self.manager, 'list'):
            self.add_url_rule(self.collection_url,
                              view_func=self.list, methods=['GET'])
        if hasattr(self.manager, 'update'):
            self.add_url_rule(self.entity_url,
                              view_func=self.update, methods=['PUT'])
        if hasattr(self.manager, 'delete'):
            self.add_url_rule(self.entity_url,
                              view_func=self.delete, methods=['DELETE'])


subsystem = Subsystem(entity.Token)
subsystem.set_policy('POST', '/users' 'bypass')
subsystem.set_policy('GET', '/users/<id>', 'all')

subsystem = Subsystem(entity.User)
subsystem.register()
