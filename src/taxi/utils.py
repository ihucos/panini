import configparser
import os


class TaskError(Exception):
    pass


def infer_driver_name(section_name, section):
    if not section:
        return section_name
    return next(iter(section.keys()))


def get_command(name):
    config = get_config()
    try:
        section = config[name]
    except KeyError:
        raise TaskError(f"no such task: {name}")
    ctx = {"section_name": name}
    return get_command2(name, dict(section))


def get_command2(name, section):
    drivers = get_drivers()

    driver = infer_driver_name(name, section)
    section.pop("driver", None)
    try:
        handler = drivers[driver]
    except KeyError:
        raise TaskError(f"no such driver ({driver}) at task {name}")
    # try:
    if section == {}:
        section = {name: None}
    try:
        ctx = {"section_name": name}
        cmd = handler(ctx, **section)
    except TypeError as exc:
        # Make error message less pythonic and more INI
        msg = (
            exc.args[0]
            .replace("keyword-only ", "")
            .replace("keyword ", "")
            .replace("argument", "key")
            .replace("arguments", "keys")
            .replace(
                "()",
                "",
            )
        )
        raise TaskError(f"section {name}: driver {msg}")
    return list(cmd)


_config = None


def init_config():
    global _config
    _config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
        allow_no_value=True,
    )
    config_file = os.environ.get("TAXI_CONFIG", "taxi.ini")
    _config.read(config_file)


def get_config():
    assert _config, "call init_config()"
    return _config


_drivers = {}


def register(func):
    _drivers[func.__name__.rstrip("_")] = func
    return func


def get_drivers():
    return _drivers
