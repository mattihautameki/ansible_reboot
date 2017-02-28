# Ansible Reboot helper

This script can be executed as local action task after a host was sent the reboot command. The script checks the host constantly every 2 seconds and returns with exitcode 0 when the host was online, went offline and comes back online. Either pings or connections to tcp ports are used to check the hosts status. 
