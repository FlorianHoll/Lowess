"""Unit tests for the linear regression classes."""
import numpy as np
from sklearn.linear_model import LinearRegression as SKLearnLinearRegression

from loess.regression import LinearRegression


class TestLinearRegression:
    """Tests for the (ordinary) linear regression."""

    @staticmethod
    def test_linear_regression_recognizes_pattern():
        """
        GIVEN a data generating pattern
        WHEN a linear regression is fit
        THEN the pattern should be recognized.
        """
        x = np.random.normal(size=50).reshape(25, 2)
        y = 3 + 2 * x[:, 0] - 0.75 * x[:, 1]
        model = LinearRegression()
        model.fit(x, y)
        assert np.all(model.coef_.round(5) == np.r_[2.0, -0.75].round(5))
        assert round(model.intercept_, 3) == 3

    @staticmethod
    def test_results_match_sklearn():
        """
        GIVEN some data and a target
        WHEN a linear regression is fit
        THEN the results should match the sklearn results.
        """
        x = np.random.normal(size=50).reshape(25, 2)
        y = np.random.normal(size=25).reshape(-1, 1)
        model = LinearRegression()
        model.fit(x, y)
        sklearn_model = SKLearnLinearRegression()
        sklearn_model.fit(x, y)

        # check that estimated coefficients match.
        assert np.all(
            sklearn_model.coef_.round(10).flatten() == model.coef_.round(10).flatten()
        )
        assert sklearn_model.intercept_[0].round(10) == model.intercept_.round(10)

        # check that prediction matches.
        new_x = np.random.normal(size=100).reshape(50, 2)
        assert np.all(
            sklearn_model.predict(new_x).round(10) == model.predict(new_x).round(10)
        )

    @staticmethod
    def test_prediction_works_as_expected():
        """
        GIVEN a data generating pattern
        WHEN the linear regression picked up on that pattern
        THEN it should also be visible in prediction.
        """
        x = np.random.normal(size=50).reshape(25, 2)
        y = 3 + 2 * x[:, 0] - 0.75 * x[:, 1]
        model = LinearRegression()
        model.fit(x, y)
        new_x = np.random.normal(size=100).reshape(50, 2)
        y = 3 + 2 * new_x[:, 0] - 0.75 * new_x[:, 1]
        assert np.all(y.round(10) == model.predict(new_x).round(10))

    @staticmethod
    def test_polynomials_work():
        """
        GIVEN some data generating pattern
        WHEN a polynomial linear regression is fit
        THEN it should be able to pick up on that trend.
        """
        x = np.random.normal(size=100).reshape(50, 2)
        y = (
            3
            + 2 * x[:, 0]
            + 0.5 * x[:, 1]
            + 0.8 * np.power(x[:, 0], 2)
            - 0.25 * np.power(x[:, 1], 2)
        )
        model = LinearRegression(polynomial_degree=2)
        model.fit(x, y)
        assert np.all(model.coef_.round(10) == np.r_[2.0, 0.5, 0.8, -0.25].round(10))
        assert model.intercept_.round(10) == 3.0

        # Test if prediction works as well.
        new_x = np.random.normal(size=20).reshape(10, 2)
        new_y = (
            3
            + 2 * new_x[:, 0]
            + 0.5 * new_x[:, 1]
            + 0.8 * np.power(new_x[:, 0], 2)
            - 0.25 * np.power(new_x[:, 1], 2)
        )
        assert np.all(model.predict(new_x).round(10) == new_y.round(10))

    def test_higher_polynomials_work(self):
        """
        GIVEN some data generating pattern
        WHEN a polynomial linear regression is fit
        THEN it should be able to pick up on that trend.
        """
        x = np.random.normal(size=100).reshape(50, 2)
        y = (
            3
            + 2 * x[:, 0]
            + 0.5 * x[:, 1]
            + 0.8 * np.power(x[:, 0], 2)
            - 0.25 * np.power(x[:, 1], 2)
            + 0.25 * np.power(x[:, 0], 3)
            + 0.7 * np.power(x[:, 1], 3)
            + 0.346 * np.power(x[:, 0], 4)
            + 0.025 * np.power(x[:, 1], 4)
            + 0.05 * np.power(x[:, 0], 5)
            + 0.078 * np.power(x[:, 1], 5)
        )
        model = LinearRegression(polynomial_degree=5)
        model.fit(x, y)
        true_coefficients = np.r_[
            2.0, 0.5, 0.8, -0.25, 0.25, 0.7, 0.346, 0.025, 0.05, 0.078
        ]
        assert np.all(model.coef_.round(10) == true_coefficients.round(10))
        assert model.intercept_.round(10) == 3.0

        # Check that prediction works.
        new_x = np.random.exponential(size=150).reshape(75, 2)
        new_y = (
            3
            + 2 * new_x[:, 0]
            + 0.5 * new_x[:, 1]
            + 0.8 * np.power(new_x[:, 0], 2)
            - 0.25 * np.power(new_x[:, 1], 2)
            + 0.25 * np.power(new_x[:, 0], 3)
            + 0.7 * np.power(new_x[:, 1], 3)
            + 0.346 * np.power(new_x[:, 0], 4)
            + 0.025 * np.power(new_x[:, 1], 4)
            + 0.05 * np.power(new_x[:, 0], 5)
            + 0.078 * np.power(new_x[:, 1], 5)
        )
        assert np.all(model.predict(new_x).round(5) == new_y.round(5))
