# importing the required module
import matplotlib.pyplot as plt
import numpy
import math

#--------------------------------------Task-------------------------------------
# Task: User changes a square by dragging the third corner to a new location.
#       The algorithm should calculate the new position of the second and fourth
#       corners.


plt.figure()


#----------------------------------Function definitions-------------------------

def draw_square(coordinates):
    plt.plot(*zip(coordinates[0],coordinates[1]))
    plt.plot(*zip(coordinates[1],coordinates[2]))
    plt.plot(*zip(coordinates[2],coordinates[3]))
    plt.plot(*zip(coordinates[3],coordinates[0]))
    return True

#---------------------------------------Setup-----------------------------------

# Square data
data_square = [(1,1),(1,2),(2,2),(2,1)]

# Rotate the figure 55 degrees counterclockwise
plt.title('Rotated basic square, 55 degree ccw')
plt.axis('equal')
plt.axis([-7, 7, -7, 7], 'scaled')
plt.plot([0], [0], 'ro')

draw_square(data_square)

plt.title('Basic square')

barrel_role_angle = 55*math.pi/180

# Calculate rotation matrix
rotation_m = [[math.cos(barrel_role_angle), -1*math.sin(barrel_role_angle)], [math.sin(barrel_role_angle), math.cos(barrel_role_angle)]]
print(rotation_m)

# Calculate new square
square_new_corner0 = numpy.matmul(rotation_m, numpy.transpose([data_square[0][0],data_square[0][1]]))

print('transpose of first corner:',numpy.transpose([data_square[0][0],data_square[0][1]]))

square_new_corner0 = numpy.matmul(rotation_m, numpy.transpose([data_square[0][0],data_square[0][1]]))
square_new_corner1 = numpy.matmul(rotation_m, numpy.transpose([data_square[1][0],data_square[1][1]]))
square_new_corner2 = numpy.matmul(rotation_m, numpy.transpose([data_square[2][0],data_square[2][1]]))
square_new_corner3 = numpy.matmul(rotation_m, numpy.transpose([data_square[3][0],data_square[3][1]]))

print('New corner 0:',square_new_corner0)
print('New corner 1:',square_new_corner1)
print('New corner 2:',square_new_corner2)
print('New corner 3:',square_new_corner3)

square_new_square = [square_new_corner0, square_new_corner1, square_new_corner2, square_new_corner3]

print(square_new_square)

draw_square(square_new_square)


# Set up done. User pulls corner 2 to a new position.
change_corner_2 = [-2, 2]
square_user_corner2 = [square_new_corner2[0] + change_corner_2[0], square_new_corner2[1] + change_corner_2[1]]

print('New corner 2:', square_user_corner2)
plt.plot(square_user_corner2[0], square_user_corner2[1], 'go')


# ---------------------------------Solution-------------------------------------
# Draw a new figure with the corners in
# (square_new_square[0], ?, square_user_corner3, ?)
#

# Move square back to origin.
s_origin_distance = square_new_corner0

s_square_moved_to_origin = square_new_square - s_origin_distance
draw_square(s_square_moved_to_origin)

# Rotate the corners back to a horizontal square.
# - Angle given by tan^-1(y_diff_0_3/x_diff_0_3)
s_y_diff = square_new_square[3][1]-square_new_square[0][1]
s_x_diff = square_new_square[3][0]-square_new_square[0][0]

s_angle_to_horizon = math.atan(s_y_diff/s_x_diff)

print('Angle from horizon:', s_angle_to_horizon*180/math.pi)

# - Rotation matrix given by:
s_rotation_m = [[math.cos(-1*s_angle_to_horizon), -1*math.sin(-1*s_angle_to_horizon)], [math.sin(-1*s_angle_to_horizon), math.cos(-1*s_angle_to_horizon)]]

# - Rotate
corner0 = numpy.matmul(s_rotation_m, s_square_moved_to_origin[0])
corner1 = numpy.matmul(s_rotation_m, s_square_moved_to_origin[1])
corner2 = numpy.matmul(s_rotation_m, s_square_moved_to_origin[2])
corner3 = numpy.matmul(s_rotation_m, s_square_moved_to_origin[3])

s_square_moved_to_origin_rotated = [corner0, corner1, corner2, corner3]
draw_square(s_square_moved_to_origin_rotated)

# Calculate the difference between square_new_corner2 and square_user_corner2.
# Call it diff_2
diff_2_m = numpy.subtract(square_user_corner2, square_new_square[2])
diff_2_x = square_user_corner2[0] - square_new_square[2][0]
diff_2_y = square_user_corner2[1] - square_new_square[2][1]

# Rotate difference back to a horizontal square.
diff_2_array = [[diff_2_x], [diff_2_y]]
diff_2_m_horizontal = numpy.matmul(s_rotation_m, diff_2_array)

print('New corner 2: ', s_square_moved_to_origin_rotated[2][0], '\n')
print('Diff_x: ', diff_2_m_horizontal[0], '\n')
print('Diff_y: ', diff_2_m_horizontal[1], '\n')

# Add the diff to corner 2.
s_horizontal_user_corner2 = numpy.array([numpy.asscalar(diff_2_m_horizontal[0]) + s_square_moved_to_origin_rotated[2][0], numpy.asscalar(diff_2_m_horizontal[1]) + s_square_moved_to_origin_rotated[2][1]])


# Plot rotated user corner
plt.plot(s_horizontal_user_corner2[0], s_horizontal_user_corner2[1], 'gx')

# Add the changes to corner 2 to the corners 1(y-component) and 3(x-component).
s_horizontal_user_corner0 = corner0

#s_horizontal_user_corner1_x = corner1[0] + diff_2_m_horizontal[0] - No addition in x-led
s_horizontal_user_corner1_y = corner1[1] + diff_2_m_horizontal[1]
s_horizontal_user_corner1 = [corner1[0], s_horizontal_user_corner1_y]


#s_horizontal_user_corner2 - Known, s_horizontal_user_corner2
s_horizontal_user_corner3 = corner3 + diff_2_m_horizontal[0]


s_horizontal_user_corner3_x = corner3[0] + diff_2_m_horizontal[0]
#s_horizontal_user_corner3_y = corner1[1] + diff_2_m_horizontal[1] - No addition in y-led
s_horizontal_user_corner3 = [s_horizontal_user_corner3_x, corner3[1]]

square_user_corner_horizontal = [s_horizontal_user_corner0, s_horizontal_user_corner1, s_horizontal_user_corner2, s_horizontal_user_corner3]
draw_square(square_user_corner_horizontal)

# Rotate back first then move it. Since s_origin_distance is in rotated coordinates
s_rotation_m_p = [[math.cos(s_angle_to_horizon), -1*math.sin(s_angle_to_horizon)], [math.sin(s_angle_to_horizon), math.cos(s_angle_to_horizon)]]

corner0_p = numpy.matmul(s_rotation_m_p, square_user_corner_horizontal[0])
corner1_p = numpy.matmul(s_rotation_m_p, square_user_corner_horizontal[1])
corner2_p = numpy.matmul(s_rotation_m_p, square_user_corner_horizontal[2])
corner3_p = numpy.matmul(s_rotation_m_p, square_user_corner_horizontal[3])

square_user_corner_p = [corner0_p, corner1_p, corner2_p, corner3_p]

# Add distance from origin, s_origin_distance
square_user_corner_p += s_origin_distance
draw_square(square_user_corner_p)

plt.show()
