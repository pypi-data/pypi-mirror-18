# [pyp-w3] Jobs Detector

Today we will develop a command line tool which aims to parse certain websites looking for job statistics based on given keywords. In this very first version of the tool, we will only implement a parser for the HackerNews blog, which includes a monthly report of "Who is hiring?". Example: https://news.ycombinator.com/item?id=11814828

## Command usage

The command line tool must be accessible by calling `jobs_detector` command. A `hacker_news` subcommand must be also available as part of this implementation.

To see the whole list of optional and mandatory parameters, you can execute the command using the `--help` flag.

```bash
$ jobs_detector hacker_news --help
Options:
  -i, --post-id TEXT       [required]
  -k, --keywords TEXT
  -c, --combinations TEXT
  --help                   Show this message and exit.
```

### Default arguments

To request jobs statistics using a default set of keywords, just call the `hacker_news` subcommand providing a valid HN post id (see the last part of the sample URL above), like this:

```bash
$ jobs_detector hacker_news -i 11814828
Total job posts: 888

Keywords:
Remote: 174 (19%)
Postgres: 81 (9%)
Python: 144 (16%)
Javascript: 118 (13%)
React: 133 (14%)
Pandas: 5 (0%)
```

### Keywords filtering

For statistics about a sub set of the default keywords, or even custom keywords out of the default set you can specify the `-k` or `--keywords` options, as a comma separated list of values.

```bash
$ jobs_detector hacker_news -i 11814828 -k python,django,ruby
Total job posts: 889

Keywords:
Python: 144 (16%)
Ruby: 80 (8%)
Django: 36 (4%)
```

### Combination stats

It's also possible to request statistics of certain combination of keywords. For example, how many offers are asking for "remote", "python", and "flask" at the same time?. To do that, use the `-c` or `-combinations` option.

```bash
$ jobs_detector hacker_news -i 11814828 -c remote-python-flask,remote-django
Total job posts: 888

Keywords:
Remote: 174 (19%)
Postgres: 81 (9%)
Python: 144 (16%)
Javascript: 118 (13%)
React: 133 (14%)
Pandas: 5 (0%)

Combinations:
Remote-Python-Flask: 2 (0%)
Remote-Django: 6 (0%)
```

Feel free to extend the functionality of this command by adding extra parameters or even more subcommands to parse different websites.

## Your command available in pypi

Finally, to wrap up this group work, you must make your command tool available in pypi (Python Package Index). Any person out there must be able to use the `pip` command and install a local version of your project. To do this, we will follow some naming conventions so we don't have conflicts between each other. This is the naming convention you must follow for your package: `rmotr-bX-cY-gZ-jobs-detector`, where `X`, `Y` and `Z` are the batch number, course number and group number respectively.

Anyone should be able to install the package by executing, for example: `pip install rmotr-b6-c1-g3-jobs-detector`.

Here you have a very detailed guide about how to upload things to pypi: https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
