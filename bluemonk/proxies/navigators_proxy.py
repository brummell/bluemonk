from butterfly import Navigator

class NavigatorsProxy(object):
    def __init__(self, butterfly):
        self.navigator = Navigator(butterfly)

    def index(self, **options):
        return self.navigator.get_navigators(**options)

    def count(self, **options):
        count = self.navigator.get_navigator_count(**options)
        if not 'count' in count:
            return 0
        return int(count['count'])

    def from_id(self, navigator_id, **options):
        return self.navigator.view_navigator(navigator_id, **options)

    def create(self, **data):
        return self.navigator.add_navigator(**data)

    def update(self, navigator_id, **data):
        return self.navigator.update_navigator(navigator_id, **data)

    def handle_controls(self, data):
        '''
        This method handles incoming control requests.
        `data` should contain:
            - id (string)
            - reboot (bool)
            - authorize (bool)
        '''
        valid_actions = {
            'reboot': self.reboot,
            'authorize': self.authorize_boot
        }

        navigator_id = data.get('id', None)
        if not navigator_id:
            return False

        actions = {a : v for a, v in valid_actions.iteritems() if data.get(a, None)}
        results = {}
        for a in actions:
            results[a] = actions[a](navigator_id)
        print results

    def authorize_boot(self, navigator_id):
        return self.navigator.update_navigator(navigator_id, authorized_boot=True)

    def reboot(self, navigator_id):
        return self.navigator.reboot_navigator(navigator_id)
