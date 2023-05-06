# Splendia

Splendia is decomposed into 2 parts: 
- a web interface (i.e., the front-end of the project) found in the "front" repository
- a server containing the model and the AIs of the game (i.e., the back-end of the project) found in the "back" repository

To run Splendia, you need to run both the back-end and the front-end.
You can find more information on how to run:
- the back-end in the README file of the "back" repository
- the front-end in the README file of the "front" repository


# Splendia back-end

To run the server you need to:
1) Create a python virtual environnement :
```
python -m venv env
```
2) Enter the virtual environnement:
```
source env/bin/activate
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
python traina_i.py
```


# Splendia front-end

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 13.3.3.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.
