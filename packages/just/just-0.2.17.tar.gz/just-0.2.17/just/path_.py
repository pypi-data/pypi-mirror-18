import sys
import os


def get_just_env_path():
    return os.environ.get("JUST_PATH")


def find_just_path(max_depth=5):
    for depth in range(max_depth):
        prefix = "../" * depth
        just_file = os.path.join(prefix, ".just")
        if os.path.isfile(just_file):
            return os.path.abspath(os.path.dirname(just_file))
    return None


def get_likely_path():
    # try:
        #main_path = os.path.abspath(sys.modules['__main__'].__file__)
    # except AttributeError:
    main_path = os.path.realpath('__file__')
    return os.path.dirname(main_path)


def get_just_path():
    just_path = get_just_env_path()
    just_path = just_path if just_path is not None else find_just_path()
    just_path = just_path if just_path is not None else get_likely_path()
    return just_path
