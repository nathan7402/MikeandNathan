import random
from math import sqrt,cos,sin,atan2

class Util:
    ########################################
    #   Mandatory functions for the rrt    #
    ########################################
    mind  = 99999
    # Tests if the new_node is close enough to the goal to consider it a goal
    def winCondition(self,new_node,goal_node,WIN_RADIUS):
        """
        new_node - newly generated node we are checking
        goal_node - goal node
        WIN_RADIUS - constant representing how close we have to be to the goal to
            consider the new_node a 'win'
        """
        new_x, new_y = new_node
        goal_x, goal_y = goal_node
        return (sqrt((new_x - goal_x)**2 + (new_y - goal_y)**2) < WIN_RADIUS)

    # Find the nearest node in our list of nodes that is closest to the new_node
    # Hint: If your solution appears to be drawing squiggles instead of the fractal like pattern
    #       of striaght lines you are probably extending from the last point not the closest point!
    def nearestNode(self,nodes,new_node):
        """
        nodes - a list of nodes in the RRT
        new_node - a node generated from getNewPoint
        """
        x_new, y_new = new_node
        closest_distance = 9999999
        closest_node = None

        for node in nodes:
            x_cur, y_cur = node
            cur_distance = sqrt((x_cur - x_new)**2 + (y_cur - y_new)**2)

            if cur_distance < closest_distance:
                closest_node = node
                closest_distance = cur_distance

        return closest_node

    # Find a new point in space to move towards uniformally randomly but with
    # probability 0.05, sample the goal. This promotes movement to the goal.
    # For the autograder to work you MUST use the already imported
    # random.random() as your random number generator.
    def getNewPoint(self,XDIM,YDIM,XY_GOAL):
        """
        XDIM - constant representing the width of the game aka grid of (0,XDIM)
        YDIM - constant representing the height of the game aka grid of (0,YDIM)
        XY_GOAL - node (tuple of integers) representing the location of the goal
        """
        if random.random() < 0.05:
            #print(XY_GOAL)
            return XY_GOAL
        else:
            return (random.random() * XDIM, random.random() * YDIM)

    # Extend (by at most distance delta) in the direction of the new_point and place
    # a new node there
    def extend(self,current_node,new_point,delta):
        """
        current_node - node from which we extend
        new_point - point in space which we are extending toward
        delta - maximum distance we extend by
        """
        x1, y1 = current_node
        x2, y2 = new_point

        # Prevent delta issues
        if(self.winCondition(current_node, new_point, delta)):
            return new_point
        else:
            angle = atan2(y2-y1, x2-x1)
            #print("CURRENT NODE" + str(current_node))
            #print("NEW POINT" + str(new_point))
            #print(x1 + delta * sin(angle), y1 + delta * cos(angle))
            return(x1 + delta * cos(angle), y1 + delta * sin(angle))

    # iterate throught the obstacles and check that our point is not in any of them
    def isCollisionFree(self,obstacles,point,obs_line_width):
        """
        obstacles - a dictionary with multiple entries, where each entry is a list of
            points which define line segments of with obs_line_width
        point - the location in space that we are checking is not in the obstacles
        obs_line_width - the length of the line segments that define each obstacle's
            boundary
        """

        ## WHAT WE NEED TO DO IS USE DOT PRODUCT TO FIND PERPENDICULAR DISTANCE
        # BETWEEN POINT AND LINES IN OBSTACLES THEN TEST IN WIN CONDITION IF IT IS LESS
        # RHAN obs_line_width / 2

        for key, items in obstacles.items():
            obs_p1 = items[0][0], items[0][1]
            obs_p2 = items[1][0], items[1][1]
            obs_vx, obs_vy = vect_sub(obs_p2, obs_p1)
            theta = atan2(- obs_vx, obs_vy)
            perp_vect = (0.5 * (obs_line_width) * cos(theta), 0.5 * (obs_line_width) * sin(theta))
            a = vect_add(obs_p1, perp_vect)
            b = vect_sub(obs_p1, perp_vect)
            c = vect_add(obs_p2, perp_vect)
            ab = vect_sub(b, a)
            bc = vect_sub(c, b)
            ap = vect_sub(point, a)
            bp = vect_sub(point, b)

            if (0 <= dot(ab, ap) <= dot(ab,ab)) and (0 <= dot(bc, bp) <= dot(bc,bc)):
                return False

        return True

    ################################################
    #  Any other helper functions you need go here #
    ################################################

def vect_add(a,b):
    ax, ay = a
    bx, by = b
    return (ax + bx, ay + by)

def vect_sub(a,b):
    ax, ay = a
    bx, by = b
    return (ax - bx, ay - by)

def dot(a,b):
    ax, ay = a
    bx, by = b
    return (ax * bx) + (ay * by)
