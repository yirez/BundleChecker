from classes.helpers import LoopHelper
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''Usage python PATHTO/bundle_check.py MBSM_ROOTDIR ''')
    parser.add_argument('path', nargs='*', default=[1], help='MBSM root dir to check for bundles')
    args = parser.parse_args()

    print("Bundle check in dir: " + sys.argv[1])
    LoopHelper.LoopHelper().loop_through(sys.argv[1])
