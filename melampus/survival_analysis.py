import pandas as pd
from lifelines import KaplanMeierFitter, NelsonAalenFitter, CoxPHFitter
from melampus.preprocessor import MelampusPreprocessor


class MelampusSurvivalAnalyzer(MelampusPreprocessor):
    """
    MelampusSurvivalAnalyzer is used for two kinds of survival analysis:  and regression. For

    - 1. Analysis for univariate models using **Kaplan-Meier** or **Nelson-Aalen** approach
    - 2. Survival regression using **Cox's model**

    :param filename: The name of the csv file that includes the data
    :type filename: str, required
    :param time_column: The column name of the duration variable
    :type time_column: str, required
    :param event_column: The column name of the observed event variable
    :type event_column: str, required
    """

    def __init__(self, filename: str, time_column: str, event_column: str):
        # Change the initialization of data, as we don't have a single outcomes array like for classification
        self.data = pd.read_csv(filename)
        self.time_column = time_column
        self.event_column = event_column
        self.T = pd.Series  # time variable
        self.E = pd.Series  # event variable
        self.analyzer = CoxPHFitter(penalizer=0.1)

    def train(self):
        """
        Train the model based on desired algorithm.

        :return: the trained analyzer as a python object and the concordance index
        """

        try:
            self.analyzer.fit(self.data, duration_col=self.time_column, event_col=self.event_column, show_progress=True)
            self.analyzer.print_summary()
        except Exception as e:
            raise Exception(str(e))

        return self.analyzer, self.analyzer.concordance_index_
