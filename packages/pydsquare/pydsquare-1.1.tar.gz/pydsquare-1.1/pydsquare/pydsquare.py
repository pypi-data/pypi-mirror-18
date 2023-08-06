import random
import math

def diamondSquare(square, ITERATIONS):
    
    return ds(square, 0, 1, ITERATIONS)


def ds(square, index, iteration, iterations):
    
    if(iteration<=iterations):
        
        
        #Step #1: Get the middle point of the square given at first
        randomValue = (random.random() -0.5)*2
            
        squareMiddlePoint = ((square[index][0] + square[index+1][0])/2, #X POSITION
                             
                             (square[index][1]+square[index+3][1])/2, #Y POSITION
                             
                             ((square[index][2]+
                               square[index+1][2]+
                               square[index+2][2]+
                               square[index+3][2])/4) + randomValue #AVERAGE OF HEIGHTS
                             )

        
        #Step #2: Get the middle point of the edges

                        # N0: 1----0
        topEdgeMiddle = ((square[index+1][0]+square[index][0])/2,
                        square[index+1][1],
                        (square[index+1][2]+square[index][2])/2)
                        # N1: 0----2
        leftEdgeMiddle =(square[index][0],
                        (square[index][1]+square[index+2][1])/2,
                        (square[index][2]+square[index+2][2])/2)
                        # N2: 3----2
        bottomEdgeMiddle=((square[index+3][0]+square[index+2][0])/2,
                        square[index+3][1],
                        (square[index+3][2]+square[index+2][2])/2)
                        # N3: 1----3
        rightEdgeMiddle= ((square[index+1][0],
                         (square[index+1][1]+square[index+3][1])/2,
                         (square[index+1][2]+square[index+3][2])/2))
        
        #Step #3: Create new squares & append them to the squares array
        
        #The problem comes here: we are reusing the vertices of the first
        #square. This way we'll have too many repeated vertices in the end.
        #This part needs inspection.    

        
        #TOP LEFT subSQUARE
        square.append(square[index])
        square.append(topEdgeMiddle)
        square.append(leftEdgeMiddle)
        square.append(squareMiddlePoint)
        
        #TOP RIGHT subSQUARE
        square.append(topEdgeMiddle)
        square.append(square[index+1])
        square.append(squareMiddlePoint)
        square.append(rightEdgeMiddle)
  
        #BOTTOM LEFT subSQUARE
        square.append(leftEdgeMiddle)
        square.append(squareMiddlePoint)
        square.append(square[index+2])
        square.append(bottomEdgeMiddle)
        
        #BOTTOM RIGHT subSQUARE
        square.append(squareMiddlePoint)
        square.append(rightEdgeMiddle)
        square.append(bottomEdgeMiddle)
        square.append(square[index+3])

        #Step 4: Recursively call the function on each subSQUARE as if
        #it was the first square.
        
        return ds(square, index+4, iteration+1, iterations)

    return square
