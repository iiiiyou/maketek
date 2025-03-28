import numpy as np
from scipy.interpolate import NearestNDInterpolator
import time


# Define the source and target points
def alignment(val):
    source_points = np.array(
        [
            [15, 166],
            [146, 166],
            [277, 166],
            [409, 166],
            [542, 166],
            [674, 166],
            [806, 166],
            [939, 166],
            [1071, 166],
            [1203, 166],
            [1336, 166],
            [1468, 166],
            [1600, 166],
            [15, 301],
            [146, 301],
            [277, 301],
            [409, 301],
            [542, 301],
            [674, 301],
            [806, 301],
            [939, 301],
            [1071, 301],
            [1203, 301],
            [1336, 301],
            [1468, 301],
            [1600, 301],
            [15, 437],
            [146, 437],
            [277, 437],
            [409, 437],
            [542, 437],
            [674, 437],
            [806, 437],
            [939, 437],
            [1071, 437],
            [1203, 437],
            [1336, 437],
            [1468, 437],
            [1600, 437],
            [15, 571],
            [146, 571],
            [277, 571],
            [409, 571],
            [542, 571],
            [674, 571],
            [806, 571],
            [939, 571],
            [1071, 571],
            [1203, 571],
            [1336, 571],
            [1468, 571],
            [1600, 571],
            [15, 706],
            [146, 706],
            [277, 706],
            [409, 706],
            [542, 706],
            [674, 706],
            [806, 706],
            [939, 706],
            [1071, 706],
            [1203, 706],
            [1336, 706],
            [1468, 706],
            [1600, 706],
            [15, 842],
            [146, 842],
            [277, 842],
            [409, 842],
            [542, 842],
            [674, 842],
            [806, 842],
            [939, 842],
            [1071, 842],
            [1203, 842],
            [1336, 842],
            [1468, 842],
            [1600, 842],
            [15, 977],
            [146, 977],
            [277, 977],
            [409, 977],
            [542, 977],
            [674, 977],
            [806, 977],
            [939, 977],
            [1071, 977],
            [1203, 977],
            [1336, 977],
            [1468, 977],
            [1600, 977],
            [15, 1112],
            [146, 1112],
            [277, 1112],
            [409, 1112],
            [542, 1112],
            [674, 1112],
            [806, 1112],
            [939, 1112],
            [1071, 1112],
            [1203, 1112],
            [1336, 1112],
            [1468, 1112],
            [1600, 1112],
            [15, 1249],
            [146, 1249],
            [277, 1249],
            [409, 1249],
            [542, 1249],
            [674, 1249],
            [806, 1249],
            [939, 1249],
            [1071, 1249],
            [1203, 1249],
            [1336, 1249],
            [1468, 1249],
            [1600, 1249],
            [15, 1384],
            [146, 1384],
            [277, 1384],
            [409, 1384],
            [542, 1384],
            [674, 1384],
            [806, 1384],
            [939, 1384],
            [1071, 1384],
            [1203, 1384],
            [1336, 1384],
            [1468, 1384],
            [1600, 1384],
            [15, 1519],
            [146, 1519],
            [277, 1519],
            [409, 1519],
            [542, 1519],
            [674, 1519],
            [806, 1519],
            [939, 1519],
            [1071, 1519],
            [1203, 1519],
            [1336, 1519],
            [1468, 1519],
            [1600, 1519]
        ]
    )

    target_points = np.array(
        [
            [2, 1],
            [3, 1],
            [4, 1],
            [5, 1],
            [6, 1],
            [7, 1],
            [8, 1],
            [9, 1],
            [10, 1],
            [11, 1],
            [12, 1],
            [13, 1],
            [14, 1],
            [2, 2],
            [3, 2],
            [4, 2],
            [5, 2],
            [6, 2],
            [7, 2],
            [8, 2],
            [9, 2],
            [10, 2],
            [11, 2],
            [12, 2],
            [13, 2],
            [14, 2],
            [2, 3],
            [3, 3],
            [4, 3],
            [5, 3],
            [6, 3],
            [7, 3],
            [8, 3],
            [9, 3],
            [10, 3],
            [11, 3],
            [12, 3],
            [13, 3],
            [14, 3],
            [2, 4],
            [3, 4],
            [4, 4],
            [5, 4],
            [6, 4],
            [7, 4],
            [8, 4],
            [9, 4],
            [10, 4],
            [11, 4],
            [12, 4],
            [13, 4],
            [14, 4],
            [2, 5],
            [3, 5],
            [4, 5],
            [5, 5],
            [6, 5],
            [7, 5],
            [8, 5],
            [9, 5],
            [10, 5],
            [11, 5],
            [12, 5],
            [13, 5],
            [14, 5],
            [2, 6],
            [3, 6],
            [4, 6],
            [5, 6],
            [6, 6],
            [7, 6],
            [8, 6],
            [9, 6],
            [10, 6],
            [11, 6],
            [12, 6],
            [13, 6],
            [14, 6],
            [2, 7],
            [3, 7],
            [4, 7],
            [5, 7],
            [6, 7],
            [7, 7],
            [8, 7],
            [9, 7],
            [10, 7],
            [11, 7],
            [12, 7],
            [13, 7],
            [14, 7],
            [2, 8],
            [3, 8],
            [4, 8],
            [5, 8],
            [6, 8],
            [7, 8],
            [8, 8],
            [9, 8],
            [10, 8],
            [11, 8],
            [12, 8],
            [13, 8],
            [14, 8],
            [2, 9],
            [3, 9],
            [4, 9],
            [5, 9],
            [6, 9],
            [7, 9],
            [8, 9],
            [9, 9],
            [10, 9],
            [11, 9],
            [12, 9],
            [13, 9],
            [14, 9],
            [2, 10],
            [3, 10],
            [4, 10],
            [5, 10],
            [6, 10],
            [7, 10],
            [8, 10],
            [9, 10],
            [10, 10],
            [11, 10],
            [12, 10],
            [13, 10],
            [14, 10],
            [2, 11],
            [3, 11],
            [4, 11],
            [5, 11],
            [6, 11],
            [7, 11],
            [8, 11],
            [9, 11],
            [10, 11],
            [11, 11],
            [12, 11],
            [13, 11],
            [14, 11]
        ]
    )

    # Create the NearestNDInterpolator object
    interpolator = NearestNDInterpolator(source_points, target_points)
    interpolated_values = []
    
    result = []


    if(val[0]==0):
        # val[1]=0
        # val[2]=0
        print("val is 0")
        return val
    
    elif(val[0]==1 and val[1]==0 and val[2]==0):
        z=1
        x=0
        y=0
        return z, x, y
    
    elif(val[0]==2 and val[1]==0 and val[2]==0):
        z=2
        x=0
        y=0
        return z, x, y
    
    else:
        result.append(1)
        for i in list(val):
            center_point = i[1:3]
            # print(i)
            # print(center_point)

        # Interpolate the query points
            print(interpolator(center_point))
            interpolated_values = interpolator(center_point)
            x, y = interpolated_values[0]

            result.append(x)
            result.append(y)

        # print(result)
        return result

