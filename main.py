import glob
import os
from termcolor import colored
import git
import threading

def finalization(thread_list: list[threading.Thread]):
    return [f.join() for f in thread_list]

def finalize_annotation(func):
    def wrapper(*args, **kwargs):
        return finalization(func(*args, **kwargs))
    return wrapper

def _java_format_file(path_file: str):
    print(f"{colored('Formatted', 'green')}: {path_file}")
    os.system(f"java -jar google-java-format-1.23.0-all-deps.jar --replace {path_file}")

def java_format_file(path_file: str):
    t = threading.Thread(target=_java_format_file, args=(path_file,))
    t.start()
    print(f"{colored('Start thread', 'blue')} {t.name}")
    return t

def java_format_file_list(path_files: list[str]):
    return [java_format_file(f) for f in path_files]

@finalize_annotation
def java_format_folder(path_folder: str):
    return java_format_file_list(glob.glob(f"{path_folder}/**", recursive=True))

@finalize_annotation
def java_format_git_change(path_folder: str):
    try:
        repo = git.Repo(path_folder)
        return java_format_file_list([f"{path_folder}/{f.a_path}" for f in repo.index.diff(None)])
    except git.exc.InvalidGitRepositoryError:
        print(f"{colored('InvalidGitRepositoryError', 'red')}: {path_folder}")

_help = '''
h help
g git local repo change
d directory
f file
'''

def ask_folder():
    return input("Path folder: ")

if __name__ == '__main__':
    alors = input("Action: ")
    match alors:
        case "g":
            java_format_git_change(ask_folder())
        case "d":
            java_format_folder(ask_folder())
        case "f":
            _java_format_file(ask_folder())
        case "h":
            print(_help)
        case _:
            print(_help)
