# rxvpntoggle
VPN toggle for indicator for Xubuntu.


### Installation
To install locally in editable mode (this has to be manually uninstalled):  
`pip3 install --user -e .`

To install from github:  
`pip3 install --user git+https://github.com/aldencolerain/rxvpntoggle.git#egg=rxvpntoggle`

To uninstall:  
`pip3 uninstall rxvpntoggle`

### Running on startup in Xubuntu:
**Before running the application must be configured!**
`rxvpntoggle configure`

Click on *Whisker Menu* and open *Session and Startup*.  Then select the *Application Autostart*
tab and create a new entry that runs `rxvpntoggle start` on startup.


### Running tests
To run all tests:  
`nox`

To run a specific test suite:  
`nox -e lint`

To run a specific test module:  
`nox -e test -- -k test_calc` (To see print statements of passing tests use the `-s` flag)


### VPN Setup
* Setup server with [PiVPN](https://www.pivpn.io/) selecting [WireGuard](https://www.wireguard.com/) as vpn.
* Install wireguard on client `sudo apt install wireguard`.
* Create client config on vpn server using pivpn command line.
* Copy config to client into `/etc/wireguard` folder.
* Make sure config file is owned by root `sudo chown root:root /etc/wireguard/example.conf`
* Check that vpn works using `sudo wg-quick up example` etc.


### Running VPN Manually
```
sudo wg-quick up example
sudo wg
sudo wg-quick down example
```

### Debugging DNS
  * Make sure that the client and vpn network subnets don't overlap.
  * Is the router accessible on 192.168.1.1 or 192.168.2.1 you might be having a
  clash with the remote vpn subnet and the local lan subnet.
  * Did you make sure to add your router or local dns server to pivpn's list of dns?
  * Use `nslookup example 192.168.2.1` to check a specific dns server for name resultion
  * Or `host example` for name resolution
  * Or `dig +search example` for name resolution (+search ensures it uses search domain)
  * Check network manager dns `nmcli device show | grep DNS`
  * Use `watch cat /run/systemd/resolve/resolv.conf` to see generated configuration
  * Use `sudo systemd-resolve --status` to see current dns servers
  * Check vpn tunnel adapters dns `systemd-resolve --status | grep -A8 tun0`
  * Restart systemd-resolved `sudo service systemd-resolved restart`
  * Check network manager dns `nmcli device show | grep DNS`
