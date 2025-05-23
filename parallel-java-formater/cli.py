import sys
from concurrent import futures
from termcolor import colored

import glob
import os
import git
import threaded

def cpu_count() -> int:
    print("Pool Size: ", end="")
    print(pool_size_count := os.cpu_count() * 2)
    return pool_size_count

threaded.ThreadPooled.configure(max_workers=cpu_count())


@threaded.ThreadPooled
def _java_format_file(path_file: str):
    print(f"{colored('Start format', 'green')}: {path_file}")
    os.system(f"java -jar google-java-format-1.23.0-all-deps.jar --replace {path_file}")

def java_format_file_list(path_files: list[str]):
    return futures.wait(_java_format_file(f) for f in path_files)

def java_format_folder(path_folder: str):
    return java_format_file_list(glob.glob(f"{path_folder}/**/*.java", recursive=True))

def java_format_git_change(path_folder: str):
    try:
        repo = git.Repo(path_folder)
        return java_format_file_list([f"{path_folder}/{f.a_path}" for f in repo.index.diff(None)])
    except git.exc.InvalidGitRepositoryError:
        print(f"{colored('InvalidGitRepositoryError', 'red')}: {path_folder}")

_help = '''
Can be use as list => python cli.py [FOLDER_NAME]
h help
g git local repo change
d directory
f file
'''

def ask_folder():
    return input("Path folder: ")


def main():
    given_folder = sys.argv[1]
    if given_folder is not None:
        try:
            git.Repo(given_folder)
            print(colored("XD Git repository detected", "green", attrs=["bold"]))
            java_format_git_change(given_folder)
            sys.exit()
        except git.exc.InvalidGitRepositoryError:
            print(colored(";X no Git repository detected", "red", attrs=["bold"]))
            java_format_folder(given_folder)
            sys.exit()
        except Exception as e:
            print("Unknow Exception: ", e)
        try:
            java_format_file_list([given_folder])
            sys.exit()
        except Exception as e:
            print("Unknow Exception: ", e)
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


if __name__ == '__main__':
    main()
