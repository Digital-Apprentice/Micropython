# copyright Tomasz Zgrys (Digital-Apprentice) - 2023 - MIT license #

# Klasa przekształceń geometrycznych i rysowania prostych kształtów
# konieczne jest przekazanie macierzy punktów, na których odwzorowane zostaną figury geometryczne
# realizacja dla esp32, rozszerzenie biblioteki framebuffer,
# która nie posiada bardziej skomplikowanych figur geometrycznych
# konieczne jest zainicjalizowanie wcześniej macierzy (bytearray) w kodzie
# i przekazanie do instacji obiektu klasy Geometry

# A class of geometric transformations and drawing simple shapes
# it is necessary to provide a matrix of points on which geometric figures will be mapped
# implementation for esp32, framebuffer library extension,
# that does not have more complicated geometric figures
# it is necessary to initialize the bytearray in the code beforehand
# and passing to a Geometry class object

import math
import framebuf
from vectors import Vector

class Geometry:
    def __init__(self, fbuf_data, width, height, color_format,stride=None):
        
        color_formats={
            'MONO_VLSB':framebuf.MONO_VLSB,
            'MONO_HLSB':framebuf.MONO_HLSB,
            'MONO_HMSB':framebuf.MONO_HMSB,
            'RGB565':framebuf.RGB565,
            'GS2_HMSB':framebuf.GS2_HMSB,
            'GS4_HMSB':framebuf.GS4_HMSB,
            'GS8':framebuf.GS8,
        }
        self.width = width   # framebuffer width
        self.height = height # framebuffer height
        color_format = color_format.upper()
        if color_format in color_formats:
            color_format = color_formats.get(color_format)
        else:
            raise ValueError('Unsupportet color format')
        if stride is None:
            self.fbuf = framebuf.FrameBuffer(fbuf_data, width, height, color_format)
        else:
            self.fbuf = framebuf.FrameBuffer(fbuf_data, width, height, color_format, stride)
        
    def fill(self, color):
        '''
        # fill buffer with desired color
        # if pixels have to be blanked, enter a value 0
        '''
        self.fbuf.fill(color) 
    
    def pixel(self, x, y, color=None):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        if color is None:
            return self.fbuf.pixel(x,y)
        else:
            self.fbuf.pixel(x,y,color)
    
    def line(self, x1, y1, x2, y2, color):
        self.fbuf.line(x1, y1, x2, y2, color)
        
    def hline(self, x, y, width, color):
        self.fbuf.line(x,y,x+width,y,color)
    
    def vline(self, x, y, height, color):
        self.fbuf.line(x,y,y+height,y,color)
    
    def rect(self,x,y,w,h,color=0xf):
        self.fbuf.rect(x, y, w, h, color)
        
    def fill_rect(self,x,y,w,h,color=0xf):
        self.fbuf.fill_rect(x, y, w, h, color)
    
    def polygon(self, points, color=0xf, filled=False):
        """
        Draw a polygon on the screen
        :param points: List of (x, y) coordinates of the vertices of the polygon
        :param color: The color of the polygon
        :param filled: Whether to draw a filled polygon or just the outline
        """
        
        points = self.round_coordinates(points)
        print(points)
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            if filled:
                self.fbuf.fill_rect(x1, y1, x2, y2, color)
            else:
                self.fbuf.line(x1, y1, x2, y2, color)
    
    def rectangle_center(self, xc, yc, edge_a, edge_b, color=0xf ,filled=False, return_points=False):
        hea = edge_a/2
        heb = edge_b/2
        if return_points:
            points = [(xc-hea,yc-heb),(xc+hea,yc-heb),(xc+hea,yc+heb),(xc-hea,yc+heb)]
            return points
        if filled:
            self.fbuf.fill_rect(int(xc-hea),int(yc-heb),edge_a,edge_b,color)
        else:
            self.fbuf.rect(int(xc-hea),int(yc-heb),edge_a,edge_b,color)

    def rotate_polygon(self, points, angle, x_c, y_c):
        """
        Rotate a polygon about a center point
        :param points: List of (x, y) coordinates of the vertices of the polygon
        :param angle: Angle of rotation in radians
        :param x_c: x-coordinate of the center point
        :param y_c: y-coordinate of the center point
        """
        rotated_points = []
        for x, y in points:
            x_rotated = x_c + (x - x_c) * math.cos(angle) - (y - y_c) * math.sin(angle)
            y_rotated = y_c + (x - x_c) * math.sin(angle) + (y - y_c) * math.cos(angle)
            rotated_points.append((x_rotated, y_rotated))           
        return rotated_points
    
    def translate_polygon(self,points, dx, dy):
        for i in range(len(points)):
            points[i] = (points[i][0] + dx, points[i][1] + dy)
        return points

    def scale_polygon(self, points, scale_x, scale_y):
         
        """
        Scale a polygon
        :param points: List of (x, y) coordinates of the vertices of the polygon
        :param scale_x: Scale factor along the x-axis
        :param scale_y: Scale factor along the y-axis
        """
        scaled_points = []
        for x,y in points:
            x_scaled = x * scale_x
            y_scaled = y * scale_y
            scaled_points.append((x_scaled, y_scaled))
        return scaled_points
    
    def circle(self, x_c, y_c, r,color=0xffff, filled=False):
        """
        Draw a circle or disc on the frame buffer
        :param x_c: x-coordinate of the center point
        :param y_c: y-coordinate of the center point
        :param r: radius of the circle
        :param filled: Whether to draw a filled disc or just the outline of a circle
        """
        x = 0
        y = r
        d = 3 - 2 * r
        while y >= x:
            if filled:
                self.fbuf.line(x_c - x, y_c - y, x_c + x, y_c - y, color)
                self.fbuf.line(x_c - x, y_c + y, x_c + x, y_c + y, color)
                self.fbuf.line(x_c - y, y_c - x, x_c + y, y_c - x, color)
                self.fbuf.line(x_c - y, y_c + x, x_c + y, y_c + x, color)
            else:
                self.fbuf.pixel(x_c + x, y_c + y, color)
                self.fbuf.pixel(x_c + y, y_c + x, color)
                self.fbuf.pixel(x_c - y, y_c + x, color)
                self.fbuf.pixel(x_c - x, y_c + y, color)
                self.fbuf.pixel(x_c - x, y_c - y, color)
                self.fbuf.pixel(x_c - y, y_c - x, color)
                self.fbuf.pixel(x_c + y, y_c - x, color)
                self.fbuf.pixel(x_c + x, y_c - y, color)
            if d < 0:
                d = d + 4 * x + 6
            else:
                d = d + 4 * (x - y) + 10
                y = y - 1
            x = x + 1
    
    def scale_circle(self, x_c, y_c, r, scale_x, scale_y):
        r_scaled = r * math.sqrt(scale_x ** 2 + scale_y ** 2)
        return (x_c, y_c, r_scaled)
    
    def draw_circle_segment(self,x, y, r, start, end):
        for angle in range(start, end + 1):
            x_offset = r * math.cos(math.radians(angle))
            y_offset = r * math.sin(math.radians(angle))
            self.fbuf.pixel(x + round(x_offset),y + round(y_offset), 555)
        '''
            x: współrzędna x środka okręgu
            y: współrzędna y środka okręgu
            r: promień okręgu
            start: początkowy kąt wycinka okręgu (w stopniach)
            end: końcowy kąt wycinka okręgu (w stopniach)
        '''        
    
    def ellipse(self, xc, yc, a, b, color=0xffff, filled=False):
        '''
        # fbuf - framebuffer instance
        # xc, yc - ellipse center coordinates
        # a, b - length of the semi-axis of the ellipse
        # color - ellipse color
        # fill - boolean value, if True ellipse will be filled, False - not
        '''
        x, y = 0, b
        a2, b2 = a*a, b*b
        fx, fy = 0, 2*a2*y
        p = b2 - a2*b + 0.25*a2

        while fx < fy:
            if filled:
                self.fbuf.vline(xc+x, yc-y, y*2, color)
                self.fbuf.vline(xc-x, yc-y, y*2, color)
            else:
                self.fbuf.pixel(xc+x, yc+y, color)
                self.fbuf.pixel(xc-x, yc+y, color)
                self.fbuf.pixel(xc+x, yc-y, color)
                self.fbuf.pixel(xc-x, yc-y, color)
            if p < 0:
                p += b2*(2*x+3)
                x += 1
                fx += 2*b2
            else:
                p += b2*(2*x+3) + a2*(2-2*y)
                x += 1
                y -= 1
                fx += 2*b2
                fy -= 2*a2

        p = b2*(x+0.5)*(x+0.5) + a2*(y-1)*(y-1) - a2*b2
        
        while y >= 0:
            if filled:
                self.fbuf.vline(xc+x, yc-y, y*2, color)
                self.fbuf.vline(xc-x, yc-y, y*2, color)
            else:
                self.fbuf.pixel(xc+x, yc+y, color)
                self.fbuf.pixel(xc-x, yc+y, color)
                self.fbuf.pixel(xc+x, yc-y, color)
                self.fbuf.pixel(xc-x, yc-y, color)
            if p > 0:
                p += a2*(3-2*y)
                y -= 1
                fy -= 2*a2
            else:
                p += b2*(2*x+2) + a2*(3-2*y)
                x += 1
                y -= 1
                fx += 2*b2
                fy -= 2*a2 
    
    def bezier_curve(self, points, num_steps):
        '''Returns points on a Bezier curve based on given control points'''
        
        def factorial(n):
            '''Returns the factorial of the given number'''
            if n == 0:
                return 1
            return n * factorial(n - 1)
            
        curve=[]
        for t in range(num_steps +1):
            t = t / num_steps
            x, y = 0, 0
            n = len(points) - 1
            for i, point in enumerate(points):
                bernstein = factorial(n) / (factorial(i)*factorial(n-i))*(t**i)*((1-t)**(n-i))
                x += point[0]*bernstein
                y += point[1]*bernstein
            curve.append((x,y))
        return curve
    
    def bezier_curve_II(self,points, num_steps):
        curve = []
        n = len(points) - 1
        fact = [1]
        for i in range(1, n + 1):
            fact.append(fact[-1] * i)
        for t in range(num_steps + 1):
            t = t / num_steps
            x, y = 0, 0
            for i, point in enumerate(points):
                bernstein = fact[n] // (fact[i] * fact[n - i]) * (t ** i) * ((1 - t) ** (n - i))
                x += point[0] * bernstein
                y += point[1] * bernstein
            curve.append((x, y))
        return curve
    
    def scroll(self, x_step,y_step):
        self.fbuf.scroll(x_step,y_step)
        
    def text(s,x,y,color=0xffff):
        self.fbuf.text(s, x, y, color)
    
    def blit(self, buf, x, y, key=-1, palette=None):
        self.fbuf.blit(buf, x, y, key=-1, palette=None)
        '''
        Draw another FrameBuffer on top of the current one at the given coordinates.
        If key is specified then it should be a color integer and the corresponding color will be considered transparent:
        all pixels with that color value will not be drawn.
        (If the palette is specified then the key is compared to the value from palette,
        not to the value directly from fbuf.)
        The palette argument enables blitting between FrameBuffers with differing formats.
        Typical usage is to render a monochrome or grayscale glyph/icon to a color display.
        The palette is a FrameBuffer instance whose format is that of the current FrameBuffer.
        The palette height is one pixel and its pixel width is the number of colors in the source FrameBuffer.
        The palette for an N-bit source needs 2**N pixels; the palette for a monochrome source would have 2 pixels representing background and foreground colors.
        The application assigns a color to each pixel in the palette.
        The color of the current pixel will be that of that palette pixel whose x position is the color of the corresponding source pixel.
        '''
        
    def transform_vecpoints(self, points, rounded=False):
        ''' transforms vector coordinates to cartesian pcoordinates and rounds if True (for matrix indices)'''
        transformed_points = []
        if isinstance(points,Vector):
            x = points.x
            y = points.y
            if rounded:
                x = round(x)
                y = round(y)
            transformed_points=(x,y)
        elif len(points)>1:    
            for point in points:
                if isinstance(points,Vector):
                    x = point.x
                    y = point.y
                elif isinstance(points,tuple):
                    x = point[0]
                    y = point[1]
                if rounded:
                    x = round(x)
                    y = round(y)
            transformed_points.append((x,y))
        return transformed_points
    
    def round_coordinates(self, coordinates):
        # rounds coordinates for matrix indices, it have to be a tuple or list of coordinates
        points_rounded = []
        for point in coordinates:
            points_rounded.append((int(point[0]),int(point[1])))
        return points_rounded
    