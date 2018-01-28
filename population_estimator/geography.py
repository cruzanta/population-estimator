#!/usr/bin/env python


class Geography:
    """Class for storing a geography's population data.

    Attributes:
        name: A string containing the name of a geography.
        annual_pop_ests: A list of population estimates represented as integers.
        first_pop_est: An integer that represents a geography's first population
            estimate.
        most_recent_pop_est: An integer that represents a geography's most
            recent population estimate.
        cagr: A float that represents a geography's compound annual growth rate.
    """

    def __init__(self, name, annual_population_estimates):
        self.name = name
        self.annual_pop_ests = annual_population_estimates
        self.first_pop_est = self.annual_pop_ests[0]
        self.most_recent_pop_est = self.annual_pop_ests[-1]
        self.cagr = self.get_compound_annual_growth_rate()

    def get_compound_annual_growth_rate(self):
        # Calculates and returns a geography's compound annual growth rate.
        beginning_pop = float(self.first_pop_est)
        ending_pop = self.most_recent_pop_est
        num_years = float(len(self.annual_pop_ests))

        return (ending_pop / beginning_pop)**(1 / num_years) - 1

    def get_projected_population(self, most_recent_year, projected_year):
        # Calculates and returns a geography's projected population estimate for
        # a future year.
        starting_pop = self.most_recent_pop_est
        cagr_plus_one = self.cagr + 1
        num_years = projected_year - most_recent_year
        future_pop = starting_pop * (cagr_plus_one)**num_years

        return int(round(future_pop, 0))
