# Splendia

Splendia is decomposed into 2 parts: 
- a web interface (i.e., the front-end of the project) found in the "front" repository
- a server containing the model and the AIs of the game (i.e., the back-end of the project) found in the "back" repository

# Splendia back-end
Python : 3.10.10

To run the server you need to:
1) Set your current working directory in the back repository
2) Create a python virtual environnement :
```
python -m venv env
```
3) Enter the virtual environnement:
```
source env/bin/activate
```
4) Install the necessary dependancies:
```
pip install -r requirements.txt
```
5) Run the server:
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
python traina_i.py
```


# Splendia front-end

Angular CLI: 14.2.11   
Node: 16.14  

## Run the front-end 
1) Navigate to the front directory.
2) Run `npm install` to install the dependencies.
3) Run `ng serve` for a dev server. 
4) Open `http://localhost:4200/` in an internet navigator. 

