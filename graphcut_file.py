#Rohit Sriram Muniganti
#DF05298
#CMSC641 Project 1 Graphcut Images
#This is the python code used for creating the final graph cut image file.

#Import the necessary modules and libraries. 
import argparse
import os
import cv2
import matplotlib.pyplot as plt
import maxflow
import networkx as nx
import numpy as np

#Functions for cutting the graph image
class CuttingGraph:

    def __init__(self, pic1, pic2, mask, initial_graph_save=False):
    
        assert (pic1.shape == pic2.shape), \
            f"pic1 and pic2 resolution/dimensions must be equal: {str(pic1.shape)} != {str(pic2.shape)}"

        # maxflow initializing
        pictureGraph = maxflow.Graph[float]()
        IDofNodes = pictureGraph.add_grid_nodes((pic1.shape[0], pic1.shape[1]))

        self.calculateWeightsOfEdges(pic1, pic2)  

        # edges are added aside terminal
        height_zone_patch = pic1.shape[0]
        width_zone_patch = pic1.shape[1]
        for indexOfRow in range(height_zone_patch):
            for indexOfColumn in range(width_zone_patch):
                if indexOfColumn + 1 < width_zone_patch:
                    weight = self.weightOfEdge[indexOfRow, indexOfColumn, 0]
                    pictureGraph.add_edge(IDofNodes[indexOfRow][indexOfColumn],
                                   IDofNodes[indexOfRow][indexOfColumn + 1],
                                   weight,
                                   weight)

                if indexOfRow + 1 < height_zone_patch:
                    weight = self.weightOfEdge[indexOfRow, indexOfColumn, 1]
                    pictureGraph.add_edge(IDofNodes[indexOfRow][indexOfColumn],
                                   IDofNodes[indexOfRow + 1][indexOfColumn],
                                   weight,
                                   weight)

                # Edge capacities of the terminals are added to pic1 and pic2
                if np.array_equal(mask[indexOfRow, indexOfColumn, :], [0, 255, 255]):
                    pictureGraph.add_tedge(IDofNodes[indexOfRow][indexOfColumn], 0, np.inf)
                elif np.array_equal(mask[indexOfRow, indexOfColumn, :], [255, 128, 0]):
                    pictureGraph.add_tedge(IDofNodes[indexOfRow][indexOfColumn], np.inf, 0)

        # Plotting the graph
        if initial_graph_save:
            Network_x_G = pictureGraph.get_nx_graph()
            self.Plotting2Dgraph(Network_x_G, (height_zone_patch, width_zone_patch))

        # Running the maxflow algorithm
        flow = pictureGraph.maxflow()
        self.segment = pictureGraph.get_grid_segments(IDofNodes)

    def calculateWeightsOfEdges(self, pic1, pic2):
        
        #Calculate the edge weights based on the dimensions

        
        self.weightOfEdge = np.zeros((pic1.shape[0], pic1.shape[1], 2))

        # For the vector operations matrices are shifted
        pic1ShiftLeft = np.roll(pic1, -1, axis=1)
        pic2ShiftLeft = np.roll(pic2, -1, axis=1)
        pic1ShiftUp = np.roll(pic1, -1, axis=0)
        pic2ShiftUp = np.roll(pic2, -1, axis=0)

        NumericStablity = 1e-10  # For the numerical stability

        # Weightage Horizontally
        TheHorzWt = np.sum(np.square(pic1 - pic2, dtype=np.float) +
                                   np.square(pic1ShiftLeft - pic2ShiftLeft, dtype=np.float),
                                   axis=2)

        TheHorzFactorNorm = np.sum(np.square(pic1 - pic1ShiftLeft, dtype=np.float) +
                                        np.square(pic2 - pic2ShiftLeft, dtype=np.float),
                                        axis=2)

        self.weightOfEdge[:, :, 0] = TheHorzWt / (TheHorzFactorNorm + NumericStablity)

        # Weightage Vertically
        TheVertWt = np.sum(np.square(pic1 - pic2, dtype=np.float) +
                                 np.square(pic1ShiftUp - pic2ShiftUp, dtype=np.float),
                                 axis=2)

        TheVertFactorNorm = np.sum(np.square(pic1 - pic1ShiftUp, dtype=np.float) +
                                      np.square(pic2 - pic2ShiftUp, dtype=np.float),
                                      axis=2)

        self.weightOfEdge[:, :, 1] = TheVertWt / (TheVertFactorNorm + NumericStablity)

    def Plotting2Dgraph(self, graph, StructOfNode,
                      ThePlotofWts=True,
                      TheTerminalPlot=True,
                      SizeOfFont=7):
        

        X, Y = np.mgrid[:StructOfNode[0], :StructOfNode[1]]
        aux = np.array([Y.ravel(), X[::-1].ravel()]).T
        PositionsPresent = {i: v for i, v in enumerate(aux)}
        PositionsPresent['p'] = (-1, StructOfNode[0] / 2.0 - 0.5)
        PositionsPresent['q'] = (StructOfNode[1], StructOfNode[0] / 2.0 - 0.5)

        plt.show()
        NetwXgraph = graph.get_nx_graph()
        print("networkX graph created")
        if not TheTerminalPlot:
            NetwXgraph.DeleteNodes(['p', 'q'])

        plt.clf()
        nx.draw(NetwXgraph, pos=PositionsPresent)

        if ThePlotofWts:
            LabelEdges = {}
            for a, b, c in NetwXgraph.edges(data=True):
                LabelEdges[(a, b)] = c['weight']
            nx.NetworkxEdgeLabelsDrawing(NetwXgraph,
                                         pos=PositionsPresent,
                                         LabelEdges=LabelEdges,
                                         label_pos=0.3,
                                         SizeOfFont=SizeOfFont)

        plt.axis('equal')
        plt.show()
    #blending the images
    def mix(self, pic1, pic2):
        
        pic2[self.segment] = pic1[self.segment]

        return pic2


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='imageDirectory', required=True, help='Saved Path of pic1 & pic2 Images.')
    args = parser.parse_args()

    # This takes in the images along with the mask.
    imageDirectory = args.imageDirectory
    pic1 = cv2.imread(os.path.join(imageDirectory, 'pic1.jpg'))
    pic2 = cv2.imread(os.path.join(imageDirectory, 'pic2.jpg'))
    mask = cv2.imread(os.path.join(imageDirectory, 'MaskedPic.jpg'))

    # using the mincut function.
    FinalGraphCut = CuttingGraph(pic1, pic2, mask)

    # Creating the output.
    pic2 = FinalGraphCut.mix(pic1, pic2)
    cv2.imwrite(os.path.join(imageDirectory, "output.jpg"), pic2)
