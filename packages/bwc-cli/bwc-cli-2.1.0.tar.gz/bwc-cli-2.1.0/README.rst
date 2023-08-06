BWC CLI
=======

.. image:: https://circleci.com/gh/StackStorm/bwc-cli.svg?style=shield&circle-token=b2b7d6b3d2a39a2413aebf9cbed0bd8cf3ab9def
    :target: https://circleci.com/gh/StackStorm/bwc-cli

CLI for Brocade Workflow Composer.
----------------------------------

**bwc** is the main CLI application. Currently for 2.0 the only solution
that we ship is IP Fabric (ipf). The goal is to allow the cli to cater
to multiple application and hence the 'bwc ipf' nouns in the commands.
The output of the commands will be updated as the implementation gets
completed

Currently the commands available are are follows:

1. **bwc ipf show** Show Fabric state or topology configuration .
2. **bwc ipf inventory** Register, Delete, Update or list switches.
3. **bwc ipf workflow** Execute Workflows on the switches.
4. **bwc ipf fabric** Add, Delete and Show Fabric/Fabric Config.

For the '**ipf show**' command here are the options available:

-  **bwc ipf show config bgp** [--fabric=fabric name] \| [--host=ip address] - Show the BGP
   configuration of the specified fabric or host
-  **bwc ipf show topology** [fabric=fabric name] [--format=<pdf, jpeg, png, svg>] [--render\_dir ]
   -Draws the topology of the specified fabric

For the '**ipf inventory**' command here are the sub-options
available:

-  **bwc ipf inventory register** [host=ip address] [fabric=fabric name][user=<user_name>] [passwd=<password>] -
   Register a switch to the specified fabric
-  **bwc ipf inventory delete** [host=ip address] - Delete the specified device
   from the inventory
-  **bwc ipf inventory update** [--fabric=fabric name \| --host=ip address] - Update the
   inventory details of the switch or the entire fabric
-  **bwc ipf inventory list** [--fabric=fabric name \| --host=ip address] - List all the
   devices in the fabric or the specified switch details
-  **bwc ipf inventory show vcs links** [fabric=fabric name] - Display VCS links
   for the specified fabric
-  **bwc ipf inventory show lldp** [fabric=fabric name] - Display LLDP details for
   the specified fabric

For the '**ipf fabric**' command here are the sub-options available:

-  **bwc ipf fabric add** [fabric=fabric name] - Create a new fabric
-  **bwc ipf fabric delete** [fabric=fabric name] - Delete an existing fabric
-  **bwc ipf fabric config show** [fabric=fabric name] - Display specified fabric
   configurations
-  **bwc ipf fabric config set** [fabric=fabric name] [key=key] [value=value] - Set (add / edit)
   current fabric configuration
-  **bwc ipf fabric config delete** [fabric=fabric name] [key=] - Delete fabric
   configuration key.

For the '**ipf workflow**' command here are the sub-options:

-  **bwc ipf workflow bgp** [fabric=fabric name] - Executed the IP Fabric workflow.
