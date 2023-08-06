import os
from cinit.templates import base_makefile


def main():

    base_dirs = ('src', 'include')

    for d in base_dirs:
        if not os.path.exists(d):
            print 'Creating directory: {}'.format(d)
            os.mkdir(d)

    make_file = 'Makefile'

    if not os.path.exists(make_file):

        with open(make_file, 'w') as make:
            print 'Generating Makefile'
            make.write(base_makefile.substitute())


if __name__ == "__main__":
    main()
