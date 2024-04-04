import subprocess


def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def main():
    subprocess.run(["python", "getCVdata.py"])
    subprocess.run(["python", "getAnnounceEmploi.py"])


if __name__ == '__main__':
    main()
    print_hi('This is my project of MIAGE')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
