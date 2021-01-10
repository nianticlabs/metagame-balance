from Util.Recorders import Recorder


def main():
    r = Recorder(name="random_agent")
    r.open()
    e = r.read()
    while e[1] != -1:
        print(e)
        e = r.read()


if __name__ == '__main__':
    main()
