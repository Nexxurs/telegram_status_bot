import helper
import sys

if __name__ == '__main__':
    args = sys.argv[1:]
    msg = ' '.join(args)
    helper.send_admins(msg)

