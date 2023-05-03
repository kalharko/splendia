# splendia back-end

To run the server you need to:
1) Create a python virtual environnement :
```
python -m venv .venv
```
2) Enter the virtual environnement:
```
source .venv/bin/activate
```
3) Install the necessary dependancies:
```
pip install -r requirements.txt
```
4) Run the server:
```
python run_server.py
```
\
To quit the virtual environnement:
```
deactivate
```
\
To run tests on the model :
```
python -m unittest -v
```
\
To train the AI:
1) Install torch:
```
pip install torch 
```
2) Install gymnasium 
```
pip install gymnasium
```
3) Run the training script:
```
python train_ai.py
```

