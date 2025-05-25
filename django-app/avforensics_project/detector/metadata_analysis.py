import subprocess
import sys

def get_android_make(path):
    # Run exiftool normally for just the one tag
    result = subprocess.run(
        ["exiftool", "-AndroidMake", path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    text = result.stdout.decode("utf-8")
    # print(len(text))
    for line in text.splitlines():
        # look for the line starting with "Android Make"
        if line.lower().startswith("android make"):
            # split at the first colon, take the right side, strip whitespace
            _, value = line.split(":", 1)
            return value.strip()
    return None

def txt_read():
    with open("model_list.txt", "r") as f:
        a = f.read().strip()
        make_list = a.split("\n")
        # print(make_list)
    return make_list

# metadata_analysis.py

def make_check(path):
    exception_occured = 0
    make_flag = 0
    try:
        make = get_android_make(path)
        make_list = txt_read()

        for make_txt in make_list:
            if make and make_txt.lower() == make.lower():
                make_flag = 1
                print(make_flag)
                break

    except Exception:
        exception_occured = 1

    # Return both flags
    return exception_occured, make_flag
