import configparser
import os


SYSTEM_CONFIG = {
    "list": {},
    "getcmd": {"getcmd": None},
}


class TaskError(Exception):
    pass


def infer_driver_name(section_name, section):
    if not section:
        return section_name
    return next(iter(section.keys()))


def get_command(name, args):
    config = get_config()
    try:
        section = config[name]
    except KeyError:
        raise TaskError(f"no such task: {name}")
    ctx = {"section_name": name}
    return get_command2(name, dict(section), args)


def addenv(cmd, env):
    cmd = list(cmd)
    env = [i for i in env.splitlines() if i]
    if env:
        yield "env"
        for e in env:
            if "=" not in e:
                raise TaskError(f"Not an env (Missing a =): {e}")
            yield e

    yield from cmd


def get_command2(name, section, args):
    drivers = get_drivers()

    driver = infer_driver_name(name, section)
    section.pop("driver", None)

    if driver not in ["assert_cmd"]:  # HACK
        env = section.pop("env", None)
        via = section.pop("via", None)
    else:
        env = ""
        via = ""

    try:
        handler = drivers[driver]
    except KeyError:
        raise TaskError(f"no such driver ({driver}) at task {name}")
    # try:
    if section == {}:
        section = {name: None}
    try:
        ctx = {"section_name": name, "args": args}
        # print(handler.__name__, section)
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

    if env:
        cmd = list(addenv(cmd, env))

    if via:
        cmd = get_command(via, list(cmd))

    cmd = list(cmd)
    return cmd


_config = None


def init_config():
    global _config
    config = configparser.ConfigParser(
        allow_no_value=True,
        interpolation=None,
        delimiters="=",
    )
    config.optionxform = str
    config_file = os.environ.get("PANINI_CONFIG", "pan.ini")
    config.read(config_file)
    user_config = {k: dict(v) for (k, v) in config.items()}
    config = SYSTEM_CONFIG.copy()
    config.update(user_config)
    _config = config


def get_config():
    assert _config, "call init_config()"
    return _config


_drivers = {}


def register(func):
    _drivers[func.__name__.rstrip("_")] = func
    return func


def get_drivers():
    return _drivers
