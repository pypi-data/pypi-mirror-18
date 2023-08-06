#==============================================================================
# Potential improvements
#==============================================================================

# Add __or__, __and__, etc functionality to allow boolean operations
# Create DeviceSet
# Replace origin/destination with source/destination
# 

#==============================================================================
# Major TODO
#==============================================================================

 # TODO Add flatten()
 # TODO Move route to geometry

#==============================================================================
# Imports
#==============================================================================

from __future__ import division # Otherwise integer division e.g.  20 / 7 = 2
from __future__ import print_function # Use print('hello') instead of print 'hello'
from __future__ import absolute_import

import gdspy
import yaml
from copy import deepcopy
import numpy as np
from numpy import sqrt, mod, pi, sin, cos
from numpy.linalg import norm

from matplotlib import pyplot as plt
from matplotlib.patches import Polygon as PolygonPatch
from matplotlib.collections import PatchCollection


#==============================================================================
# Useful transformation functions
#==============================================================================

def rotate_points(points, angle = 45, center = (0,0)):
    """ Rotates points around a centerpoint defined by ``center``.  ``points`` may be
    input as either single points [1,2] or array-like[N][2], and will return in kind
    """
    angle = angle*pi/180
    ca = cos(angle)
    sa = sin(angle)
    sa = np.array((-sa, sa))
    c0 = np.array(center)
    if np.array(points).ndim == 2: 
        return (points - c0) * ca + (points - c0)[:,::-1] * sa + c0
    if np.array(points).ndim == 1: 
        return (points - c0) * ca + (points - c0)[::-1] * sa + c0
    
def reflect_points(points, p1 = (0,0), p2 = (1,0)):
    """ Reflects points across the line formed by p1 and p2.  ``points`` may be
    input as either single points [1,2] or array-like[N][2], and will return in kind
    """
    # From http://math.stackexchange.com/questions/11515/point-reflection-across-a-line
    points = np.array(points); p1 = np.array(p1); p2 = np.array(p2);
    if np.array(points).ndim == 1: 
        return 2*(p1 + (p2-p1)*np.dot((p2-p1),(points-p1))/norm(p2-p1)**2) - points
    if np.array(points).ndim == 2: 
        return np.array([2*(p1 + (p2-p1)*np.dot((p2-p1),(p-p1))/norm(p2-p1)**2) - p for p in points])

def translate_points(points, d = [1,2]):
    """ Reflects points across the line formed by p1 and p2.  ``points`` may be
    input as either single points [1,2] or array-like[N][2], and will return in kind
    """
    points = np.array(points) + d
    return points
    

    
    
class _GeometryHelper(object):
    """ This is a helper class. It can be added to any other class which has 
    the functions move() and the property ``bbox`` (as in self.bbox).  It uses
    that function+property to enable you to do things like check what the center
    of the bounding box is (self.center), and also to do things like move the
    bounding box such that its maximum x value is 5.2 (self.xmax = 5.2) """
    
    @property
    def center(self):
        return np.sum(self.bbox,0)/2

    @center.setter
    def center(self, destination):
        self.move(destination = destination, origin = self.center)
        
    @property
    def x(self):
        return np.sum(self.bbox,0)[0]/2

    @x.setter
    def x(self, destination):
        destination = (destination, self.center[1])
        self.move(destination = destination, origin = self.center, axis = 'x')
        
    @property
    def y(self):
        return np.sum(self.bbox,0)[1]/2

    @y.setter
    def y(self, destination):
        destination = ( self.center[0], destination)
        self.move(destination = destination, origin = self.center, axis = 'y')
        
    @property
    def xmax(self):
        return self.bbox[1][0]

    @xmax.setter
    def xmax(self, destination):
        self.move(destination = (destination, 0), origin = self.bbox[1], axis = 'x')
        
    @property
    def ymax(self):
        return self.bbox[1][1]

    @ymax.setter
    def ymax(self, destination):
        self.move(destination = (0, destination), origin = self.bbox[1], axis = 'y')
        
    @property
    def xmin(self):
        return self.bbox[0][0]

    @xmin.setter
    def xmin(self, destination):
        self.move(destination = (destination, 0), origin = self.bbox[0], axis = 'x')
        
    @property
    def ymin(self):
        return self.bbox[0][1]

    @ymin.setter
    def ymin(self, destination):
        self.move(destination = (0, destination), origin = self.bbox[0], axis = 'y')
        
    @property
    def xsize(self):
        bbox = self.bbox
        return bbox[1][0] - bbox[0][0]
        
    @property
    def ysize(self):
        bbox = self.bbox
        return bbox[1][1] - bbox[0][1]

    def movex(self, origin = 0, destination = None):
        if destination is None:
            destination = origin
            origin = 0
        self.move(origin = (origin,0), destination = (destination,0))
        return self

    def movey(self, origin = 0, destination = None):
        if destination is None:
            destination = origin
            origin = 0
        self.move(origin = (0,origin), destination = (0,destination))
        return self
        




