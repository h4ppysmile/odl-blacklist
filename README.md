#Introduction
As you know opendaylight comes with a list of plugins which help you configure how it works through **REST**. List of all installed plugins and their REST methods on an odl instance is accessible at :

**http://CONTROLLER_IP:8181/apidoc/explorer/index.html**

Which at the time of writing, this was the only tutorial I found. 

This app is a blacklist tools, written using plugins:
> opendaylight-inventory(2013-08-19) 

> network-topology(2013-07-12) 

And the usage is:
```
list
disable[enable] HOST_NAME
```

#How it works?
Project contains two file: **connectionMannager.py** containing the code, and **data.xml** containing body of massage sent to controller to write flow.
##Flow of operation:
* In ``` Topo.updateTopo() ``` topology is gotten in json format by **GET**ing  ``` /restconf/operational/network-topology:network-topology ```, using 
``` requests.get( URL) ```. Gotten topology is parsed using ``` json.load() ```

* In ``` Topo.buildNodes() ``` we build a dictionary of nodes with their id as keys 

* Enabling nodes is implemented by writing a flow to discard packets coming from wanted node and disabling by deleting this flow.
**PUT**ed massage:
  * Header:
  
    ```
    { 'Content-Type': 'application/xml', 'Accept':'application/xml'}
    ```
  
  * Authentication:
  
     Is in basic authentication

  * Body:
  
    body is the **data.xml** file which is filled in run time.
    Make sure table id and node id of URL and the body be same.
