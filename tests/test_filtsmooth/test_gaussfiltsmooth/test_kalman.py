import numpy as np
import pytest

import probnum.problems.zoo.filtsmooth as filtsmooth_zoo
from probnum import filtsmooth

# Problems


@pytest.fixture(params=[filtsmooth_zoo.car_tracking, filtsmooth_zoo.ornstein_uhlenbeck])
def setup(request):
    """Filter and regression problem."""
    problem = request.param
    regression_problem, statespace_components = problem()

    kalman = filtsmooth.Kalman(
        statespace_components["dynamics_model"],
        statespace_components["measurement_model"],
        statespace_components["initrv"],
    )
    return kalman, regression_problem


def test_rmse_filt_smooth(setup):
    """Assert that smoothing beats filtering beats nothing."""

    np.random.seed(12345)
    kalman, regression_problem = setup
    truth = regression_problem.solution

    posterior = kalman.filtsmooth(regression_problem)

    filtms = posterior.filtering_posterior.states.mean
    smooms = posterior.states.mean

    filtms_rmse = np.mean(np.abs(filtms[:, :2] - truth[:, :2]))
    smooms_rmse = np.mean(np.abs(smooms[:, :2] - truth[:, :2]))
    obs_rmse = np.mean(np.abs(regression_problem.observations - truth[:, :2]))

    assert smooms_rmse < filtms_rmse < obs_rmse
