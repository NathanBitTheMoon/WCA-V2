class Announcement:
    def __init__(self, client):
        self.client = client
        self.hooks = {}
        self.hook_objects = {}
    
    @staticmethod
    def construct_hook_id(hook):
        return f"{hook.hook_object.event.id_name};{hook.hook_object.area};{hook.hook_object.ranking_type}"

    def add_hook(self, channel : int, hook):
        hook_id = Announcement.construct_hook_id(hook)
        if hook_id in self.hooks.keys():
            self.hooks[hook_id].append(channel)
            self.hook_objects[hook_id] = hook
        else:
            self.hooks[hook_id] = [channel]