from framework.util.Recording import GamePlayRecorder


def main():
    r = GamePlayRecorder(name="random_agent")
    r.open()
    e = r.read()
    while e[1] != -1:
        print(e)
        e = r.read()


if __name__ == '__main__':
    main()
