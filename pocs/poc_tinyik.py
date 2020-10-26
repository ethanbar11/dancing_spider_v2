import numpy as np
import tinyik
from scipy.optimize import Bounds

a0 = 1
a1 = 1
a2 = 1
bounds = ((-np.pi, 2 * np.pi), (-np.pi, np.pi * 2), (-np.pi, np.pi * 2))
# arm = tinyik.Actuator(['z', [a0, 0., 0.], 'y', [1., 0., 0.],
#                        'y', [1.0, 0, 0]],
#                       optimizer=tinyik.optimizer.ScipyConstraintOptimizer(bounds))
arm = tinyik.Actuator(['z', [a0, 0., 0.], 'y', [1., 0., 0.],
                       'y', [1.0, 0, 0]],
                      )
arm.ee = [3, 2, 0]
print(arm.ee)
print(np.round(np.rad2deg(arm.angles)))
