
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
    def __init__(self, imgPath, generations=1, epochs=2, brushes=1):
        self.image = cv.imread(imgPath)     # Read Image
        self.generations = generations      # Set Number of Generations Per Iteration
        # We need this to keep changing the brush sizes and obtain finer details after every Iteration
        self.epochs = epochs
        self.brushes = str(brushes)         # Select Brushes
        self.imageHeight, self.imageWidth, _ = self.image.shape
        self.population = []
        self.generate()

    # Returns Different Size and Number of Strokes Depending on the Epoch
    def getStrokes(self, epoch, strokes, relativeStrokeSizes):
        allStrokes = []
        numberOfStrokes = 30 + 2 * epoch

        for stroke in self.strokes:
            stroke = cv.resize(stroke, None, fx=max(
                0.1, 0.3/epoch), fy=max(0.1, 0.3/epoch), interpolation=cv.INTER_AREA)
            rows, cols, ch = stroke.shape
            for i in range(1, numberOfStrokes//3 + 1):
                M = cv.getRotationMatrix2D(
                    ((cols-1)/2.0, (rows-1)/2.0), 360/i, 1)
                allStrokes.append(cv.warpAffine(stroke, M, (cols, rows)))

        # random.shuffle(allStrokes)
        return allStrokes

    def paintCanvas(self, canvas, strokeHeight, strokeWidth, epoch):
        for stroke in self.allStrokes:
            y = random.randint(0, self.imageHeight-strokeHeight)
            x = random.randint(0, self.imageWidth-strokeWidth)
            canvas[y:y+strokeHeight, x:x+strokeWidth] += stroke

        return cv.blur(canvas, (self.epochs-epoch, self.epochs-epoch))

    def calculateFitness(self, canvas, comparisonImage):
        diff1 = cv.subtract(canvas, comparisonImage)
        diff2 = cv.subtract(comparisonImage, canvas)
        totalDiff = cv.add(diff1, diff2)
        totalDiff = np.sum(totalDiff)
        return(totalDiff)

    def selectFit(self, varianceValues):
        length = len(varianceValues)
        fit = []
        unfit = []
        for i in range(length//2):
            unfit.append(varianceValues[i][1])
        for i in range(length//2, length):
            unfit.append(varianceValues[i][1])
        return(fit, unfit)

    def generateChildren(self, population, fit):
        

    # This is The Main Function
    def generate(self):
        # Read the strokes and define their properties
        strokes = os.listdir("strokes/set" + self.brushes)
        self.strokes = []
        for stroke in strokes:
            self.strokes.append(
                cv.imread("strokes/set" + self.brushes + '/' + stroke))
        relativeStrokeSizes = []
        # for stroke in self.strokes:
        #     y = self.image.shape[0] / stroke.shape[0]
        #     x = self.image.shape[1] / stroke.shape[1]
        #     relativeStrokeSizes.append([y, x])

        for epoch in range(1, self.epochs):
            self.allStrokes = self.getStrokes(
                epoch, self.strokes, relativeStrokeSizes)  # Clears Out the strokes and gives new ones every epoch
            strokeHeight, strokeWidth, _ = self.allStrokes[0].shape

            if not len(self.population):
                self.population = [(self.image*0 + 255) for i in range(60)]

            for generation in range(self.generations):
                comparisonImage = cv.blur(
                    self.image, (self.generations-generation, self.generations-generation))
                varianceValues = []
                for i in range(len(self.population)):
                    canvas = self.population[i]
                    canvas = self.paintCanvas(
                        canvas, strokeHeight, strokeWidth, epoch)
                    varianceValues.append(
                        (self.calculateFitness(canvas, comparisonImage), i))

                fit, unfit = self.selectFit(sorted(varianceValues))
                children = self.generateChildren(self.population, fit)
                # self.population = self.killMisFits(self.population, children)


initiate = Main("sample.png")
print(initiate.image.shape)
