# Civil-Unrest-Forecaster-FSE-Challenge

For this project, I was tasked with building a model that can forecast the probability of unrest one month in advance given **unrest.csv**, a dataset containing monthly indicators for 50 regions over a 10-year period.

Please clone this repository and run the Jupyter notebook to view my full solution and analysis.

---

### 🛠 Setup & Installation

In order to set up the proper virtual environment and requirements to run the notebook, please follow the instructions below:

1.  **Open Terminal** Run Anaconda prompt terminal as an **administrator** and navigate to the folder where the repository is located.

2.  **Create a Virtual Environment** Execute the following commands to set up your environment:
    ```bash
    # i. Create the environment
    conda create --name <env-name> python=3.12

    # ii. Activate the environment
    conda activate <env-name>

    # iii. Install dependencies
    pip install -r requirements.txt

    # iv. Install the ipykernel
    python -m ipykernel install --user --name=<env-name> --display-name "Python (<env-name>)"
    ```

3.  **Launch the Notebook** Navigate to the directory where you downloaded the notebook and run:
    ```bash
    jupyter notebook
    ```

---

### 🌐 Online Dashboard

In order to view the online dashboard where you will be able to select a region, select a month, and view the probability of unrest, please visit this link:

👉 **[civil-unrest-forecaster.vercel.app](https://civil-unrest-forecaster.vercel.app/)**
