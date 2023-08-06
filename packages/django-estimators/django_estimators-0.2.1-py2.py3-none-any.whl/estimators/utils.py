

def get_subclasses(cls, recursive=True):
    subclasses = []

    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        if recursive:
            subclasses.extend(get_subclasses(subclass))

    return subclasses
