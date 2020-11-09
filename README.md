# Visualization of multivariate, temporal trajectories using t-SNE trajectories

Increasingly available high-dimensional, longitudinal datasets extending over long periods of time, require novel, integrated data visualization techniques.
Dimensionality reduction methods like t-distributed stochastic neighbor embedding (Maaten & Hinton 2008) allows for visualizing high-dimensional data in low-dimensional (i.e., 2d,3d) spaces.

The script multivariate_temporal_trajectories_visualization.py allows for reading longitudinal, multi-dimensional data of arbitrary number of instances (objects) and transforms the provided data points into a 2d space using t-SNE. Then, the trajectories of each instance (object) are plotted in the t-SNE space (t-SNE trajectories). The script is based on matplotlib and scikit-learn.

Such a visualization enables visual interpretation of large amounts of data in an integrated manner. Moreover, the script allows for labelling selected objects in the first and last point in time.

The script exemplarily uses longitudinal data on population size, age, and sex for each country in the world for each decade from 1950-2020 (United Nations 2019). The resulting figure shows the world countries trajectories (1950-2020) in a t-SNE space of population size, age, and sex (blue=1950,red=2020):

# References
Maaten, L. V. D., & Hinton, G. (2008). Visualizing data using t-SNE. Journal of machine learning research, 9(Nov), 2579-2605.

United Nations, Department of Economic and Social Affairs, Population Division (2019). World Population Prospects 2019 - Special Aggregates, Online Edition. Rev. 1.

# Source datasets:
## Total Population - Both Sexes
https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/EXCEL_FILES/1_Population/WPP2019_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.xlsx
## Sex Ratio of Total Population
https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/EXCEL_FILES/1_Population/WPP2019_POP_F04_SEX_RATIO_OF_TOTAL_POPULATION.xlsx
## Median Age of Population
https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/EXCEL_FILES/1_Population/WPP2019_POP_F05_MEDIAN_AGE.xlsx


