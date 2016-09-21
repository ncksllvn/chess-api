# chess-api
A chess API written in Python using the Tornado web server that interfaces with the Stockfish engine.

To run this, it's probably best you set up a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) first 
in case the version of Python running on your machine isn't compatible with this project, which requires >=3.5.

Then you should just start the virtual environment, run `pip install -r requirements.txt` from the root of the project 
to install the dependencies, and then start it with `python3 main.py`.

Right now Windows isn't supported because I haven't added the corresponding Stockfish exe yet.

