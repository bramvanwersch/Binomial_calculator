from math import factorial


class BinomialDistribution:

    def __init__(self, succes_probability):
        self.probability_of_succes = succes_probability
        self.probability_of_failure = 1 - self.probability_of_succes
        self.previous_total_trials = -1  # value that cannot be taken to make sure that first calculation is always done
        self.result = None

    def calculate_distribution_probabilities(self, total_trials, progress_var):
        self.previous_total_trials = total_trials
        probabilities = []
        cumulative_probability = 0.0
        no_succeses = 0
        while cumulative_probability < 0.99999 and no_succeses <= total_trials:
            probability = self._binomial_probability(no_succeses, total_trials)
            probabilities.append(probability)
            cumulative_probability += probability
            no_succeses += 1
            # not most accurate but more relevant for the cases where this variable will actualy be seen
            progress_var.set(f"Calulating: {cumulative_probability * 100:.1f}%")
        self.result = BinomialResult(probabilities)

    def _binomial_probability(self, no_successes, total_trials):
        first_part = factorial(total_trials) / \
                     (factorial(total_trials - no_successes) * factorial(no_successes))
        second_part = self.probability_of_succes ** no_successes * \
                      self.probability_of_failure ** (total_trials - no_successes)
        return first_part * second_part


class BinomialResult:

    def __init__(self, all_probabilities):
        self.all_probabilities = all_probabilities

    def binomial_probability(self, nr_succeses):
        if nr_succeses >= len(self.all_probabilities):
            return 0
        return self.all_probabilities[nr_succeses - 1]

    def cumulative_smaller_then(self, nr_succeses):
        if nr_succeses >= len(self.all_probabilities):
            return 1.0
        return sum(self.all_probabilities[:nr_succeses - 1])

    def cumulative_smaller_then_or_equal(self, nr_succeses):
        if nr_succeses >= len(self.all_probabilities):
            return 1.0
        return sum(self.all_probabilities[:nr_succeses])

    def cumulative_greater_then(self, nr_succeses):
        if nr_succeses >= len(self.all_probabilities):
            return 0.0
        return sum(self.all_probabilities[nr_succeses + 1:])

    def cumulative_greater_then_or_equal(self, nr_succeses):
        if nr_succeses >= len(self.all_probabilities):
            return 0.0
        return sum(self.all_probabilities[nr_succeses:])

    def __len__(self):
        return len(self.all_probabilities)

    def __iter__(self):
        return iter(self.all_probabilities)
