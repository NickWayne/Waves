import pygame,math,os
os.environ['SDL_VIDEO_CENTERED'] = '1'
SIZE = (1280,720) # size of the screen
DEBUG = False
class ocean (object):
    def __init__(self):
        self.points = []
        self.num = 30 # the grid will be self.num * self.num
        self.amplitude = 100
        self.angle = 30
        self.threeD = .1
        self.offsetX = 1
        self.offsetY = 9
        self.wireFrame = 1
        self.colorMax = (255, 0, 0)
        self.colorMin = (0, 0, 0)
        self.dire = True

    def populate(self):
        self.points = []
        for i in range(self.num):
            self.points.append([])
            for g in range(self.num):
                clamp_y = ((1-self.threeD*self.num)-(self.threeD*self.num)*i)/self.num
                x = g*math.cos(math.radians(self.angle))-clamp_y*math.sin(math.radians(self.angle))
                y = g*math.sin(math.radians(self.angle))+clamp_y*math.cos(math.radians(self.angle))
                self.points[i].append(point(x+self.offsetX,y+self.offsetY,self.num-1,0))

    def display(self,surface):
        self.dire = True # reset boolean
        for i in range(self.num-1):
            for g in range(self.num-1):
                if self.dire == True:
                    pts = (self.points[i][g],self.points[i+1][g],self.points[i][g+1],self.points[i+1][g+1])  # bottom left to top right diagonal square
                elif self.dire == False:
                    pts = (self.points[i][g+1],self.points[i][g],self.points[i+1][g+1],self.points[i+1][g]) # top left to bottom right diagonal square
                for colour in pts:
                    colour.get_colour(self.amplitude, self.colorMax, self.colorMin) # lerps the points colour based on its height multiplier

                color = self.average_colours(0,pts) # averages pts[0] pts[1] and pts[2] colours

                pygame.draw.polygon(surface,color,(pts[0].loc,pts[1].loc,pts[2].loc),self.wireFrame) # draws the bottom left triangle

                color = self.average_colours(1,pts) # averages pts[1] pts[2] and pts[3] colours

                pygame.draw.polygon(surface,color,(pts[1].loc,pts[2].loc,pts[3].loc),self.wireFrame) # draws the top right triangle

                if DEBUG == True:
                    for f in pts:
                        pygame.draw.circle(surface,(100,100,100),(int(f.loc[0]),int(f.loc[1])),4)  # draws circles on each of the points for debug

                self.dire = not self.dire # changes a boolean to draw a bottom left to top right triangle

    def redo_mult(self,delta):
        # changes the height multiplier based on time and a wave function
        for i in self.points:
            for g in i:
                g.redo_height_mult(self.amplitude, delta)

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

    def redo_height_mult(self, amplitude, delta):
        self.loc = self.loc_base

        self.height_mult = (math.cos(self.x / 2 + delta / 2) + math.sin(self.y - delta * 2)) * .5 * amplitude

        # self.height_mult = (math.cos(self.x + delta) + math.sin(self.y + delta )) * .5 * amplitude

        # freq = .01
        # self.height_mult = (math.cos(self.x / 2 + delta / 2) + math.sin(self.y - delta * freq)) * .5 * amplitude

        # self.height_mult = (math.cos(40*math.sqrt(self.x**2+delta**2))) * .5 * amplitude

        self.loc = (self.loc[0],self.loc[1]+self.height_mult)

    def get_colour(self, amplitude, colorMax, colorMin):
        percent = (self.height_mult + amplitude)/float(2*amplitude)
        self.color = (self.lerp(percent, colorMax[0], colorMin[0]), self.lerp(
            percent, colorMax[1], colorMin[1]), self.lerp(percent, colorMax[2], colorMin[2]))

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
    screen = pygame.display.set_mode(SIZE, pygame.HWSURFACE)
    clock = pygame.time.Clock()
    done = False
    topColor = True

    water = ocean()
    water.populate()

    pygame.key.set_repeat(30, 30)
    while not done:
        time_passed_seconds = clock.tick(120)/1000.0
        tps += time_passed_seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_LEFT:
                    water.angle += 1
                    water.populate()
                if event.key == pygame.K_RIGHT:
                    water.angle -= 1
                    water.populate()
                if event.key == pygame.K_DOWN:
                    water.amplitude = max(1, water.amplitude - 10)
                    water.populate()
                if event.key == pygame.K_UP:
                    water.amplitude += 10
                    water.populate()

                if event.key == pygame.K_i:
                    water.threeD += .01
                    water.populate()
                
                if event.key == pygame.K_k:
                    water.threeD = max(.01, water.threeD - .01)
                    water.populate()

                if event.key == pygame.K_w:
                    water.offsetY -= 1
                    water.populate()
                if event.key == pygame.K_a:
                    water.offsetX -= 1
                    water.populate()
                if event.key == pygame.K_s:
                    water.offsetY += 1
                    water.populate()
                if event.key == pygame.K_d:
                    water.offsetX += 1
                    water.populate()

                if event.key == pygame.K_SPACE:
                    topColor = not topColor

                if event.key == pygame.K_r and event.mod == pygame.KMOD_SHIFT:
                    if topColor:
                        water.colorMax = (
                            max(water.colorMax[0] - 1, 0), water.colorMax[1], water.colorMax[2])
                    else:
                        water.colorMin = (
                            max(water.colorMin[0] - 1, 0), water.colorMin[1], water.colorMin[2])
                    
                    water.populate()

                if event.key == pygame.K_r:
                    if topColor:
                        water.colorMax = (
                            min(water.colorMax[0] + 1, 255), water.colorMax[1], water.colorMax[2])
                    else:
                        water.colorMin = (
                            min(water.colorMin[0] + 1, 255), water.colorMin[1], water.colorMin[2])

                    water.populate()
                
                if event.key == pygame.K_g and event.mod == pygame.KMOD_SHIFT:
                    if topColor:
                        water.colorMax = (
                            water.colorMax[0], max(water.colorMax[1] - 1, 0),  water.colorMax[2])
                    else:
                        water.colorMin = (
                            water.colorMin[0], max(water.colorMin[1] - 1, 0), water.colorMin[2])

                    water.populate()

                if event.key == pygame.K_g:
                    if topColor:
                        water.colorMax = (
                            water.colorMax[0], min(water.colorMax[1] + 1, 255),  water.colorMax[2])
                    else:
                        water.colorMin = (
                            water.colorMin[0], min(water.colorMin[1] + 1, 255), water.colorMin[2])

                    water.populate()

                if event.key == pygame.K_b and event.mod == pygame.KMOD_SHIFT:
                    if topColor:
                        water.colorMax = (
                            water.colorMax[0], water.colorMax[1], max(water.colorMax[2] - 1, 0))
                    else:
                        water.colorMin = (
                            water.colorMin[0], water.colorMin[1], max(water.colorMin[2] - 1, 0))

                    water.populate()

                if event.key == pygame.K_b:
                    if topColor:
                        water.colorMax = (
                            water.colorMax[0], water.colorMax[1], min(water.colorMax[2] + 1, 255))
                    else:
                        water.colorMin = (
                            water.colorMin[0], water.colorMin[1], min(water.colorMin[2] + 1, 255))

                    water.populate()

                if event.key == pygame.K_0:
                    if water.wireFrame == 1:
                        water.wireFrame = 0
                    else :
                        water.wireFrame = 1

                    water.populate()

        screen.fill((255,255,255))
        water.update(screen,tps)
        pygame.display.flip()
        pygame.display.set_caption("%.1f"%clock.get_fps())

    pygame.quit()

if __name__ == "__main__":
    run()
