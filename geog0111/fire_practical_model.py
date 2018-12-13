#!/usr/bin/env python
"""Fit the linear model of fire counts based on lagged teleconnnections.
"""

import numpy as np

import scipy.stats

__author__ = "J Gomez-Dans"
__copyright__ = "Copyright 2018 J Gomez-Dans"
__version__ = "1.0 (03.12.2018)"
__email__ = "j.gomez-dans@ucl.ac.uk"


def fit_model(telecon, peak_fire_month, fire_count_year, train_years=12):
    """Fits a linear model of fire counts using `train_years`. The telecon
    data is passed as `telecon`, and we also required the peak fire month
    (1-based, so January is 1), and the number of fire counts at the peak
    fire activity month per year.
    
    Parameters
    ------------
    telecon: ndarray
        A 2D array of `n_years*24`. Each row contains the previous 12 months
        as well as the current year
    peak_fire_month: ndarray
        A 2D spatial array where for each pixel, the fire peak month is defined.
        January is 1
    fire_count_year: ndarray
        A 3D dataset that holds the fire count for the peak fire month for all
        considered years
    train_years: int
        A subuset of years to train the model on
    
    Returns
    ----------
    A bunch of 2D arrays: slope, intercept, best_r2 and month of best lag.
    """
    nn, mm = peak_fire_month.shape
    slope = np.zeros_like(peak_fire_month) * 1.0
    intercept = np.zeros_like(peak_fire_month) * 1.0
    best_lag = np.zeros_like(peak_fire_month)
    best_r2 = np.zeros_like(peak_fire_month) * 1.0

    # Training
    for i in range(nn):
        for j in range(mm):
            pf_month = peak_fire_month[i, j] - 1  # 1-based month
            counts = fire_count_year[:train_years, i, j]
            # You get to use lager in a practical!
            reg = [
                scipy.stats.linregress(
                    telecon[:train_years, pf_month - lager], counts
                )
                for lager in range(0, -12, -1)
            ]

            iloc = np.argmax([x.rvalue ** 2 for x in reg])
            slope[i, j] = reg[iloc].slope
            intercept[i, j] = reg[iloc].intercept
            best_r2[i, j] = reg[iloc].rvalue ** 2
            best_lag[i, j] = 12 - iloc
    return slope, intercept, best_r2, best_lag
