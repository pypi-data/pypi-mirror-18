class Domovoi(object):
    scheduled_tasks = []

    def schedule(self, schedule):
        def register_scheduled_task(func):
            self.scheduled_tasks.append((schedule, func))
            return func
        return register_scheduled_task

    def __call__(self, event, context):
        context.log("Domovoi here! {}".format(event))
