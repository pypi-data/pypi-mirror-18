#!/bin/bash

set -e

# Clean / test fresh installs:
# make clean && rm /usr/local/lib/libvnc* || rm /usr/local/include/rfb || echo clean

if [[ "$OSTYPE" == "darwin"* ]]; then
        which -s brew
        if [[ $? != 0 ]] ; then
            echo ""
            echo "ERROR: Homebrew is not installed, please install from http://brew.sh"
            echo ""
            exit 1
        else
            brew update
        fi
        brew install libgcrypt libtool
        cd libvncserver
        autoreconf -fiv
        brew install openssl # TODO: Test if this is needed on macOS Sierra

        # libvncserver warns reduced performance without jpeg-turbo,
        # BUT in my testing on MBP 2015 El Capitan, libjpeg consistently yielded 15% more vnc
        # updates per second on GTAV 800x600 compress level 9
        brew install libjpeg

        brew install libpng
        ./libserver-configure.mac --with-ssl=/usr/local/opt/openssl
        make
        make install
fi