# Follow step by step these instructions

# First Update Raspbian Linux
sudo apt-get update

Execute the following command for CMAKE and MAKE functionalities (Should take 20+ minutes to be done!)
sudo apt-get install -y git cmake libgcrypt11-dev libjson0-dev libcurl4-openssl-dev libexpat1-dev libboost-filesystem-dev libboost-program-options-dev libboost-all-dev build-essential automake autoconf libtool pkg-config libcurl4-openssl-dev intltool libxml2-dev libgtk2.0-dev libnotify-dev libglib2.0-dev libevent-dev checkinstall qt4-dev-tools

# Open a folder for the sources
mkdir -p /home/pi/sources

# Go to the sources folder
cd /home/pi/sources

# There is one dependency that must be installed from source:
git clone git://github.com/lloyd/yajl yajl

# Go to that new folder
cd yajl

# Complete the installation
./configure
cmake .
make
sudo checkinstall --nodoc --default

# Now build the GDrive executable
sudo git clone git://github.com/Grive/grive.git

# Now go to the new folder GDrive and complete the installation
cd ./grive
sudo cmake .
sudo make

# Create a new folder for the executable to be accessible and Auth file to be located
mkdir -p /home/pi/google-drive

# Go to the Google Drive folder and copy the Grive executable
cp /home/pi/sources/grive/grive/grive /home/pi/google-drive
