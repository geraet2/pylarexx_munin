How to use:

Requirements:
- a running instance of munin-node (munin-node collects the data whereas munin provides RRD database and graphical frontend)
- pylarexx daemon to read data from Arexx data logger (via USB)
- Arexx sensors and data logger

How to install:
Copy the content of munin/ into your munin-node instance, usually /etc/munin/.

plugins/ does contain the code to read and process data from pylarexx daemon.
  The main plugin is reading temperature values. Other sensor types are optional,
  the code recognizes the type of data by the plugin name. You may delete the symbolic
  links which are not used or required (CO2, humidity and sensor strength).

plugin-conf.d/ contains configuration to run the plugin as unprivileged user pylarexx.
  This user is created when installing the pylarexx daemon.
