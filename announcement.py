import discord, time

class Announcement:
    def __init__(self, client):
        self.client = client
        self.hooks = {}
        self.hook_objects = {}
    
    @staticmethod
    def log_usage(command, arg):
        f = open('ann.log', 'a')
        f.write("\n" + str(int(time.time())) + ":" + command + f"({arg})")
        f.close()

    @staticmethod
    def log_action(action):
        f = open('ann.log', 'a')
        f.write(";" + action)
        f.close()

    @staticmethod
    def construct_hook_id(hook):
        return f"{hook.hook_object.event.id_name};{hook.hook_object.area};{hook.hook_object.ranking_type}"

    def add_hook(self, channel, hook):
        hook_id = Announcement.construct_hook_id(hook)
        if hook_id in self.hooks.keys():
            self.hooks[hook_id].append(channel)
            self.hook_objects[hook_id] = hook
        else:
            self.hooks[hook_id] = [channel]
            self.hook_objects[hook_id] = hook
    
    async def background(self):
        Announcement.log_usage("background_start", "")
        while True:
            Announcement.log_usage("background_restart", "")
            print(self.hook_objects)
            for i in self.hook_objects.values():
                Announcement.log_action(f"check({Announcement.construct_hook_id(i)})")
                changes = i.get_changes()
                if i != False:
                    # Change detected
                    Announcement.log_action("change")
                    hook_id = Announcement.construct_hook_id(i)
                    for _ in self.hooks[hook_id]:
                        content = discord.Embed(title = f"New {i.hook_object.event.name} {i.hook_object.area} record!")
                        content.add_field(name = "Name", value = changes.name)
                        content.add_field(name = "Time", value = changes.result)
                        content.add_field(name = "WCA ID", value = changes.wca_id)

                        await _.send("@everyone", embed = content)
                else:
                    Announcement.log_action("none")
            time.sleep(120)