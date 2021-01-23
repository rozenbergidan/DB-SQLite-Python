import sys

from ApplicationLayer.Session import Session

def main(args):
        # TODO: i changed here
        config = args[1]
        orders = args[2]
        output = args[3]
        ses = Session(config, orders, output)
        ses.run()

if __name__ == '__main__':
        main(sys.argv)

