# Refactoring Python Code talk

[Slides](https://littlepea.github.io/python-refactoring-talk/) and code for the "Refactoring Python Code" talk at the [Beijing Python Meetup](https://www.meetup.com/Beijing-Python/events/234021155/).

---

## Talk Description

* Title: Refactoring Python Code
* Duration: 1 hour
* Level: Intermediate
* Presenter: [Evgeny Demchenko](https://twitter.com/littlepea12)

## Summary

Refactoring is an extremely important technical practice for creating clean and maintainable code. 
It doesn't have to be clean, readable and idiomatic Python code from the beginning of the implementation 
as long as you don't forget to refactor it at the end. 

There are a lot of types of refactoring you can do to make your code better:

* Improve form (names, functions size, nesting)
* Improve style (PEP8/PyLint, pythonic code)
* Reduce duplication (DRY) and complexity (KISS)
* Apply design patterns (such as "Ports and Adapters")
* Apply SOLID principles (such as "Single Responsibility Principle")
* Improve code structure (modularity and composability)

In this talk, we're going to get our hands dirty by walking through some examples of all these types of refactoring 
applied to an existing application of aggregating movie reviews from multiple sources.
 
This is an Intermediate level talk but both beginners and advanced developers will find something new or useful here too.

---

### References:

* [Presentation Slides](https://littlepea.github.io/python-refactoring-talk/)
* [Pull Request](https://github.com/littlepea/python-refactoring-talk/pull/1/files?diff=unified)
* [Commits](https://github.com/littlepea/python-refactoring-talk/pull/1/commits)

---

## Running the example code

### Set up the environment

```
virtualenv env
. env/bin/activate
pip install -r requirements.txt
```

#### Make sure you have the following ENV vars set up:

* TWITTER_CONSUMER_KEY
* TWITTER_CONSUMER_SECRET
* TWITTER_ACCESS_TOKEN
* TWITTER_TOKEN_SECRET
* NY_TIMES_API_KEY

### Run "before" code

```
python before/movie_reviews.py Spy
```

Where "Spy" is the name of the movie to search reviews for.

### Run "after" code

```
python after/movie_reviews.py Spy
```

Where "Spy" is the name of the movie to search reviews for.

### Run the Jupyter notebook

```
jupyter notebook
```

### Create the slides

```
jupyter-nbconvert --to slides refactoring.ipynb --post serve
```
