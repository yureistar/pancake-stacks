from display import *
from matrix import *
from draw import *
from copy import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         sphere: add a sphere to the edge matrix - 
	    takes 4 arguemnts (cx, cy, cz, r)
         torus: add a torus to the edge matrix - 
	    takes 5 arguemnts (cx, cy, cz, r1, r2)
         box: add a rectangular prism to the edge matrix - 
	    takes 6 arguemnts (x, y, z, width, height, depth)	    

	 circle: add a circle to the edge matrix - 
	    takes 3 arguments (cx, cy, r)
	 hermite: add a hermite curve to the edge matrix -
	    takes 8 arguments (x0, y0, x1, y1, rx0, ry0, rx1, ry1)
	 bezier: add a bezier curve to the edge matrix -
	    takes 8 arguments (x0, y0, x1, y1, x2, y2, x3, y3)
         line: add a line to the edge matrix - 
	    takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
	 ident: set the transform matrix to the identity matrix - 
	 scale: create a scale matrix, 
	    then multiply the transform matrix by the scale matrix - 
	    takes 3 arguments (sx, sy, sz)
	 move: create a translation matrix, 
	    then multiply the transform matrix by the translation matrix - 
	    takes 3 arguments (tx, ty, tz)
	 rotate: create a rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 2 arguments (axis, theta) axis should be x, y or z
         clear: clear the edge matrix of points
	 apply: apply the current transformation matrix to the 
	    edge matrix
	 display: draw the lines of the edge matrix to the screen
	    display the screen
	 save: draw the lines of the edge matrix to the screen
	    save the screen to a file -
	    takes 1 argument (file name)
	 quit: end parsing

See the file script for an example of the file format
"""
ARG_COMMANDS = [ 'line', 'scale', 'move', 'rotate', 'save', 'circle', 'bezier', 'hermite', 'box', 'sphere', 'torus' ]

def parse_file( fname, polyedge, transform, screen, color ):

    f = open(fname)
    lines = f.readlines()
    cs = []
    cs.append(new_matrix())
    ident(cs[0])
    
    step = 0.1
    c = 0
    while c < len(lines):
        line = lines[c].strip()
        ##print ':' + line + ':'

        if line in ARG_COMMANDS:            
            c+= 1
            args = lines[c].strip().split(' ')
            ##print 'args\t' + str(args)
        
        if line == 'push':
            print 'PUSH\t'
            cs.append(deepcopy(cs[-1]))
                
        elif line == 'pop':
            print 'POP\t'
            cs.pop()
        
        elif line == 'sphere':
            print 'SPHERE\t' + str(args)
            add_sphere(polyedge,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult(cs[-1], polyedge)
            draw_polygons(polyedge, screen, color)
            polyedge = []
            
        elif line == 'torus':
            print 'TORUS\t' + str(args)
            add_torus(polyedge,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step)
            matrix_mult(cs[-1], polyedge)
            draw_polygons(polyedge, screen, color)
            polyedge = []
            
        elif line == 'box':
            print 'BOX\t' + str(args)
            add_box(polyedge,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(cs[-1], polyedge)
            draw_polygons(polyedge, screen, color)
            polyedge = []
            
        elif line == 'circle':
            print 'CIRCLE\t' + str(args)
            add_circle(polyedge,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult(cs[-1], polyedge)
            draw_lines(polyedge, screen, color)
            polyedge = []

        elif line == 'hermite' or line == 'bezier':
            print 'curve\t' + line + ": " + str(args)
            add_curve(polyedge,
                      float(args[0]), float(args[1]),
                      float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]),
                      float(args[6]), float(args[7]),
                      step, line)                      
            matrix_mult(cs[-1], polyedge)
            draw_lines(polyedge, screen, color)
            polyedge = []
            
        elif line == 'line':            
            print 'LINE\t' + str(args)
            add_edge( polyedge,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult(cs[-1], polyedge)
            draw_lines(polyedge, screen, color)
            polyedge = []
            
        elif line == 'scale':
            print 'SCALE\t' + str(args)
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(t, cs[-1])

        elif line == 'move':
            print 'MOVE\t' + str(args)
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(t, cs[-1])

        elif line == 'rotate':
            print 'ROTATE\t' + str(args)
            theta = float(args[1]) * (math.pi / 180)
            
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(t, cs[-1])

        elif line == 'clear':
            polyedge = []
            
        elif line == 'ident':
            ident(cs[-1])

        #elif line == 'apply':
        #    matrix_mult( cs[-1], polyedge )

        elif line == 'display' or line == 'save':
            if line == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
            
        c+= 1
