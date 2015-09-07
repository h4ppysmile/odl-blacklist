#!/usr/bin/python



import requests
import json

###global vars
ctrlAddr= 'http://127.0.0.1:8181'
ctrlUser= "admin"
ctrlPass= "admin"
auth= ( ctrlUser, ctrlPass)
headers= { 'Content-Type': 'application/xml', 'Accept':'application/xml'}
###



class FlowMod:
    url= ctrlAddr+ "/restconf/config/opendaylight-inventory:nodes/node/{OVS_NAME}/table/{TABLE_ID}/flow/{FLOW_ID}"
    TABLE_ID= 0
    PRIO= 200
    OVS_NAME= 'openflow:1'

    def genFlowId( self, nodeName):
        return 'disable:'+nodeName
    def disableNode( self, node):
        flow_id= self.genFlowId( node.getNodeId())
        flow= open( 'data', 'r').read().format( TABLE_ID= self.TABLE_ID, FLOW_ID= flow_id, MAC= node.getNodeMac(), FLOW_NAME= node.getNodeId(), PRIO= self.PRIO)

        url= self.url.format( OVS_NAME= self.OVS_NAME, TABLE_ID= self.TABLE_ID, FLOW_ID= flow_id)
        print url
        r= requests.put( url, headers= headers, auth= auth, data= flow)
        print r
    def enableNode( self, node):
        flow_id= self.genFlowId( node.getNodeId())
        url= self.url.format( OVS_NAME= self.OVS_NAME, TABLE_ID= self.TABLE_ID, FLOW_ID= flow_id)
        r= requests.delete( url, headers= headers, auth= auth)
        print r


class Node:
    mac= ''
    nodeId= ''

    def __init__( self, nodeObj):
        self.nodeObj= nodeObj
        self.setNodeId()
        self.setNodeMac()
    def setNodeId( self):
        self.nodeId= self.nodeObj[ 'node-id']
    def setNodeMac( self):
        for key in self.nodeObj:
            if key== 'host-tracker-service:addresses':
                self.mac= self.nodeObj[ key][ 0][ 'mac']
    def getNodeId( self):
        return self.nodeId
    def getNodeMac( self):
        return self.mac

class Topo:
    topo= ""

    def __init__( self):
        self.updateTopo();
        self.buildNodes()
    def updateTopo( self):
        url= ctrlAddr+ "/restconf/operational/network-topology:network-topology"
        self.topo= requests.get( url, auth= auth).text
        if self.connectedController( self.topo):
            self.topo= json.loads( self.topo)
        else:
            print '[ ERR ] no controller connected.'
            exit( 1)
    def buildNodes( self):
        nodes= self.topo[ 'network-topology']['topology'][0]['node']
        self.nodes= {}
        for node in nodes:
            newNode= Node( node)
            self.nodes[ newNode.getNodeId()]= newNode
    def printNodes( self):
        for node in self.nodes:
            print 'node-id:', node, ',mac: ', self.nodes[ node].getNodeMac()
    def nodeExist( self, nodeId):
        return self.nodes.has_key( nodeId)
    def getNode( self, nodeId):
        if self.nodeExist( nodeId):
            return self.nodes[ nodeId]
        return -1
    def connectedController( self, url):
        return url.find( 'node')!= -1


def intro():
    print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
    print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ODL blacklist app <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
    print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

    print 'usage:'
    print '\tdisable[enable] HOST_NAME'
    print '\tlist'




if __name__== '__main__':

    topo= Topo()
    flowmode= FlowMod()

    intro()

    i= raw_input( ">>")
    while ( i!= 'end'):
        i= i.split()
        print i[ 0]
        if i[ 0]== 'list':
            topo.printNodes()
        elif i[ 0]== 'disable':
            if topo.nodeExist( i[ 1]):
                flowmode.disableNode( topo.getNode( i[ 1]))
            else:
                print '[ ERR ] no such node exist'
        elif i[ 0]== 'enable':
            if topo.nodeExist( i[ 1]):
                flowmode.enableNode( topo.getNode( i[ 1]))
            else:
                print '[ ERR ] no such node exist'
        else:
            print '[ ERR ] wrong cmd'

        i= raw_input( ">>")
