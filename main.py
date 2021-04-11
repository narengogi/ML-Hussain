
# 1)  The  generator  function  generatesninitial  randompaintings.
# 2)  The  selector  function  select some of  the  initial  randompaintings to mate and produce child paintings.
# 3)  The  crossover  function  takes  two  selected  paintings and  combines  their  strokes,  half  from  one  and  halffrom  the  other,  to  create  a  child  painting.  It  repeatsthis  process  until  all  of  the  selected  paintings  havebeen mated.
# 4)  Another  selector  function  selectsorandom  membersof the population.
# 5)  The mutation function mutates theseomembers.
# 6)  The simulator then stochastically kills offmpaintingsfrom the population.
# 7)  Go  back  to  step  2  and  repeat  until  a  predeterminednumber of iterations has been met.
# 8)  Render the most fit, according to the fitness function,of the population and output it as the final result.
import cv2 as cv
import os
import time
import numpy
import random


class Main:
    def __init__(self, imgPath, generations=20, epochs=20, brushes=1):
        self.image = cv.imread(imgPath)     # Read Image
        self.generations = generations      # Set Number of Generations Per Iteration
        # We need this to keep changing the brush sizes and obtain finer details after every Iteration
        self.epochs = epochs
        self.brushes = str(brushes)         # Select Brushes
        self.generate()

    # Returns Different Size and Number of Strokes Depending on the Epoch
    def getStrokes(self, epoch, strokes, relativeStrokeSizes):
        allStrokes = []
        numberOfStrokes = 24 + 2 * epoch

        for stroke in self.strokes:
            stroke = cv.resize(stroke, None, fx=max(
                0.1, 0.8/epoch), fy=max(0.1, 0.8/epoch), interpolation=cv.INTER_AREA)
            rows, cols, ch = stroke.shape
            for i in range(1, numberOfStrokes//5 + 1):
                M = cv.getRotationMatrix2D(
                    ((cols-1)/2.0, (rows-1)/2.0), 360/i, 1)
                allStrokes.append(cv.warpAffine(stroke, M, (cols, rows)))

        random.shuffle(allStrokes)
        return allStrokes

    def generate(self):                     # This is The Main Function
        # Read the strokes and define their properties
        strokes = os.listdir("strokes/set" + self.brushes)
        self.strokes = []
        for stroke in strokes:
            self.strokes.append(
                cv.imread("strokes/set" + self.brushes + '/' + stroke))
        relativeStrokeSizes = []
        for stroke in self.strokes:
            y = self.image.shape[0] / stroke.shape[0]
            x = self.image.shape[1] / stroke.shape[1]
            relativeStrokeSizes.append([y, x])

        for epoch in range(self.epochs):
            self.allStrokes = self.getStrokes(epoch+1, self.strokes, relativeStrokeSizes)
            
        #     for generation in range(self.generations):


initiate = Main("sample.png")
print(initiate.image.shape)
