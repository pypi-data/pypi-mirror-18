

def print_post_init(sender, instance, **kwargs):
    instance.done = 'haha'


def post_init_with_abstract_object(sender, instance, *args, **kwargs):

    obj = kwargs.pop(sender.INIT_ARG_NAME)
    print(obj)
    instance.set_object(args[0])


def pre_init_with_abstract_object(sender, instance, *args, **kwargs):

    obj = kwargs.pop(sender.INIT_ARG_NAME)
    print(obj)
    instance.set_object(args[0])
