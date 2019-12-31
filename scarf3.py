import pygame,math,os
os.environ['SDL_VIDEO_CENTERED'] = '1'
amplitude = 200
COLOURMAX = (238, 238, 0)# colour at the highest point
COLOURMIN = (255,0,0)# colour at the lowest point
SIZE = (1280,720) # size of the screen
THREED = .1 # the lower the more 3D it is 0 - 1
DEBUG = False
WIDTH = 1 # width of the triangles, 0 is filled in
ANGLE = math.radians(20) # the angle the matrix is rotated, in degrees
class ocean (object):
    def __init__(self):
        self.points = []
        self.num = 30 # the grid will be self.num * self.num
        self.dire = True

    def populate(self):
        for i in range(self.num):
            self.points.append([])
            for g in range(self.num):
                clamp_y = ((1-THREED*self.num)-(THREED*self.num)*i)/self.num
                x = g*math.cos(ANGLE)-clamp_y*math.sin(ANGLE)
                y = g*math.sin(ANGLE)+clamp_y*math.cos(ANGLE)
                self.points[i].append(point(x+1,y+9,self.num-1,0))

    def display(self,surface):
        self.dire = True # reset boolean
        for i in range(self.num-1):
            for g in range(self.num-1):
                if self.dire == True:
                    pts = (self.points[i][g],self.points[i+1][g],self.points[i][g+1],self.points[i+1][g+1])  # bottom left to top right diagonal square
                elif self.dire == False:
                    pts = (self.points[i][g+1],self.points[i][g],self.points[i+1][g+1],self.points[i+1][g]) # top left to bottom right diagonal square
                for colour in pts:
                    colour.get_colour() # lerps the points colour based on its height multiplier

                color = self.average_colours(0,pts) # averages pts[0] pts[1] and pts[2] colours

                pygame.draw.polygon(surface,color,(pts[0].loc,pts[1].loc,pts[2].loc),WIDTH) # draws the bottom left triangle

                color = self.average_colours(1,pts) # averages pts[1] pts[2] and pts[3] colours

                pygame.draw.polygon(surface,color,(pts[1].loc,pts[2].loc,pts[3].loc),WIDTH) # draws the top right triangle

                if DEBUG == True:
                    for f in pts:
                        pygame.draw.circle(surface,(100,100,100),(int(f.loc[0]),int(f.loc[1])),4)  # draws circles on each of the points for debug

                self.dire = not self.dire # changes a boolean to draw a bottom left to top right triangle

    def redo_mult(self,delta):
        # changes the height multiplier based on time and a wave function
        for i in self.points:
            for g in i:
                g.redo_height_mult(delta)

    def average_colours(self,num,pts):
        #averages the colours of the 3 points given
        r = (pts[num].color[0]+pts[num + 1].color[0]+pts[num + 2].color[0])/3
        g = (pts[num].color[1]+pts[num + 1].color[1]+pts[num + 2].color[1])/3
        b = (pts[num].color[2]+pts[num + 1].color[2]+pts[num + 2].color[2])/3
        return (r,g,b)

    def update(self,surface,delta):
        self.redo_mult(delta)
        self.display(surface)

class point (object):
    def __init__(self,layer,height,num,mult):
        self.x = layer
        self.y = height
        self.loc_base = (self.x*(SIZE[0]/num),self.y*(SIZE[1]/num))
        self.loc = self.loc_base
        self.color = (0,100,200)
        self.height_mult = 0
        self.lerp = lambda t, a, b:  a + t * (b - a)

    def redo_height_mult(self,delta):
        self.loc = self.loc_base

        self.height_mult = (math.cos(self.x / 2 + delta / 2) + math.sin(self.y - delta * 2)) * .5 * amplitude

        #self.height_mult = (math.cos(self.x + delta) + math.sin(self.y + delta )) * .5 * amplitude

        # freq = .01
        # self.height_mult = (math.cos(self.x / 2 + delta / 2) + math.sin(self.y - delta * freq)) * .5 * amplitude

        # self.height_mult = (math.cos(40*math.sqrt(self.x**2+delta**2))) * .5 * amplitude

        self.loc = (self.loc[0],self.loc[1]+self.height_mult)

    def get_colour(self):
        percent = (self.height_mult + amplitude)/float(2*amplitude)
        self.color = (self.lerp(percent,COLOURMAX[0],COLOURMIN[0]),self.lerp(percent,COLOURMAX[1],COLOURMIN[1]),self.lerp(percent,COLOURMAX[2],COLOURMIN[2]))

    def sign(self,num):
        if num < 0:
            return -1
        if num == 0:
            return 0
        if num > 0:
            return 1

def run():
    tps = 0
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    done = False

    water = ocean()
    water.populate()

    while not done:
        time_passed_seconds = clock.tick(120)/1000.0
        tps += time_passed_seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        screen.fill((255,255,255))
        water.update(screen,tps)
        pygame.display.flip()
        pygame.display.set_caption("%.1f"%clock.get_fps())

    pygame.quit()

if __name__ == "__main__":
    run()