from math import factorial


class BinomialDistribution:

    def __init__(self, succes_probability):
        self.probability_of_succes = succes_probability
        self.probability_of_failure = 1 - self.probability_of_succes

    def get_succes_probabilites(self, total_trials, total_successes):
        if total_trials < total_successes:
            raise ValueError(f"Total trials has to be bigger than or equal to total "
                             f"successes")
        probabilities = []
        for no_successes in range(total_successes + 1):
            probability = self._binomial_probability(no_successes, total_trials)
            probabilities.append(probability)
        return BinomialResult(probabilities)

    def get_distribution_probabilities(self, total_trials):
        probabilities = []
        cumulative_probability = 0
        no_succeses = 0
        while cumulative_probability < 0.5:
            probability = self._binomial_probability(no_succeses, total_trials)
            probabilities.append(probability)
            cumulative_probability += probability
            no_succeses += 1
        probabilities = probabilities + probabilities[::-1]
        return probabilities

    def _binomial_probability(self, no_successes, total_trials):
        first_part = factorial(total_trials) / \
                     (factorial(total_trials - no_successes) * factorial(no_successes))
        second_part = self.probability_of_succes ** no_successes * \
                      self.probability_of_failure ** (total_trials - no_successes)
        return first_part * second_part


class BinomialResult:

    def __init__(self, succes_probabilities):
        self._succes_probabilities = succes_probabilities
        self.binomial_probability = self._succes_probabilities[-1]
        self.cumulative_smaller_then = sum(self._succes_probabilities[:-1])
        self.cumulative_smaller_then_or_equal = sum(self._succes_probabilities)
        self.cumulative_larger_then = 1 - self.cumulative_smaller_then_or_equal
        self.cumulative_larger_then_or_equal = 1 - self.cumulative_smaller_then

    def __getitem__(self, item):
        return self.all_results()[item]

    def all_results(self):
        return [
            self.binomial_probability,
            self.cumulative_smaller_then,
            self.cumulative_smaller_then_or_equal,
            self.cumulative_larger_then,
            self.cumulative_larger_then_or_equal
        ]


if __name__ == '__main__':
    d = BinomialDistribution(0.5)
    results = d.get_succes_probabilites(10, 2)
    print(results.all_results())
