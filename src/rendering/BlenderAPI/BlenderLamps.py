import bpy
import math
import random
import mathutils as mathU
import itertools

from BlenderObjects import *


class BlenderLamp(BlenderObject):
    """
    subclasses BlenderObject.
    This is the base class to represent all types of lamps, including but not limited to:
    Point Lamps, Area Lamps, and Sun. 
    Every lamp has the following attributes:
    i. data - reference to the native lamp data structure
    ii. default brightness - some default value chosen by eye for an adequate lighting condition
    iii default size - the larger the size, the more diffuse the casted shadows will be    
    """
    
    def __init__(self, obj_reference):
        super(BlenderLamp, self).__init__(reference=obj_reference)
        self.data = self.reference.data
        self.default_brightness = 0.0
        self.default_size = 0.0

    def blender_create_operation(self, location):
        """
        interface method for all BlenderObjects
        """
        bpy.ops.object.lamp_add(location=location)

    def set_size(self, size):
        self.data.shadow_soft_size = size

    def set_brightness(self, strength):
        """
        Use nodes to set brightness
        """
        self.data.use_nodes = True
        self.data.node_tree.nodes["Emission"].inputs["Strength"].default_value = strength

    def turn_off(self):
        """
        push it to second layer to hide
        """
        self.reference.layers[1] = True
        self.reference.layers[0] = False

    def turn_on(self):
        """
        push it to the topmost layer to show
        """
        self.reference.layers[0] = True
        self.reference.layers[1] = False

    def face_towards(self, x, y, z):
        """
        given a coordinate x, y, z
        calculate a rotational axis and angle, such that when applied, the central axis
        passes through x,y,z
        """
        # vector of target w.r.t camera
        target = mathU.Vector([x, y, z]) - mathU.Vector(self.reference.location)
        target.normalize()
        # rotational origin of camera is (0,0,-1) for some reason
        rot_origin = mathU.Vector([0, 0, -1])
        rot_origin.normalize()
        # get the rotational axis and angle by crossing the two vectors
        rot_axis = rot_origin.cross(target)
        rot_angle = math.degrees(math.acos(rot_origin.dot(target)))
        # set rotation quaternion
        self.set_rot(rot_angle, rot_axis[0], rot_axis[1], rot_axis[2])

    def random_lighting_conditions(self, reference_location=(0.0, 0.0, 0.0), location_variance=1.0):
        """
        choose a random coordinate to face
        choose a random brightness and size
        both according to a gaussian distribution with mean (0,0,0), default brightness and size
        and variance being 30% of mean (negative values of brightness and size will be evaluated
        to zero)
        """
        loc = random_cartesian_coords(0.0, 0.0, 0.0, location_variance, 6.0)
        self.face_towards(*loc)
        self.set_brightness(random.gauss(self.default_brightness, 0.3 * self.default_brightness))
        self.set_size(random.gauss(self.default_size, 0.3 * self.default_size))


class BlenderSun(BlenderLamp):
    """
    Directional, but position invariant (always from above, at infinity)
    """
    def __init__(self, obj_reference, default_brightness=15.0, default_size=0.1):
        super(BlenderSun, self).__init__(obj_reference)
        self.data.type = 'SUN'
        self.default_brightness = default_brightness
        self.default_size = default_size
        self.set_brightness(default_brightness)
        self.set_size(default_size)


class BlenderArea(BlenderLamp):
    """
    Directional, and depends on position. Area 'behind the lamp' will not be illuminated
    """
    def __init__(self, obj_reference, default_brightness=500.0, default_size=5.0):
        super(BlenderArea, self).__init__(obj_reference)
        self.data.type = 'AREA'
        self.default_brightness = default_brightness
        self.default_size = default_size
        self.set_brightness(default_brightness)
        self.set_size(default_size)


class BlenderPoint(BlenderLamp):
    """
    Non-directional, source concentrated in a spot.
    """
    def __init__(self, obj_reference, default_brightness=5000.0, default_size=5.0):
        super(BlenderPoint, self).__init__(obj_reference)
        self.data.type = 'POINT'
        self.default_brightness = default_brightness
        self.default_size = default_size
        self.set_brightness(default_brightness)
        self.set_size(default_size)
