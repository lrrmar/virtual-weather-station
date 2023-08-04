import numpy as np

class Interpolator:

    def __init__(self,y_weight: float, x_weight: float):
        self.y0 = int(y_weight)
        self.y1 = self.y0 + 1
        self.y_weights =  np.array(
                [y_weight - self.y0, self.y1 - y_weight])
        self.x0 = int(x_weight)
        self.x1 = self.x0 + 1
        self.x_weights =  np.array(
                [x_weight - self.x0, self.x1 - x_weight])

    def interp(self, arr: np.ndarray):

        vals = arr[self.x0:self.x0+2,self.y,self.y+2]
        interp = np.transpose(self.x_weights * np.transpose(vals))\
                * self.y_weights
        return interp
