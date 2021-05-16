# Binomial calculator

Simple application for calculating binomial distributions (see [wikipedia](https://en.wikipedia.org/wiki/Binomial_distribution)).

### Usage
Using the application is simple, there are 3 values to consider:
1. Succes probability: The chance that a given outcome (named a succes) is encountered
2. Total trials: The total amount that is rolled for an outcome
3. Number of succeses: The total number of succeses out of the total trials

The probability for the exact event is returned (P(X=x)) and cumulative probabilities that express the chance that the number of successes occured or a lower or larger
number of successes.

### Coin Example
To make it a bit clearer here an example with a coin:
The probability of a fair coin landing on heads is 0.5. So for the Succes probability we fill in 0.5. We trow the coin 100 times, meaning the Total trials is set to 100.
We observe heads 35 times out of a 100. So, we fill in 35 for the number of succeses. We can now see that this is very unlikely with a cumulative probability to observe this
number of heads or a lower number at 0.00089. See the image to see what it looks like in the GUI.
