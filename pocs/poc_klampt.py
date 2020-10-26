from klampt.model import trajectory
from klampt import vis

milestones = [[-2, 0, 0], [0.02, 0, 0], [1, 0, 0], [1, 0, 1], [1.2, 0, 1.5], [2, 0, 1], [3, 0, -0.3]]
traj = trajectory.Trajectory(milestones=milestones)
vis
vis.add("point", [-1, 0, 0])
vis.animate("point", traj)
vis.add("traj", traj)
vis.spin(float('inf'))  # show the window until you close it