class Port(object):
    def __init__(self, name = None, midpoint = (0,0), width = 1, orientation = 90, parent = None):
        self.name = name
        self.midpoint = np.array(midpoint, dtype = 'float64')
        self.width = width
        self.orientation = mod(orientation,360)
        self.parent = parent
        if self.width <= 0: raise ValueError('[DEVICE] Port creation error: width cannot be negative or zero')
        
    def __repr__(self):
        return ('Port (name %s, midpoint %s, width %s, orientation %s)' % \
                (self.name, self.midpoint, self.width, self.orientation))
       
    @property
    def endpoints(self):
        dx = self.width/2*np.cos((self.orientation - 90)*pi/180)
        dy = self.width/2*np.sin((self.orientation - 90)*pi/180)
        left_point = self.midpoint - np.array([dx,dy])
        right_point = self.midpoint + np.array([dx,dy])
        return np.array([left_point, right_point])
    
    # FIXME currently broken
    @endpoints.setter
    def endpoints(self, points):
        p1, p2 = np.array(points[0]), np.array(points[1])
        self.midpoint = (p1+p2)/2
        dx, dy = p2-p1
        self.orientation = np.arctan2(-dy,dx)*180/pi
        self.width = sqrt(dx**2 + dy**2)
        
    @property
    def normal(self):
        dx = np.cos((self.orientation)*pi/180)
        dy = np.sin((self.orientation)*pi/180)
        return np.array([self.midpoint, self.midpoint + np.array([dx,dy])])
        
        


class Polygon(gdspy.Polygon, _GeometryHelper):
    @property
    def bbox(self):
        return np.asarray( (np.min(self.points, axis = 0), np.max(self.points, axis = 0)))

    def rotate(self, angle = 45, center = (0,0)):
        super(Polygon, self).rotate(angle = angle*pi/180, center = center)
        return self
            
    def move(self, origin = (0,0), destination = None, axis = None):
        """ Moves elements of the Device from the origin point to the destination.  Both
         origin and destination can be 1x2 array-like, Port, or a key
         corresponding to one of the Ports in this device """

        # If only one set of coordinates is defined, make sure it's used to move things
        if destination is None:
            destination = origin
            origin = [0,0]

        if isinstance(origin, Port):            o = origin.midpoint
        elif np.array(origin).size == 2:    o = origin
        elif self.ports.has_key(origin):    o = self.ports[origin].midpoint
        else: raise ValueError('[DeviceReference.move()] ``origin`` not array-like, a port, or port name')
            
        if isinstance(destination, Port):           d = destination.midpoint
        elif np.array(destination).size == 2:        d = destination
        elif self.ports.has_key(destination):   d = self.ports[destination].midpoint
        else: raise ValueError('[DeviceReference.move()] ``destination`` not array-like, a port, or port name')

        if axis == 'x': d = (d[0], o[1])
        if axis == 'y': d = (o[0], d[1])

        dx,dy = np.array(d) - o

        super(Polygon, self).translate(dx, dy)
        return self

            
    def reflect(self, p1 = (0,1), p2 = (0,0)):
        self.points = reflect_points(self.points, p1, p2)
        return self


        
