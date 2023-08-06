import typing


class Gettable:
    def get(self):
        raise NotImplementedError("This must be implemented")

T = typing.TypeVar('T')


def get_with_retry(get_from: Gettable, retry_count: int, fallback_value: T) -> T:
    return retry_callable(get_from.get, retry_count, fallback_value)


def retry_callable(idem_potent_callable: typing.Callable[[], T], retry_count: int, fallback_value: T) -> T:
    if retry_count < 0:
        print("falling back to fallback value")
        return fallback_value
    else:
        try:
            return idem_potent_callable()
        except Exception as e:
            print(e)
            print("failed, retrying up to {} more times...".format(retry_count))
            return retry_callable(idem_potent_callable, retry_count - 1, fallback_value)
