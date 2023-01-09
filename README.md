## The Sonar Data 

### Detecting a Rock or a Mine

Sonar (sound navigation ranging) is a technique that uses sound propagation (usually underwater, as in submarine navigation) to navigate, communicate with or detect objects on or under the surface of the water, such as other vessels.



The data set contains the response metrics for 60 separate sonar frequencies sent out against a known mine field (and known rocks). These frequencies are then labeled with the known object they were beaming the sound at (either a rock or a mine). 



Our main goal is to create a machine learning model capable of detecting the difference between a rock or a mine based on the response of the 60 separate sonar frequencies.


Data Source: https://archive.ics.uci.edu/ml/datasets/Connectionist+Bench+(Sonar,+Mines+vs.+Rocks)

### Tech Stack Used
1. Python 
2. FastAPI 
3. Machine learning algorithms
4. MongoDB

### Step 1: Clone the repository
```bash
git clone https://github.com/divyuk/sonar-vs-rock
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -n sonar python=3.7.6 -y
```

```bash
conda activate sensor
```

### Step 3 - Install the requirements
```bash
pip install -r requirements.txt
```

### Step 4 - Export the environment variable
```bash
export MONGODB_URL="mongodb+srv://<username>:<password>@clustersonar.gdhpjkz.mongodb.net/?retryWrites=true&w=majority"

```

### Step 5 - Run the application server

```bash
python app.py
```

### Step 6. Train application
```bash
http://localhost:8080/train
```

### Step 7. Prediction application
```bash
http://localhost:8080/predict
```