class Device(gdspy.Cell, _GeometryHelper):
    uid = 0
    
    def __init__(self, name = 'Unnamed'):
        self.ports = {}
        self.parameters = {}
        self.meta = {}
        self.references = []

        Device.uid += 1
        name = '%s%06d' % (name[:20], Device.uid) # Write name e.g. 'Unnamed000005'

        super(Device, self).__init__(name, exclude_from_global=True)

    @property
    def layers(self):
        return self.get_layers()

    @property
    def bbox(self):
        self.bb_is_valid = False # IMPROVEMENT This is a hack to get around gdspy caching issues
        return np.array(self.get_bounding_box())

        
    def add_ref(self, device, config = None, **kwargs):
        """ Takes a Device (or Device-making function with config) and adds it
        as a DeviceReference to the current Device.  """
         # Check if ``device`` is actually a device-making function
        if callable(device):    d = makedevice(fun = device, config = config, **kwargs)
        else:                   d = device
        device_ref = DeviceReference(d)   # Create a DeviceReference (CellReference)
        self.add(device_ref)             # Add DeviceReference (CellReference) to Device (Cell)
        self.references.append(device_ref) # Add to the list of references (for convenience)
        return device_ref                # Return the DeviceReference (CellReference)


    def add_polygon(self, points, layer = 0, datatype = 0):
        if isinstance(points, gdspy.Polygon):
            points = points.points
        elif isinstance(points, gdspy.PolygonSet):
            return [self.add_polygon(p, layer, datatype) for p in points.polygons]
        
        if len(points[0]) == 2: # Then it must be of the form [[1,2],[3,4],[5,6]]
            polygon = Polygon(points, layer, datatype)
        elif len(points[0]) > 2: # Then it must be of the form [[1,3,5],[2,4,6]]
            polygon = Polygon(xy2p(points), layer, datatype)
        self.add(polygon)
        return polygon
        
        
    def add_port(self, name = None, midpoint = (0,0), width = 1, orientation = 45, port = None):
        """ Can be called to copy an existing port like add_port(port = existing_port) or
        to create a new port add_port(myname, mymidpoint, mywidth, myorientation).
        Can also be called to copy an existing port with a new name like add_port(port = existing_port, name = new_name)"""
        if isinstance(port, Port): p = deepcopy(port)
        elif isinstance(name, Port):
            p = deepcopy(name)
            name = p.name
        else:                  p = Port(name, midpoint, width, orientation, parent = self)
        if name is not None: p.name = name
        if self.ports.has_key(p.name):
            raise ValueError('[DEVICE] add_port() error: Port name already exists in this device') 
        self.ports[p.name] = p
        return p
        
        
    def add_array(self, device, start = (0,0), spacing = (10,0), num_devices = 6, config = None, **kwargs):
         # Check if ``device`` is actually a device-making function
        if callable(device):    d = makedevice(fun = device, config = config, **kwargs)
        else:                   d = device
        references = []
        for n in range(num_devices):
            sd = self.add_ref(d)
            sd.move(destination = np.array(spacing)*n, origin = -np.array(start))
            references.append(sd)
        return references
        

    def annotate(self, text = 'hello', position = (0,0), layer = 89):
        if type(text) is not str: text = str(text)
        l = self.add(gdspy.Label(text = text, position = position, anchor = 'o', layer=layer))
        return l
        

    def delete_port(self, name):
        self.ports.pop(name, None)
    
    
    def write_gds(self, filename, unit = 1e-6, precision = 1e-9):
        if filename[-4:] != '.gds':  filename += '.gds'
        tempname = self.name
        self.name = 'toplevel'
        gdspy.gds_print(filename, cells=[self], name='library', unit=unit, precision=precision)
        self.name = tempname


    def distribute(self, elements, direction = 'x', spacing = 100, separation = True):
        multiplier = 1
        if   direction[0] == '+':
            direction = direction[1:]
        elif direction[0] == '-':
            direction = direction[1:]
            multiplier = -1

        xy = np.array([0,0])
        for e in elements:
            e.center = xy
            if direction == 'x':
                xy = xy + (np.array([spacing, 0]) + np.array([e.xsize, 0])*(separation==True))*multiplier
            elif direction == 'y':
                xy = xy + (np.array([0, spacing]) + np.array([0, e.ysize])*(separation==True))*multiplier
            else:
                raise ValueError('[PHIDL] distribute() needs a direction of "x", "+y", "-x", etc')

        
    def flatten(self, depth = None):
        pass

    
    def rotate(self, angle = 45, center = (0,0)):
        for e in self.elements:
            if isinstance(e, Polygon):
                e.rotate(angle = angle, center = center)
            elif isinstance(e, (gdspy.Polygon, gdspy.PolygonSet)):
                e.rotate(angle = angle*pi/180, center = center)
            elif isinstance(e, DeviceReference):
                e.rotate(angle, center)
        for p in self.ports.values():
            p.midpoint = rotate_points(p.midpoint, angle, center)
            p.orientation = mod(p.orientation + angle, 360)
        return self
            
    def move(self, origin = (0,0), destination = None, axis = None):
        """ Moves elements of the Device from the origin point to the destination.  Both
         origin and destination can be 1x2 array-like, Port, or a key
         corresponding to one of the Ports in this device """

        # If only one set of coordinates is defined, make sure it's used to move things
        if destination is None:
            destination = origin
            origin = [0,0]

        if isinstance(origin, Port):            o = origin.midpoint
        elif np.array(origin).size == 2:    o = origin
        elif self.ports.has_key(origin):    o = self.ports[origin].midpoint
        else: raise ValueError('[DeviceReference.move()] ``origin`` not array-like, a port, or port name')
            
        if isinstance(destination, Port):           d = destination.midpoint
        elif np.array(destination).size == 2:        d = destination
        elif self.ports.has_key(destination):   d = self.ports[destination].midpoint
        else: raise ValueError('[DeviceReference.move()] ``destination`` not array-like, a port, or port name')

        if axis == 'x': d = (d[0], o[1])
        if axis == 'y': d = (o[0], d[1])

        dx,dy = np.array(d) - o
        
        # Move geometries
        for e in self.elements:
            if isinstance(e, (gdspy.Polygon, gdspy.PolygonSet)): 
                e.translate(dx,dy)
            if isinstance(e, DeviceReference): 
                e.move(destination = d, origin = o)
        for p in self.ports.values():
            p.midpoint = np.array(p.midpoint) + np.array(d) - np.array(o)
        
        # Move labels
        for l in self.labels:
            l.translate(dx,dy)
        
        return self
            
    def reflect(self, p1 = (0,1), p2 = (0,0)):
        for e in self.elements:
            if isinstance(e, gdspy.Polygon):
                e.points = reflect_points(e.points, p1, p2)
            elif isinstance(e, gdspy.PolygonSet):
                for poly in e.polygons:
                    poly.points = reflect_points(poly.points, p1, p2)
            elif isinstance(e, DeviceReference):
                e.reflect(p1, p2)
        for p in self.ports.values():
            p.midpoint = reflect_points(p.midpoint, p1, p2)
            phi = np.arctan2(p2[1]-p1[1], p2[0]-p1[0])*180/pi
            p.orientation = 2*phi - p.orientation
                
    
    
