#!/usr/bin/python

# apt-get install python-appindicator
import os
import time
import signal
import threading
from . import vpn
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator


# config
APPINDICATOR_ID = 'vpntoggle'
ICONS_DIR = os.path.dirname(os.path.realpath(__file__))
ENABLED = os.path.join(ICONS_DIR, 'icons/vpn-enabled.svg')
DISABLED = os.path.join(ICONS_DIR, 'icons/vpn-disabled.svg')
ERROR = os.path.join(ICONS_DIR, 'icons/vpn-error.svg')
WARNING = os.path.join(ICONS_DIR, 'icons/vpn-warning.svg')
SUCCESS = os.path.join(ICONS_DIR, 'icons/vpn-success.svg')
HAPPY = os.path.join(ICONS_DIR, 'icons/vpn-happy.svg')


class Toggle:

    def __init__(self):
        # prevent keyboard interrupt error from hitting command line
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        # create app indicator
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, DISABLED,
            appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.status = 'uncertain'

    # enable vpn
    def enable(self, _):
        vpn.up()
        self.indicator.status = 'on'
        self.indicator.set_icon(ENABLED)

    # disable vpn
    def disable(self, _):
        vpn.down()
        self.indicator.status = 'off'
        self.indicator.set_icon(DISABLED)

    # update widget status
    def update(self, status):
        # debug statement
        print(self.indicator.status, status)
        # if we don't know our indicator's state update it
        if self.indicator.status == 'uncertain' and status == 'down':
            self.indicator.status = 'off'
        elif self.indicator.status == 'uncertain' and status != 'down':
            self.indicator.status = 'on'

        # if we disabled the indicator and vpn is down show disabled
        if self.indicator.status == 'off' and status == 'down':
            self.indicator.set_icon(DISABLED)
        # show red if we enabled vpn but the wireguard device is down
        elif status == 'down':
            self.indicator.set_icon(ERROR)
        # show orange if the wireguard device is up but ip is wrong or can't reach google.com
        elif status == 'disconnected':
            self.indicator.set_icon(WARNING)
        # show green if we have expected ip and we can ping google
        elif status == 'connected':
            self.indicator.set_icon(SUCCESS)
        # show purple if we are connected and we could also ping a known internal lan ip/host
        elif status == 'localized':
            self.indicator.set_icon(HAPPY)

    # close widget
    def close(self, _):
        vpn.down()
        # kill monitor thread?
        gtk.main_quit()

    # start widget
    def start(self):
        # start monitor
        thread = threading.Thread(target=self.monitor)
        thread.daemon = True
        thread.start()

        # start widget
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build())
        gtk.main()

    # build widget
    def build(self):
        menu = gtk.Menu()

        enable_item = gtk.MenuItem('Enable')
        enable_item.connect('activate', self.enable)
        menu.append(enable_item)

        disable_item = gtk.MenuItem('Disable')
        disable_item.connect('activate', self.disable)
        menu.append(disable_item)

        quit_item = gtk.MenuItem('Close')
        quit_item.connect('activate', self.close)
        menu.append(quit_item)

        menu.show_all()
        return menu

    # monitor vpn status and update indicator
    def monitor(self):
        while True:
            # don't check status if its off (I guess we could also check less frequently)
            time.sleep(3)
            if self.indicator.status != 'off':
                self.update(vpn.status())

toggle = Toggle()
