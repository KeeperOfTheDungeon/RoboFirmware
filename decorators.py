
def own_decorator(wait_pin):
    def specific_decorator(func):
        def wrapper():
            return func(wait_pin)
        return wrapper
    return specific_decorator
