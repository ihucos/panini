import configparser


def infer_driver_name(section_name, section):
    if not section:
        return section_name
    return next(iter(section.keys()))


def get_command(name):
    config = get_config()
    drivers = get_drivers()
    section = config[name]
    section = dict(section)
    driver = infer_driver_name(name, section)
    section.pop("driver", None)
    handler = drivers[driver]
    # try:
    cmd = handler(**section)
    # except TypeError as exc:
    #     breakpoint()
    return list(cmd)


_config = None


def get_config():
    global _config
    if _config is not None:
        return _config
    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
        allow_no_value=True,
    )
    config.read("taxi.ini")
    _config = config
    return config


_drivers = {}


def register(func):
    _drivers[func.__name__] = func
    return func


def get_drivers():
    return _drivers
