#!/usr/bin/env python
# -*- python -*-
# -*- coding: <utf-8> -*-
"""
=head1 NAME

arexx sensor readout

=head1 AUTHOR

05-03-2021 Arnold Meissner

Inspired by code written by Peter Palfrader and the ipmi_sensor_ wildcard plugin

=head1 CONFIGURATION

requires a running pylarexx daemon to read data from arexx sensor

=head1 LICENSE

GNU GPLv2 or any later version

=begin comment

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

=end comment

=head1 BUGS

=head1 MAGIC MARKERS

=cut
"""

# sys required to read command line argument
import sys

sensorList = {
"Temperature" :
    {
    "20444"  : {"label" : "Schlafzimmer"},
    "10331"  : {"label" : "Aussen"},
    "10855"  : {"label" : "Dachgeschoss"},
    "11809"  : {"label" : "Gewaechshaus"},
    "12346"  : {"label" : "Buero"},
    "11905"  : {"label" : "Warmwasser"},
    },
"Humidity" :
    {
    "20444"  : {"label" : "Schlafzimmer"},
    },
"CO2" :
    {
    "12346"  : {"label" : "Buero"},
    }
}

# Configure munin graph
# Read sensor information from dict
def config(quantity):
    print "multigraph %s" % (quantity)
    if quantity == "Temperature":
        print "graph_title Temperatur"
        print "graph_vlabel Temperatur / K"
        print "graph_info Temperaturen"
    elif quantity == "Humidity":
        print "graph_title Luftfeuchte"
        print "graph_vlabel RH / %"
        print "graph_info Relative Feuchtigkeit"
    elif quantity == "CO2":
        print "graph_title CO2-Konzentration"
        print "graph_vlabel CO2 / ppm"
        print "graph_info CO2-Konzentrationen"
    elif quantity == "Signal":
        print "graph_title Signalstaerke"
        print "graph_vlabel RF / %"
        print "graph_info Staerke des Funksignals"
        quantity="Temperature"

    print "graph_category Umweltdaten"
    for name in sensorList[quantity]:
        label = sensorList[quantity][name]["label"]
        print "%s.label %s" % (name, label)

def dataStorage(quantity):
    # all units stored in one file
    dataStorage="/var/run/pylarexx"
    fileName = "%s/sensor.dat" % (dataStorage)
    return fileName

# Print data
def report(quantity):
    print "multigraph %s" % (quantity)
    data = []
    try:
        with open(dataStorage(quantity), "r+") as file:
            rl = file.readlines()
            for line in rl[:]:
                # ID, raw data, value unit, time, signal strength, label, unit
                (key, raw, valueText, time, signal, label, unitText) = line.split(',')
                try:
                    signal = int(signal)
                    if (type(signal) == int) and (quantity in unitText):
                        (value, unit) = valueText.split(' ')
                        data.append( [key, time, value] )
                    elif (type(signal) == int) and (quantity == "Signal"):
                        data.append( [key, time, signal] )
                except:
                    continue

        # keep data from 300 sec. for max. 11 sensors
        # (300s sampled every 10s * 11 sensors = 330 lines)
        #file.seek(0,0)   # rewind the file
        #file.truncate(0)  # erase all of it
        #file.write("".join(rl[-330:]))  # write the last 330 lines again
    except:
        print "file open failed"

    for line in data:
        key = line[0]
        time = line[1]
        value = line[2]
        print "%s.value %s:%s" % (key, time, value)

# Munin autoconf - does nothing at the moment
def autoconf():
    try:
        data = report("Temperature")
    finally:
        if data:
            print "yes"
        else:
            print "no"


def main():
    # define which data type to collect
    # If this is called by liq_DataType.py, then only DataType related values are reported.
    # Otherwise, all known types of data are reported in multigraph style
    pluginName = sys.argv[0]
    if "Temperature" in pluginName:
        quantity = "Temperature"
    elif "Humidity" in pluginName:
        quantity = "Humidity"
    elif "CO2" in pluginName:
        quantity = "CO2"
    elif "Signal" in pluginName:
        quantity = "Signal"

    if len(sys.argv)>1:
        command = sys.argv[1]
    else:
        command = ""
    if command=="autoconf":
        autoconf()
    #elif command=="suggest":
    #    suggest()
    elif command=='config':
        config(quantity)
    #elif command=='debug':
    #    debug()
    else:
        report(quantity)

if __name__ == "__main__":
    main()

