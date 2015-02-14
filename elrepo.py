#!/usr/bin/python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Copyright 2015 by Dag Wieers

from yum.plugins import TYPE_CORE
import glob
import fnmatch

requires_api_version = '2.1'
plugin_type = (TYPE_CORE,)

def init_hook(conduit):
    global elrepo_devices
    elrepo_devices = []

    ### Scan for (acpi, dmi, pci, serio, usb) hardware devices
    for file in glob.glob('/sys/bus/*/devices/*/modalias') + \
                glob.glob('/sys/devices/virtual/dmi/id/modalias'):
        modalias = open(file).read()
        elrepo_devices.append('modalias(' + modalias[:-1] + ')')

def exclude_hook(conduit):
    global elrepo_matches
    elrepo_matches = []

    def find_matches(pkg, values, matchfor=None):
        if pkg.name in [ p.name for p in elrepo_matches ]: return
        for provide in values:
            if not provide.startswith('modalias('): continue
            for modalias in elrepo_devices:
                filter = provide.split()[0]
                if fnmatch.fnmatch(modalias, filter):
                    elrepo_matches.append(pkg)

                    ### If we get a match for this package, don't bother with other provides
                    return

    conduit._base.searchPackageProvides(['modalias(*)', ], callback=find_matches, callback_has_matchfor=True)

    if elrepo_matches:
        conduit.info(1, 'ELRepo hardware support detected using:')
        for pkg in elrepo_matches:
            conduit.info(1, ' * %s (%s)' % (pkg.name, pkg.repo.id))