class DeviceReference(gdspy.CellReference, _GeometryHelper):
    def __init__(self, device, origin=(0, 0), rotation=0, magnification=None, x_reflection=False):
        super(DeviceReference, self).__init__(device, origin, rotation, magnification, x_reflection)
        self.parent = device
        self._parent_ports = device.ports
        self._local_ports = deepcopy(device.ports)
    
    @property
    def ports(self):
        """ This property allows you to access my_device_reference.ports, and receive a copy
        of the ports dict which is correctly rotated and translated"""
        for key in self._parent_ports.keys():
            port = self._parent_ports[key] 
            new_midpoint, new_orientation = self._transform_port(port.midpoint, \
                port.orientation, self.origin, self.rotation, self.x_reflection)
            self._local_ports[key].midpoint = new_midpoint
            self._local_ports[key].orientation = mod(new_orientation,360)
            self._local_ports[key].parent = self
        return self._local_ports

    @property
    def meta(self):
        return self.parent.meta
        
    @property
    def bbox(self):
        return self.get_bounding_box()

        
    def _transform_port(self, point, orientation, origin=(0, 0), rotation=None, x_reflection=False):
        # Apply GDS-type transformations (x_ref)
        new_point = np.array(point)
        new_orientation = orientation
        
        if x_reflection:
            new_point[1] = -new_point[1]
            new_orientation = -orientation
        if rotation is not None:
            new_point = rotate_points(new_point, angle = rotation, center = [0, 0])
            new_orientation += rotation
        if origin is not None:
            new_point = new_point + np.array(origin)
        new_orientation = mod(new_orientation, 360)
            
        return new_point, new_orientation

        
    def move(self, origin = (0,0), destination = None, axis = None):
        """ Moves the DeviceReference from the origin point to the destination.  Both
         origin and destination can be 1x2 array-like, Port, or a key
         corresponding to one of the Ports in this device_ref """

        # If only one set of coordinates is defined, make sure it's used to move things
        if destination is None:
            destination = origin
            origin = (0,0)

        if isinstance(origin, Port):            o = origin.midpoint
        elif np.array(origin).size == 2:    o = origin
        elif self.ports.has_key(origin):    o = self.ports[origin].midpoint
        else: raise ValueError('[DeviceReference.move()] ``origin`` not array-like, a port, or port name')
            
        if isinstance(destination, Port):           d = destination.midpoint
        elif np.array(destination).size == 2:   d = destination
        elif self.ports.has_key(destination):   d = self.ports[destination].midpoint
        else: raise ValueError('[DeviceReference.move()] ``destination`` not array-like, a port, or port name')
            
        # Lock one axis if necessary
        if axis == 'x': d = (d[0], o[1])
        if axis == 'y': d = (o[0], d[1])

        # This needs to be done in two steps otherwise floating point errors can accrue
        dxdy = np.array(d) - np.array(o)
        self.origin = np.array(self.origin) + dxdy
        return self

        
    def rotate(self, angle = 45, center = (0,0)):
        if type(center) is Port:  center = center.midpoint
        self.rotation += angle
        self.origin = rotate_points(self.origin, angle, center)
        return self
        
        
    def reflect(self, p1 = (0,1), p2 = (0,0)):
        if type(p1) is Port:  p1 = p1.midpoint
        if type(p2) is Port:  p2 = p2.midpoint
        p1 = np.array(p1);  p2 = np.array(p2)
        # Translate so reflection axis passes through origin
        self.origin = self.origin - p1
        
        # Rotate so reflection axis aligns with x-axis
        angle = np.arctan((p2[1]-p1[1])/(p2[0]-p1[0]))*180/pi
        self.origin = rotate_points(self.origin, angle = -angle, center = [0,0])
        self.rotation -= angle
        
        # Reflect across x-axis
        self.x_reflection = not self.x_reflection
        self.origin[1] = -self.origin[1]
        self.rotation = -self.rotation
        
        # Un-rotate and un-translate
        self.origin = rotate_points(self.origin, angle = angle, center = [0,0])
        self.rotation += angle
        self.origin = self.origin + p1
        return self
        
        
    def connect(self, port, destination):
        # ``port`` can either be a string with the name or an actual Port
        if self.ports.has_key(port):
            p = self.ports[port]
        elif type(port) is Port:
            p = port
        else:
            raise ValueError('[PHIDL] connect() did not receive a Port or valid port name' + \
                ' - received (%s), ports available are (%s)' % (port, self.ports.keys()))

        self.rotate(angle =  180 + destination.orientation - p.orientation, center = p.midpoint)
        self.move(origin = p, destination = destination)
        return self


