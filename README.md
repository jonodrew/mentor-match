# Mentor Match

This is a package to help match mentees and mentors. It's specifically designed for a volunteer programme I support, but you could probably extend or alter it to suit whatever you're doing.

It uses [this implementation of Munkres](https://github.com/bmc/munkres) to find the most effective pairings. The Munkres algorithm works on a grid of scores.

## Scoring

Full details of how the matches are calculated can be read in the code itself.

## Setup

If you've never done Python before in your life this project might not be for you. On the other hand, I think the code is
beautiful and I've made an effort with the documentation, and you can [find me on twitter](https://www.twitter.com/jonodrew)
if you need to ask me questions, so what the heck. Let's get stuck in.

You will need:

- Python 3.6+ : I've used type hinting throughout, which was only introduced in Python 3.6
- admin rights, or at least enough rights to install stuff
- `git`
- a file of mentors and mentees. Next update will include a template input file. These files should be called "mentees.csv"
and "mentors.csv"

Start by [cloning this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository).
Then [set up a virtual environment](https://docs.python.org/3/library/venv.html), to make sure the things you're about to
install don't mess around with your base system. Now activate it following the instructions. Now install the requirements for this
project: `pip install -r requirements.txt`

Now type `python match.py path/to/folder/with/my/data` and hit return. It should run quietly for up to five minutes and then
spit out an `output` folder with two files. These are your matched mentors/mentees!

This software also exists as a web application. To run it locally, run the following commands in your terminal:
```
export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run
```
This will run the Flask server locally, and you'll be able to see it running at http://127.0.0.1:5000/
