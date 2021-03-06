from tkinter import *
from binomial_distribution import *
from distribution_graph import *
from utilities import ToolTip, readable_round_result
from threading import Thread


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
        self.distribution = None
        self.__init_widgets()

    def __init_widgets(self):
        self.warning_label = Label(self, textvariable=self._warning_text, fg='#f00')
        self.warning_label.grid(row=0, columnspan=6, padx=self.PAD_SIZE, pady=self.PAD_SIZE)

        self.__init_input_frame()
        self.__init_output_frame()

        self.calculate_button = Button(self, text="Calculate", command=self.calculate_binomial_result)
        self.calculate_button.grid(row=2, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE)

        self.show_graph_button = Checkbutton(self, text="Show graph", variable=self._is_graph_active,
                                             command=self._toggle_graph)
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
        ToolTip(binomial_probability_lbl, "Exact probability of the number of succeses")

        self.binomial_probability_out_lbl = Label(self.output_frame, textvariable=self._binomial_probability)
        self.binomial_probability_out_lbl.grid(row=0, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        cumulative1_probability_lbl = Label(self.output_frame, text="P(X < x):")
        cumulative1_probability_lbl.grid(row=1, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)
        ToolTip(cumulative1_probability_lbl, "Cumulative probability for number of succeses - 1 and any number"
                                             " of succeses smaller than that")

        self.cumulative1_probability_out_lbl = Label(self.output_frame, textvariable=self._cumulative1)
        self.cumulative1_probability_out_lbl.grid(row=1, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        cumulative2_probability_lbl = Label(self.output_frame, text="P(X <= x):")
        cumulative2_probability_lbl.grid(row=2, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)
        ToolTip(cumulative2_probability_lbl, "Cumulative probability for number of succeses and any number of succeses "
                                             "smaller than that")

        self.cumulative2_probability_out_lbl = Label(self.output_frame, textvariable=self._cumulative2)
        self.cumulative2_probability_out_lbl.grid(row=2, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        cumulative3_probability_lbl = Label(self.output_frame, text="P(X > x):")
        cumulative3_probability_lbl.grid(row=3, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)
        ToolTip(cumulative3_probability_lbl, "Cumulative probability for number of succeses + 1 and any number"
                                             " of succeses larger than that")

        self.cumulative3_probability_out_lbl = Label(self.output_frame, textvariable=self._cumulative3)
        self.cumulative3_probability_out_lbl.grid(row=3, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

        cumulative4_probability_lbl = Label(self.output_frame, text="P(X >= x):")
        cumulative4_probability_lbl.grid(row=4, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)
        ToolTip(cumulative4_probability_lbl, "Cumulative probability for number of succeses and any number of succeses "
                                             "larger than that")

        self.cumulative4_probability_out_lbl = Label(self.output_frame, textvariable=self._cumulative4)
        self.cumulative4_probability_out_lbl.grid(row=4, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

    def __init_graph_frame(self):
        if self.graph_frame is None:
            self.graph_frame = LabelFrame(self, relief=GROOVE, text="Distribution:")
            self.graph_frame.grid(row=0, column=7, rowspan=3, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=W)

    def calculate_binomial_result(self):
        thread = Thread(target=self.display_binomial_result, daemon=True)
        thread.start()

    def display_binomial_result(self):
        self._warning_text.set("")
        try:
            succes_nr = self._get_total_successes_info()
            self._generate_binomial_result()
        except ValueError as e:
            self._warning_text.set(str(e))
            return
        self.set_binomial_result(succes_nr)
        if self.graph_frame is not None:
            self._toggle_graph()

    def _generate_binomial_result(self):
        try:
            succes_probability = self._get_succes_probability_info()
            total_trials = self._get_total_trials_info()
        except ValueError as e:
            raise e
        if self.distribution is None or succes_probability != self.distribution.probability_of_succes or \
                total_trials != self.distribution.previous_total_trials:
            self.distribution = BinomialDistribution(succes_probability)
            try:
                self.distribution.calculate_distribution_probabilities(total_trials, self._warning_text)
            except OverflowError as e:
                raise self._warning_text.set(str(e))
        self._warning_text.set("")

    def set_binomial_result(self, succes_nr):
        result = self.distribution.result
        self._binomial_probability.set(readable_round_result(result.binomial_probability(succes_nr), 5))
        self._cumulative1.set(readable_round_result(result.cumulative_smaller_then(succes_nr), 5))
        self._cumulative2.set(readable_round_result(result.cumulative_smaller_then_or_equal(succes_nr), 5))
        self._cumulative3.set(readable_round_result(result.cumulative_greater_then(succes_nr), 5))
        self._cumulative4.set(readable_round_result(result.cumulative_greater_then_or_equal(succes_nr), 5))

    def _get_succes_probability_info(self):
        str_prob = self.succes_probability_input.get()
        if "/" in str_prob:
            value = self._disect_division_notation(str_prob)
        else:
            try:
                value = float(str_prob)
            except ValueError:
                raise ValueError(self._get_conversion_warning("succes probability", str_prob, float))
        if value < 0 or value > 1:
            raise ValueError("The succes probability has to be between 0 and 1")
        return value

    def _disect_division_notation(self, str_prob):
        num1, num2 = str_prob.split("/")
        try:
            num1 = float(num1.strip())
            num2 = float(num2.strip())
        except ValueError:
            raise ValueError(self._get_conversion_warning("succes probability", str_prob, float))
        if num2 == 0:
            raise ValueError("Cannot divide by 0")
        return num1 / num2

    def _get_total_successes_info(self):
        str_prob = self.number_succeses_input.get()
        try:
            value = int(str_prob)
        except ValueError:
            raise ValueError(self._get_conversion_warning("number successes", str_prob, int))
        if value < 0:
            raise ValueError("The total amount of succeses has to be 0 or more")
        return value

    def _get_total_trials_info(self):
        str_prob = self.total_trials_input.get()
        try:
            value = int(str_prob)
        except ValueError:
            raise ValueError(self._get_conversion_warning("total trials", str_prob, int))
        if value < 0:
            raise ValueError("The total amount of trials has to be 0 or more")
        return value

    def _get_conversion_warning(self, origin, value, type_):
        return f"'{value}' of {origin} cannot be converted to a {type_}."

    def _toggle_graph(self):
        if self._is_graph_active.get():
            self.calculate_graph()
        else:
            self.graph_frame.grid_forget()
            self.graph_frame = None

    def calculate_graph(self):
        thread = Thread(target=self._generate_graph, daemon=True)
        thread.start()

    def _generate_graph(self):
        self.__init_graph_frame()
        try:
            total_succeses = self._get_total_successes_info()
        except ValueError:
            total_succeses = -1
        if self.graph is not None:
            self.graph.grid_forget()
        try:
            self._generate_binomial_result()
        except ValueError as e:
            self._warning_text.set(str(e))
            return
        points = [Point(index, point) for index, point in enumerate(self.distribution.result)]
        filtered_points = self._filter_low_points(points)
        try:
            self.graph = BinomialDistributionGraph(self.graph_frame, filtered_points, total_succeses)
            self.graph.grid(row=0, column=0)
        except ZeroDivisionError:
            self._warning_text.set("Cannot draw graph. Not enough data points")
            return
        self._warning_text.set("")

    def _filter_low_points(self, points):
        max_remove_points = len(points) - BinomialDistributionGraph.MAX_DATA_POINTS
        if max_remove_points <= 0:
            return points
        sorted_points = sorted(points, key=lambda x: x.y)
        min_y = 0.001 * sorted_points[-1].y
        index = 0
        for index, point in enumerate(sorted_points):
            if point.y >= min_y or index >= max_remove_points:
                break
        unsorted_points = sorted(sorted_points[index:], key=lambda x: x.x)
        return unsorted_points


def maingui():
    """
    Starting point of the gui and mainloop
    """
    root = Tk()
    if sys.platform == 'win32':
        try:
            root.iconbitmap("images\\logo.ico")
        except Exception as e:
            pass
    root.title('Binomial Distributions')

    MainGui(root)
    root.mainloop()


if __name__ == '__main__':
    maingui()
