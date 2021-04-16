
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
import numpy as np
import random


class Main:
    def __init__(self, imgPath, generations=20, epochs=3, brushes=1):
        self.image = cv.imread(imgPath)     # Read Image
        self.generations = generations      # Set Number of Generations Per Iteration
        # We need this to keep changing the brush sizes and obtain finer details after every Iteration
        self.epochs = epochs
        self.brushes = str(brushes)         # Select Brushes
        self.imageHeight, self.imageWidth, _ = self.image.shape
        self.population = []
        self.children = []
        self.allStrokes = []
        self.generate()                     # Begin evolution

    # Returns Different Size and Number of Strokes Depending on the Epoch
    def getStrokes(self, epoch, strokes):
        allStrokes = []
        numberOfStrokes = 2

        for stroke in self.strokes:
            stroke = cv.resize(stroke, None, fx=0.2, fy=0.2, interpolation=cv.INTER_AREA)
            rows, cols, ch = stroke.shape
            for i in range(1, numberOfStrokes+1):
                M = cv.getRotationMatrix2D(
                    ((cols-1)/2.0, (rows-1)/2.0), 360/i, 1)
                allStrokes.append(cv.warpAffine(stroke, M, (cols, rows)))

        # random.shuffle(allStrokes)
        return allStrokes

    # Paints strokes on the canvas
    def paintCanvas(self, canvas, strokeHeight, strokeWidth, epoch):
        canvas[1] = []
        for stroke in self.allStrokes:
            y = random.randint(0, self.imageHeight-strokeHeight)
            x = random.randint(0, self.imageWidth-strokeWidth)
            canvas[0][y:y+strokeHeight, x:x+strokeWidth] += stroke
            canvas[1].append([y, x])

        return canvas

    # Calculates fitness in comparison to the comparisonImage
    def calculateFitness(self, canvas, comparisonImage):
        diff1 = cv.subtract(canvas, comparisonImage)
        diff2 = cv.subtract(comparisonImage, canvas)
        totalDiff = cv.add(diff1, diff2)
        totalDiff = np.sum(totalDiff)
        return(totalDiff)

    # Selects the fittest of the bunch
    def selectFit(self, varianceValues):
        length = len(varianceValues)
        fit = []
        unfit = []
        for i in range(length//3):
            unfit.append(varianceValues[i][1])
        for i in range(length//3, length):
            fit.append(varianceValues[i][1])
        return(fit, unfit)

    def generateChildren(self, fit, strokeHeight, strokeWidth):
        leftParent = 0
        child = 0
        rightParent = len(fit)-1
        while leftParent < rightParent:
            for i in range(len(self.allStrokes)):
                if random.randint(1, 2) == 1:
                    positions = self.population[leftParent][1][i]
                else:
                    positions = self.population[rightParent][1][i]
            self.children[child][positions[0]:positions[0] +
                                 strokeHeight, positions[1]:positions[1]+strokeWidth]
            child += 1
            leftParent += 1
            rightParent -= 1

    def killSomeRandomly(self):
        random.shuffle(self.population)
        self.population = self.population[len(self.children):]
        for child in self.children:
            self.population.append([child, []])

    # This is The Main Function

    def generate(self):
        # Read the strokes and define their properties
        strokes = os.listdir("strokes/set" + self.brushes)
        self.strokes = []
        for stroke in strokes:
            self.strokes.append(
                cv.imread("strokes/set" + self.brushes + '/' + stroke))
        # relativeStrokeSizes = []
        # for stroke in self.strokes:
        #     y = self.image.shape[0] / stroke.shape[0]
        #     x = self.image.shape[1] / stroke.shape[1]
        #     relativeStrokeSizes.append([y, x])

        for epoch in range(1, self.epochs+1):
            self.allStrokes.clear()
            self.allStrokes = self.getStrokes(
                epoch, self.strokes)  # Clears Out the strokes and gives new ones every epoch
            strokeHeight, strokeWidth, _ = self.allStrokes[0].shape

            if not len(self.population):
                self.population = [[(self.image*0 + 255), []]
                                   for i in range(60)]
                self.children = [(self.image*0 + 255) for i in range(20)]

            for generation in range(self.generations):
                comparisonImage = self.image     # Gradually less blurred image for comparison
                varianceValues = []
                for i in range(len(self.population)):
                    canvas = self.population[i]
                    canvas = self.paintCanvas(
                        canvas, strokeHeight, strokeWidth, epoch)
                    varianceValues.append(
                        (self.calculateFitness(canvas[0], comparisonImage), i))
                fit, unfit = self.selectFit(sorted(varianceValues))
                self.generateChildren(fit, strokeHeight, strokeWidth)
                self.killSomeRandomly()
            print(len(self.population))
            cv.imwrite("out/" + str(epoch)+".png", self.population[0][0])


if __name__ == "__main__":
    initiate = Main("sample.png")
    print(initiate.image.shape)
