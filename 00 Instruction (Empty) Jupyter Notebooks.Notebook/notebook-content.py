# Synapse Analytics notebook source

# METADATA ********************

# META {
# META   "synapse": {
# META     "lakehouse": {
# META       "default_lakehouse": "c95d7b56-9a7f-4b7c-baf4-ea0bdaacbbf7",
# META       "default_lakehouse_name": "PySparkLakehouse",
# META       "default_lakehouse_workspace_id": "e8b3335a-5e83-466c-bd0d-748c45da7cc9",
# META       "known_lakehouses": [
# META         {
# META           "id": "c95d7b56-9a7f-4b7c-baf4-ea0bdaacbbf7"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Spark notebooks + quick Python refresher

# MARKDOWN ********************

# ---

# MARKDOWN ********************

# Why use Notebooks? They make it very handy to:
# 
# - Try out code and experiment with it
# - Combine code with plots of your data
# - Annotate your code and findings with markdown, just like this text.
# - You don't need to rerun your script every time, but can choose parts of it: variables are kept in memory

# MARKDOWN ********************

# ---

# MARKDOWN ********************

# You can run code in a Notebook by using the shortcut <kbd>Shift</kbd> + <kbd>Enter</kbd> inside the code cell.<br>Let's write a welcome text assign it to a variable and use `print()` to get the output

# CELL ********************


# MARKDOWN ********************

# But a Notebook doesn't need the `print()` statement to print a variable. It will print the string representation of your variable when you just type it and then execute it with `Shift + Enter`. See what happens when you just run the code below:

# CELL ********************


# MARKDOWN ********************

# ---

# MARKDOWN ********************

# What is also very handy, is the <kbd>Ctrl</kbd> + <kbd>Space</kbd> inside functions: it shows you all the arguments of that function. See what happens for yourself if you use <kbd>Ctrl</kbd> + <kbd>Space</kbd> inside the `print()` function below:

# CELL ********************


# MARKDOWN ********************

# You can also get information about the documentation of the function, by putting a question mark `?` in front of it and running the cell. Please try below:

# CELL ********************


# MARKDOWN ********************

# ---

# MARKDOWN ********************

# Good to know is that you also run simple command line statements and other with so-called **magic commands**. They have a `%` in front of the statement. Below is an example with `ls`. This is not a python statement but it will run nevertheless.

# CELL ********************


# MARKDOWN ********************

# ---

# MARKDOWN ********************

# Converting your cell from code to markdown can be done by pressing <kbd>Ctrl</kbd> + <kbd>m</kbd> followed by <kbd>m</kbd> (you first press <kbd>Ctrl</kbd> + <kbd>m</kbd>, release, then press <kbd>m</kbd>):

# MARKDOWN ********************

# #### Just writing some markdown
# - bullet 1
# - bullet 2

# MARKDOWN ********************

# Let's try writing some markdown:

# CELL ********************


# MARKDOWN ********************

# ---

# MARKDOWN ********************

# You can create new code cells by pressing <kbd>Esc</kbd> followed by <kbd>a</kbd> (a stands for above). This is very much like an vim code editor. Please try to add some new code cells.

# MARKDOWN ********************

# The same goes for adding a new code cell below. This can be done by <kbd>Esc</kbd> followed by <kbd>b</kbd> (b stands for below)

# MARKDOWN ********************

# Deleting cells can be done with <kbd>Esc</kbd>, followed by <kbd>d</kbd> followed by <kbd>d</kbd>. Please delete the cells you just added above or below:

# CELL ********************


# MARKDOWN ********************

# ---

# MARKDOWN ********************

# Python has list over which you can easily iterate. Notice the 4 space indentation (or 1 tab).<br>Let's write a fruit list `['apples', 'banana', 2, 'oranges']` and loop over it.

# CELL ********************


# MARKDOWN ********************

# This is very different from other programming languages where you might write something like this. Here you can also see python's focus on ease and readability:

# CELL ********************


# MARKDOWN ********************

# Or even something like this:

# CELL ********************


# MARKDOWN ********************

# Slicing lists using brackets. Slicing starts at 0

# CELL ********************


# MARKDOWN ********************

# Getting the last element of a list

# CELL ********************


# MARKDOWN ********************

# ---

# MARKDOWN ********************

# Python dictionary: key value pairs, unordered.

# CELL ********************


# MARKDOWN ********************

# ---

# MARKDOWN ********************

# Defining a function with `def`:

# CELL ********************


# MARKDOWN ********************

# Everything you saw right here is exactly the same in regular Python, as it is in PySpark.

# CELL ********************

