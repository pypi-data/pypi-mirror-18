import sys


def extract_is_release_from_argv():
    if "--vcver-release" in sys.argv:
        sys.argv.remove("--vcver-release")
        return True
    return False
