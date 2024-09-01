from os import path
from os.path import abspath

from dotenv import load_dotenv


def setup_environment(base_path):
    # find the .env files
    env_path = path.join(base_path, ".env")
    if path.exists(env_path):
        print("ENV: will load environment from: %s" % env_path)
        load_dotenv(env_path)
        print()
        return

    # also try to find a file in the parent dir
    env_path = abspath(path.join(base_path, "../", ".env"))
    if path.exists(env_path):
        print("ENV: will load environment from: %s" % env_path)
        load_dotenv(env_path)
        return
