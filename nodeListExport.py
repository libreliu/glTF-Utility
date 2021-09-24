#!/usr/bin/env python3

import sys
from gltflib import GLTF, gltf
from gltflib.models.gltf_model import GLTFModel

def nodeListDump(gltfObject: GLTFModel, showGCLNameExt=False, dumpFunc=print):
    defaultScene = gltfObject.model.scenes[0]
    rootNodes = defaultScene.nodes

    # build dag
    nodeParent = {}
    workingQueue = [idx for idx in rootNodes]
    while len(workingQueue) > 0:
        workingNode = workingQueue.pop()
        if gltfObject.model.nodes[workingNode].children is not None:
            for child in gltfObject.model.nodes[workingNode].children:
                assert(child not in nodeParent.keys())
                nodeParent[child] = workingNode
                workingQueue.append(child)
    

    # traverse in Childs1->...->ChildsN->Self manner
    def getName(node):
        name = gltfObject.model.nodes[node].name
        return name if name is not None else "None"

    def getPath(node):
        result = f"{getName(node)}"
        while node not in rootNodes:
            node = nodeParent[node]
            result = f"{getName(node)}->{result}"
        return result

    def traverse(node):
        childs = gltfObject.model.nodes[node].children
        # dump information about myself
        dumpFunc(f"{getPath(node)}")
        if childs is not None:
            for child in childs:
                traverse(child)
    
    for rootNode in rootNodes:
        traverse(rootNode)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} gltf_filepath")
        sys.exit(1)

    gltfFilename = sys.argv[1]
    gltfObject = GLTF.load(gltfFilename)

    nodeListDump(gltfObject)