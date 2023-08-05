Net-Survey
==========

Net-Sruvey allows you to deploy agents throughout your infrastructure to
gather network, interface, and ip configuration with the end goal of running
a smart scan of basica reachability and port scans.  Server and agents deployed
will progress through a seires of steps once started:

* Gathering of interface and network information.
* Updating the central server.
* Processing of topology information.
* Distribution of topology data to clients.
* Clients then proceed to scanning of neighboring hosts.
* Retrieeval of test results.

The benefit of Net-Survey is to provide testing in situations where networks
are isolated, i.e. a backend storage network.

Installation
============

Simple install via pypi:

```
pip install net-survey
```

Usage
=====

Server start:

```
net-survey --mode server --inventory_file <path> --config-file <path>
```

Client start:

```
net-survey --config-file <path>
```