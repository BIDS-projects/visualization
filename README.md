# Visualization

End product, map and visualization as a recommendation engine

[website](http://bidsiem.herokuapp.com)

# Installation

Clone the repository.

```
git clone git@github.com:BIDS-projects/visualization
```

Setup your virtual environment. The following will create a new environment called `visualization`.
a
```
conda create -n visualization python=2.7
```

Activate your virtual environment, and install all dependencies from `requirements.txt`.

```
source activate visualization
pip install -r requirements.txt
```

Installation complete. See "How to Use" to get started.

# How to Use

Make sure to activate your virtual environment, if you haven't already. (If you are in the environment, your prompt will be prefixed by `(visualization)`)

```
source activate visualization
```

Run the application.

```
python run.py
```

# Deployment

## Heroku

This repository to Heroku-ready! Go ahead and push to a Heroku app.

```
git push heroku master
```
