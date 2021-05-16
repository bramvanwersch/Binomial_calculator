from tkinter import *
from binomial_distribution import *
from distribution_graph import *
from utilities import ToolTip


class MainGui(Frame):
    PAD_SIZE = 10
    
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(padx=20, pady=20)
        self._warning_text = StringVar()
        self._is_graph_active = IntVar()
        self._binomial_probability = StringVar()
        self._cumulative1 = StringVar()
        self._cumulative2 = StringVar()
        self._cumulative3 = StringVar()
        self._cumulative4 = StringVar()
        self.graph_frame = None
        self.graph = None
        self.__init_widgets()

    def __init_widgets(self):
        self.warning_label = Label(self, textvariable=self._warning_text, fg='#f00')
        self.warning_label.grid(row=0, columnspan=6, padx=self.PAD_SIZE, pady=self.PAD_SIZE)

        self.__init_input_frame()
        self.__init_output_frame()

        self.calculate_button = Button(self, text="Calculate", command=self.generate_binomial_result)
        self.calculate_button.grid(row=2, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE)

        self.show_graph_button = Checkbutton(self, text="Show graph", variable=self._is_graph_active,
                                             command=self._generate_graph)
        self.show_graph_button.grid(row=2, column=2, padx=self.PAD_SIZE, pady=self.PAD_SIZE)

    def __init_input_frame(self):
        self.input_frame = LabelFrame(self, relief=GROOVE, text="Input parameters")
        self.input_frame.grid(row=1, columnspan=3, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        succes_probability_lbl = Label(self.input_frame, text="Succes probability:")
        succes_probability_lbl.grid(row=0, column=0, pady=self.PAD_SIZE, sticky=W)
        ToolTip(succes_probability_lbl, "The chance that a given action is a succes. Can be supplied as"
                                              " a fraction or as a divisional")

        self.succes_probability_input = Entry(self.input_frame)
        self.succes_probability_input.grid(row=0, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        total_trials_lbl = Label(self.input_frame, text="Total trials:")
        total_trials_lbl.grid(row=1, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)
        ToolTip(total_trials_lbl, "Total amount of actions performed")

        self.total_trials_input = Entry(self.input_frame)
        self.total_trials_input.grid(row=1, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        number_succeses_lbl = Label(self.input_frame, text="No. successes:")
        number_succeses_lbl.grid(row=2, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)
        ToolTip(number_succeses_lbl, "Number of successes out of the total trials")

        self.number_succeses_input = Entry(self.input_frame)
        self.number_succeses_input.grid(row=2, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

    def __init_output_frame(self):
        self.output_frame = LabelFrame(self, relief=GROOVE, text="Results")
        self.output_frame.grid(row=1, column=4, columnspan=3, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        binomial_probability_lbl = Label(self.output_frame, text="P(X = x):")
        binomial_probability_lbl.grid(row=0, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        self.binomial_probability_out_lbl = Label(self.output_frame, textvariable=self._binomial_probability)
        self.binomial_probability_out_lbl.grid(row=0, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        cumulative1_probability_lbl = Label(self.output_frame, text="P(X < x):")
        cumulative1_probability_lbl.grid(row=1, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        self.cumulative1_probability_out_lbl = Label(self.output_frame, textvariable=self._cumulative1)
        self.cumulative1_probability_out_lbl.grid(row=1, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        cumulative2_probability_lbl = Label(self.output_frame, text="P(X <= x):")
        cumulative2_probability_lbl.grid(row=2, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        self.cumulative2_probability_out_lbl = Label(self.output_frame, textvariable=self._cumulative2)
        self.cumulative2_probability_out_lbl.grid(row=2, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        cumulative3_probability_lbl = Label(self.output_frame, text="P(X > x):")
        cumulative3_probability_lbl.grid(row=3, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        self.cumulative3_probability_out_lbl = Label(self.output_frame, textvariable=self._cumulative3)
        self.cumulative3_probability_out_lbl.grid(row=3, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        cumulative4_probability_lbl = Label(self.output_frame, text="P(X >= x):")
        cumulative4_probability_lbl.grid(row=4, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        self.cumulative4_probability_out_lbl = Label(self.output_frame, textvariable=self._cumulative4)
        self.cumulative4_probability_out_lbl.grid(row=4, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

    def __init_graph_frame(self):
        self.graph_frame = LabelFrame(self, relief=GROOVE, text="Distribution:")
        self.graph_frame.grid(row=0, column=7, rowspan=3, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

    def generate_binomial_result(self):
        self._warning_text.set("")

        succes_probability = self._get_succes_probability_info()
        total_succeses = self._get_total_successes_info()
        total_trials = self._get_total_trials_info()
        if succes_probability is None or total_succeses is None or total_trials is None:
            return
        distribution = BinomialDistribution(succes_probability)
        try:
            result = distribution.get_succes_probabilites(total_trials, total_succeses)
        except ValueError as e:
            self._warning_text.set(str(e))
            return
        self.set_binomial_result(result)
        if self.graph_frame is not None:
            self._generate_graph()

    def set_binomial_result(self, result):
        self._binomial_probability.set(f"{result[0]:.2f}")
        self._cumulative1.set(f"{result[1]:.2f}")
        self._cumulative2.set(f"{result[2]:.2f}")
        self._cumulative3.set(f"{result[3]:.2f}")
        self._cumulative4.set(f"{result[4]:.2f}")

    def _get_succes_probability_info(self):
        str_prob = self.succes_probability_input.get()
        try:
            if "/" in str_prob:
                value = self._disect_division_notation(str_prob)
            else:
                value = float(str_prob)
            if value is None:
                return None
            if value < 0 or value > 1:
                self._warning_text.set("The succes probability has to be between 0 and 1")
                return None
            return value
        except ValueError:
            self._set_conversion_warning("succes probability", str_prob, float)
            return None

    def _disect_division_notation(self, str_prob):
        num1, num2 = str_prob.split("/")
        try:
            num1 = float(num1.strip())
            num2 = float(num2.strip())
        except ValueError:
            self._set_conversion_warning("succes probability", str_prob, float)
            return
        if num2 == 0:
            self._warning_text.set("Cannot divide by 0")
            return
        return num1 / num2

    def _get_total_successes_info(self):
        str_prob = self.number_succeses_input.get()
        try:
            value = int(str_prob)
            if value < 0:
                self._warning_text.set("The total amount of succeses has to be 0 or more")
                return None
            return value
        except ValueError:
            self._set_conversion_warning("number successes", str_prob, int)
            return None

    def _get_total_trials_info(self):
        str_prob = self.total_trials_input.get()
        try:
            value = int(str_prob)
            if value < 0:
                self._warning_text.set("The total amount of trials has to be 0 or more")
                return None
            return value
        except ValueError:
            self._set_conversion_warning("total trials", str_prob, int)
            return None

    def _set_conversion_warning(self, origin, value, type_):
        self._warning_text.set(f"'{value}' of {origin} cannot be converted to a {type_}.")

    def _generate_graph(self):
        if self._is_graph_active.get():
            self.__init_graph_frame()
            total_succeses = self._get_total_successes_info()
            if total_succeses is None:
                total_succeses = -1
            try:
                self.graph = BinomialDistributionGraph(self.graph_frame, self._generate_binomial_graph_data(),
                                                       total_succeses)
                self.graph.grid(row=0, column=0)
            except ZeroDivisionError:
                self._warning_text.set("Cannot draw graph. Not enough data points")
        else:
            self.graph_frame.grid_forget()
            self.graph_frame = None

    def _generate_binomial_graph_data(self):
        self._warning_text.set("")

        succes_probability = self._get_succes_probability_info()
        total_trials = self._get_total_trials_info()
        if succes_probability is None or total_trials is None:
            return []
        distribution = BinomialDistribution(succes_probability)
        try:
            data_points = distribution.get_distribution_probabilities(total_trials)
        except ValueError as e:
            self._warning_text.set(str(e))
            return
        points = [Point(index, point) for index, point in enumerate(data_points)]
        filtered_points = self._filter_low_points(points)
        return filtered_points

    def _filter_low_points(self, points):
        max_point = max(points, key=lambda x: x.y)
        min_y = 0.001 * max_point.y
        filtered_points = []
        for point in points:
            if point.y >= min_y:
                filtered_points.append(point)
        return filtered_points


def maingui():
    """
    Starting point of the gui and mainloop
    """
    root = Tk()
    # if sys.platform == 'win32':
    #     try:
    #         root.iconbitmap(default='{}{}visual_copys{}mgb.ico'.format(MGBPATH, os.sep, os.sep))
    #     except Exception:
    #         pass
    root.title('Binomial Distributions')

    MainGui(root)
    root.mainloop()


if __name__ == '__main__':
    maingui()
