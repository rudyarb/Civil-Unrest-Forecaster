# Civil-Unrest-Forecaster-FSE-Challenge
For this project, I was tasked with building a model that can forecast the probability of unrest one month in advance given unrest.csv, a dataset containing monthly indicators for 50 regions over a 10-year period.

Please clone this repository and run the Jupyter notebook to view my full solution and analysis.

In order to set up the proper virtual environment and requirements to run the notebook, please follow the instructions below:

1. Run Anaconda prompt terminal as an administrator and navigate to the folder where the repository is
2. Execute the following commands to create a virtual environment:
   i. conda create --name <env-name> python=3.12
   ii. conda activate <env-name>
   iii. pip install -r requirements.txt
   iv. python -m ipykernel install --user --name=<env-name> --display-name "Python (<env-name>)"
3. Navigate to the directory where you downloaded the notebook to and run Jupyter Notebook by executing this command: jupyter notebook

In order to run the web application where will be able to select a region, select a month, and view the probability of unrest, please follow the instructions below:

1. Open another Anaconda prompt and navigate to the folder where the repository is
2. Run this command: streamlit run unrest_predict.py

The web page will appear in the browser you are using.
   
