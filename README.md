# Title register challenge

## Quick start

This app was developed using `python 3.8`. The easiest way to test it
is using the docker image.

First build it:

```
docker build -t extractor .
```

Then run the app:

```
docker run -it --rm extractor ./extract.py --json-file schedule_of_notices_of_lease_examples.json
```


If you don't want to use Docker, make sure to install `python3.8` with `pyenv`. You
will also need [poetry](https://python-poetry.org/docs/) to install the dependencies.

```
poetry install
poetry shell
./extract.py --json-file schedule_of_notices_of_lease_examples.json
```

## Testing

I have made a few tests for the entry texts. If you want to follow along,
you can run them with `py.test`

```
python -m pytest -v -s tests/test_parse_entry.py
```

## Design considerations


I've used `Poetry` just because I like the dependecy tree and the ability
to split the dev and normal dependencies. It also gives you a virtual environment
out-of-the-box.

The main libraries used are `ijson` and `pydantic.` The first is a convinient
way of parsing JSON files into python native types without too much of hassle as
it conververts JSON automatically. The downside is loading the whole file into
memory. I think using the lower-level API you can have a more memory efficient
way of parsing the file, but for the tech challenge I think the way it is is fine.

`Pydantic` is a good tool to parse data for correctness, either type or required
fields

The normal flow of the app is:

load JSON file -> for each **leaseschedule** parse the whole tree with pydantic -> parse the entry text

For the entry text, I've tried a few different things and the one that seems to work better is
to try to match the whitespace delimeters instead of a complex regex to catch all desired text.

Example:

```
21.01.2011      Parking space 166 (basement   01.12.2010      AGL226281
         10     16                        43  46        56    62
```

Positions 10-16 are the whitespaces delimeters between column 1 and 2. By finding
all delimeters for the whitespaces, I also get the information of the start of each
column. That helps for the cases where one column is skipped (just that whitespaces)
and the next one has data.

The caveat is relying on the first column to have 4 well defined columns which is not
the case for a few entries like:

```
 ITEM CANCELLED on 4 April 2018.
 Low Voltage Electricity       25.03.1993
 18.03.2005      Office Suite 3C, Second       26.10.1998
 4 Grotto Passage              20.02.1937
 2 and 4 Moxon Street          20.11.1905      105191
 16, 18 and 20 Moxon Street    23.12.1909      144131
 Parts of The Royal Free       13.03.1989      NGL636352
 Gas Governor and Connecting   24.02.1987      NGL587236
 02.04.2008      Equipment cubicle at roof     18.05.2007
```

I don't actually know what to do with the above as it clear have important
missing information like the title or the registration date. We could talk about this.

Another error is difficult-to-parse automatically fields. Take the below example

```
"entryText": [
    "12.12.2012      41 Boydell Court (fourth      23.11.2012      NGL930869  ",
    "4 (part of)     floor flat)                   From                       ",
    "23/11/2012 to              ",
    "22/11/2137"
]
```

It's an easy to parse structure but the last 2 lines are not part of the registration
data but the date of lease and term. I think a few different regex for each column can
be used to parse its correctness but more invesigation is needed.