#==============================================================================
# Handy geometry functions
#==============================================================================


def _load_gds(filename, cell_name, load_ports = True):
    # Format "Port(name = hello, width = 20, orientation = 180)"
    gdspy.Cell.cell_dict.clear()
    gdsii = gdspy.GdsImport(filename)
    gdsii.extract(cell_name)
    d = Device(cell_name)
    d.elements = gdspy.Cell.cell_dict[cell_name].elements
    for label in gdspy.Cell.cell_dict[cell_name].labels:
        t = label.text
        if t[0:5] == 'Port(' and t[-1] == ')':
            arguments = t[5:-1]
            arguments = arguments.replace(' ', '')
            args = {a.split('=')[0] : a.split('=')[1] for a in arguments.split(',')}
            if args['name'].isdigit():args['name'] = int(args['name'])
            d.add_port(name = args['name'], midpoint = label.position, width = float(args['width']), orientation = float(args['orientation']))
        else:
            d.labels.append(label)
    return d


#==============================================================================
# Helper functions
#==============================================================================

def p2xy(points):
    """ Takes in a list of [x,y] pairs and converts them to lists of x points 
    and y points.  So p2xy([[1,5],[2,6],[3,7]]) returns [[1,2,3],[5,6,7]]
    """
    p = np.array(points)
    x = p[:,0]
    y = p[:,1]
    return np.array([x,y])
    
