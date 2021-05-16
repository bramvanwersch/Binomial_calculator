from tkinter import *
from random import sample
from math import ceil, log10


class Point:
    """
    Class for tracking a d dimensional point
    """
    def __init__(self, x, y):
        """
        When initialising the point needs to be named and the coordinates
        need to be supplied

        point. This can be useful when accessing certain dimensions of the
        point by name
        """
        self.x = x
        self.y = y

    def __str__(self):
        """
        Behaviour for when str() is called on this container.

        :return: a string of all the dimensions of the point
        """
        return str((self.x, self.y))


class BinomialDistributionGraph(Frame):
    """
    Class for generating a graph for a KMeans object
    """
    # constants for this class
    CANVAS_WIDTH = 300
    CANVAS_HEIGHT = 300
    SURROUNDING_MARGINS_LEFT = 50
    SURROUNDING_MARGINS_RIGHT = 25
    SURROUNDING_MARGINS_TOP = 50
    SURROUNDING_MARGINS_BOTTOM = 50
    GRAPH_WIDTH = CANVAS_WIDTH - SURROUNDING_MARGINS_LEFT - SURROUNDING_MARGINS_RIGHT
    GRAPH_HEIGHT = CANVAS_HEIGHT - SURROUNDING_MARGINS_TOP - SURROUNDING_MARGINS_BOTTOM
    IN_GRAPH_MARGIN = 10
    DATA_POINT_SIZE = 6
    MAX_AXIS_NUMBERS = 6
    MAX_DATA_POINTS = 25

    LOWER_COLOR = "blue"
    HIGHER_COLOR = "red"
    EXACT_COLOR = "green"

    def __init__(self, master, points, succes_number=-1):
        """
        Initialize a K-means graph with a kmeans object and the 2 dimensions
        for the different axis.

        :param master: Tk Object to be passed to Frame
        points in the kmeans to use for the y-axis
        """
        Frame.__init__(self, master)
        # determine the range of the values that need to be plotted
        x_values = [point.x for point in points]
        y_values = [point.y for point in points]
        if len(x_values) != 0 and len(y_values) != 0:
            self.min_max_x_axis = [min(x_values), max(x_values)]
            self.min_max_y_axis = [min(y_values), max(y_values)]
        else:
            self.min_max_x_axis = [0, 1]
            self.min_max_y_axis = [0, 1]
        # get the amount of pixels per 1 number for both axis
        self.pixels_per_1_x, self.pixels_per_1_y = self.__pixels_per_x_y()

        # create the graph
        pixel_points = self.__points_to_pixels(*points)
        self.graph = self.__create_graph()
        self.__draw_axis_numbers()
        self.__draw_bars(pixel_points, points, succes_number)
        self.graph.pack()

    def __pixels_per_x_y(self):
        """
        Calculates the amount of pixels available per 1 whole number based on
        the size of the graph

        :return: two floats that signify the amount of pixels for the x and
        y axis respectively
        """
        x_axis_pixel_size = self.GRAPH_WIDTH - self.IN_GRAPH_MARGIN
        y_axis_pixel_size = self.GRAPH_HEIGHT - self.IN_GRAPH_MARGIN
        x_axis_number_range = self.min_max_x_axis[1] - self.min_max_x_axis[0]
        y_axis_number_range = self.min_max_y_axis[1] - self.min_max_y_axis[0]

        pixels_per_1_x = x_axis_pixel_size / x_axis_number_range
        pixels_per_1_y = y_axis_pixel_size / y_axis_number_range
        return pixels_per_1_x, pixels_per_1_y

    def __create_graph(self):
        """
        Create a canvas with 2 axis on it.

        :return: a tkinter canvas object
        """
        graph = Canvas(self, bg='white', width=self.CANVAS_WIDTH,
                       height=self.CANVAS_HEIGHT, highlightthickness=0)
        # draw the x axis
        graph.create_line(self.SURROUNDING_MARGINS_LEFT,
                          self.CANVAS_HEIGHT - self.SURROUNDING_MARGINS_BOTTOM,
                          self.CANVAS_WIDTH - self.SURROUNDING_MARGINS_RIGHT,
                          self.CANVAS_HEIGHT - self.SURROUNDING_MARGINS_TOP)

        # draw y axis
        graph.create_line(self.SURROUNDING_MARGINS_LEFT,
                          self.SURROUNDING_MARGINS_BOTTOM,
                          self.SURROUNDING_MARGINS_LEFT,
                          self.CANVAS_HEIGHT - self.SURROUNDING_MARGINS_TOP)
        return graph

    def __draw_points(self, points, color, size=None):
        """
        Draw a list of points by there 2 dimensions

        :param points: a list of Point objects of 2 dimensions named x and y
        :param color: a string that is a tkinter readable color
        :param size: an optional parameter to change the size of the points to
        something other then self.DATA_POINT_SIZE
        """
        pixel_points = self.__points_to_pixels(*points)
        for point in pixel_points:
            half_data_point_size = int(0.5 * self.DATA_POINT_SIZE)
            if size is not None:
                half_data_point_size = int(0.5 * size)
            x0 = point.x - half_data_point_size
            y0 = point.y - half_data_point_size
            x1 = point.x + half_data_point_size
            y1 = point.y + half_data_point_size
            self.graph.create_oval(x0, y0, x1, y1, fill=color, outline=color)

    def __draw_bars(self, pixel_points, points, succes_number):
        bottom_y = self.GRAPH_HEIGHT + self.SURROUNDING_MARGINS_BOTTOM
        if self.MAX_DATA_POINTS > len(pixel_points):
            step = 1
        else:
            step = int(len(pixel_points) / self.MAX_DATA_POINTS)
        color = self.LOWER_COLOR
        for index in range(0, len(pixel_points), step):
            pixel_point = pixel_points[index]
            x = points[index].x
            if x < succes_number:
                color = self.LOWER_COLOR
            elif x == succes_number:
                color = self.EXACT_COLOR
            elif x > succes_number:
                if color == self.LOWER_COLOR:
                    color = self.EXACT_COLOR
                else:
                    color = self.HIGHER_COLOR
            self.graph.create_rectangle(pixel_point.x - 3, pixel_point.y, pixel_point.x + 3, bottom_y, fill=color)

    def __points_to_pixels(self, *points):
        """
        Converts a Point object with the original values to Point objects with
        those values set to there corresponding amount of pixels

        :param points: a list of Point objects of 2 dimensions named x and y
        :return: a list of Point objects of 2 dimensions named x and y
        """
        pixel_points = []
        for point in points:
            pixel_x = self.__x_number_to_pixels(point.x)[0]
            pixel_y = self.__y_number_to_pixels(point.y)[0]
            pixel_points.append(Point(pixel_x, pixel_y))
        return pixel_points

    def __x_number_to_pixels(self, *x_values):
        """
        Converts a list of x_values into pixel values that reflect the
        location of the x_values in pixels

        :param x_values: a list of floats within the range of
        self.min_max_x_axis
        :return: a list of floats within the area destined for the values
        """
        pixel_values = []
        for value in x_values:
            pixel_values.append(self.SURROUNDING_MARGINS_LEFT +
                                self.IN_GRAPH_MARGIN +
                                self.pixels_per_1_x *
                                (value - self.min_max_x_axis[0]))
        return pixel_values

    def __y_number_to_pixels(self, *y_values):
        """
        Converts a list of y_values into pixel values that reflect the
        location of the y_values in pixels

        :param y_values: a list of floats within the range of
        self.min_max_y_axis
        :return: a list of floats within the area destined for the values
        """
        pixel_values = []
        for value in y_values:
            pixel_values.append(self.CANVAS_HEIGHT -
                                (self.SURROUNDING_MARGINS_BOTTOM +
                                 self.IN_GRAPH_MARGIN + self.pixels_per_1_y *
                                 (value - self.min_max_y_axis[0])))
        return pixel_values

    def __draw_title(self, k, w):
        """
        Create a title for the graph

        :param k: the amount of clusters of the kmeans
        :param w: the w value of the kmeans
        """
        self.graph.create_text(int(self.CANVAS_WIDTH / 2), 10,
                               fill="black",
                               font="Ariel 13",
                               text="{}-means cluster (W = {})".format(k, w),
                               anchor="n")

    def __draw_axis_numbers(self):
        """
        Draws around self.MAX_AXIS_NUMBERS of numbers along each axis
        """
        x_axis_numbers = self.__get_axis_numbers(self.min_max_x_axis)
        y_axis_numbers = self.__get_axis_numbers(self.min_max_y_axis)
        x_axis_pixel_numbers = self.__x_number_to_pixels(*x_axis_numbers)
        y_axis_pixel_numbers = self.__y_number_to_pixels(*y_axis_numbers)
        for index, number in enumerate(x_axis_numbers):
            # if the number is outside the graph axis do not add it
            if x_axis_pixel_numbers[index] > self.CANVAS_WIDTH - self.SURROUNDING_MARGINS_RIGHT / 2:
                continue
            self.graph.create_text(x_axis_pixel_numbers[index],
                                   self.CANVAS_HEIGHT - self.SURROUNDING_MARGINS_BOTTOM,
                                   fill="black", font="Ariel 10", text=round(number, 2),
                                   anchor="n")
        for index, number in enumerate(y_axis_numbers):
            # if the number is outside the graph axis do not add it
            if y_axis_pixel_numbers[index] < self.SURROUNDING_MARGINS_TOP / 2:
                continue
            self.graph.create_text(self.SURROUNDING_MARGINS_LEFT - 5,
                                   y_axis_pixel_numbers[index],
                                   fill="black", font="Ariel 10", text=round(number, 2),
                                   anchor="e")

    def __get_axis_numbers(self, min_max):
        """
        Get a range of numbers to put along each of the two axis.

        :param min_max: a Point object with 2 dimensions min and max. These
        are needed to know the distance on the axis
        :return: a list of floats rounded to the nearest power of 10
        """
        axis_size = min_max[1] - min_max[0]
        distance_between_numbers = axis_size / self.MAX_AXIS_NUMBERS
        # find the power of 10 that the total distance is in and round it to
        # a full number
        power_of_10 = round(log10(distance_between_numbers))
        axis_numbers = []
        # round the distance to the nearest power of 10 (can be negative)
        rounded_distance = ceil(distance_between_numbers / 10 ** power_of_10) * 10 ** power_of_10
        for number in range(self.MAX_AXIS_NUMBERS):
            axis_number = min_max[0] + number * rounded_distance
            rounded_axis_number = round(axis_number / 10 ** power_of_10) * 10 ** power_of_10
            axis_numbers.append(rounded_axis_number)
        return axis_numbers
