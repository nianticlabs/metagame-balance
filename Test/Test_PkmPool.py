from Engine.PkmPoolGenerator import StandardPkmPoolGenerator


def main():
    pool_gen = StandardPkmPoolGenerator(10, 100)
    pool = pool_gen.get_pool()
    for pt in pool:
        print(pt)
        print()


if __name__ == '__main__':
    main()