def xy2p(*args):
    """ Takes in lists of x points and y points, e.g. [1,2,3],[5,6,7] and
    converts it to the point format e.g. [[1,5],[2,6],[3,7]].  Can either be
    called as xy2p(xpts, ypts) or as xy2p(xy) where xy = [xpts, ypts]
    """
    if len(args) == 1:      x,y = args[0][0], args[0][1] 
    elif len(args) == 2:    x,y = args[0],    args[1]
    points = np.array(zip(*[x,y]))
    return points
    
    
def quickplot(items, overlay_ports = True, overlay_subports = True, label_ports = True, new_window = True):
    """ Takes a list of devices/references/polygons or single one of those, and
    plots them.  Also has the option to overlay their ports """
    if new_window: fig, ax = plt.subplots(1)
    else:
        ax = plt.gca()  # Get current figure
        ax.cla()        # Clears the axes of all previous polygons
    
    # Iterate through each each Device/DeviceReference/Polygon
    patches = []
    if type(items) is not list:  items = [items]
    for item in items:
        if isinstance(item, (Device, DeviceReference)):
            polygons = item.get_polygons(by_spec=False, depth=None)
            for p in polygons:
                patches.append(PolygonPatch(p, closed=True, alpha = 0.4))
            for name, port in item.ports.items():
                _draw_port(port, arrow_scale = 2, shape = 'full', color = 'k')
                plt.text(port.midpoint[0], port.midpoint[1], name)
        if isinstance(item, Device) and overlay_subports is True:
            for sd in item.references:
                for name, port in sd.ports.items():
                    _draw_port(port, arrow_scale = 1, shape = 'right', color = 'r')
                    plt.text(port.midpoint[0], port.midpoint[1], name)
        if isinstance(item, gdspy.Polygon):
            patches.append(PolygonPatch(item.points, closed=True, alpha = 0.4))
        if isinstance(item, gdspy.PolygonSet):
            for p in item.polygons:
                patches.append(PolygonPatch(p, closed=True, alpha = 0.4))
    pc = PatchCollection(patches, alpha=0.4)
    # TODO: Change this to per-layer coloring    
    np.random.seed(0)
    colors = 100*np.random.rand(len(patches))
    pc.set_array(np.array(colors))
    ax.add_collection(pc)
    plt.axis('equal')
    ax.grid(True, which='both', alpha = 0.4)
    ax.axhline(y=0, color='k', alpha = 0.2, linewidth = 1)
    ax.axvline(x=0, color='k', alpha = 0.2, linewidth = 1)
    plt.draw()


def _draw_port(port, arrow_scale = 1, **kwargs):
    x = port.midpoint[0]
    y = port.midpoint[1]
    nv = port.normal
    n = (nv[1]-nv[0])*arrow_scale
    dx, dy = n[0], n[1]
    xbound, ybound = p2xy(port.endpoints)
    #plt.plot(x, y, 'rp', markersize = 12) # Draw port midpoint
    plt.plot(xbound, ybound, 'r', linewidth = 3) # Draw port edge
    plt.arrow(x, y, dx, dy,length_includes_head=True, width = 0.1*arrow_scale, head_width=0.3*arrow_scale, **kwargs)


def makedevice(fun, config = None, **kwargs):
    config_dict = {}
    if type(config) is str:
        with open(config) as f:  config_dict = yaml.load(f) # Load arguments from config file
    elif type(config) is dict:   config_dict = config
    config_dict.update(**kwargs)
    return fun(**config_dict)
#
#    
#def useconfig(filename = 'myconfig.yaml', **kwargs):
#    with open(filename) as f:  config_dict = yaml.load(f) # Load arguments from config file
#    config_dict.update(**kwargs)                          # Replace any additional arguments  
#    return config_dict
#
#    
#filename = 'C:/Users/anm16/Downloads/temp.yaml'
#d = _load_config_file(filename)
#
#
#y = makedevice(beamsplitter, filename, arm_length = 50)
#quickplot(y)
#
#y = beamsplitter(**useconfig(filename, arm_length = 50))
#quickplot(y)


