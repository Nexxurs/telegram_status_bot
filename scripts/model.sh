#!/usr/bin/env bash
if command -v vcgencmd &> /dev/null; then
    sys_rev=$(awk '/Revision/ {print $3}' < /proc/cpuinfo)
    case "$sys_rev" in
      000[2-6]) sys_model=" 1, Model B";; # 256MB
      000[7-9]) sys_model=" 1, Model A" ;; # 256MB
      000d|000e|000f) sys_model=" 1, Model B";; # 512MB
      0010|0013) sys_model=" 1, Model B+";; # 512MB
      0012|0015) sys_model=" 1, Model A+";; # 256MB
      a0104[0-1]|a21041|a22042) sys_model=" 2, Model B";; # 1GB
      900021) sys_model=" 1, Model A+";; # 512MB
      900032) sys_model=" 1, Model B+";; # 512MB
      90009[2-3]|920093) sys_model=" Zero";; # 512MB
      9000c1) sys_model=" Zero W";; # 512MB
      a02082|a[2-3]2082) sys_model=" 3, Model B";; # 1GB
      *) sys_model="" ;;
    esac
    sys_type="Raspberry Pi$sys_model"
else
    source "/etc/os-release"
    CODENAME=$(sed 's/[()]//g' <<< "${VERSION/* /}")
    sys_type="${NAME/ */} ${CODENAME^} $VERSION_ID"
fi

echo $sys_type