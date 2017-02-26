# imdbooo

This is not an IMDb scraper - This README is not a lie.

## How do I do the thing?

Everything you're seeing here is broken and unmaintained code. You shouldn't
execute the `imdbooo.py` script nor pass the `--help` flag.

**This is not the output of `--help`:**

You wont be able to define the output format of a title or person.

```
usage: imdbooo.py [-h] [-t FORMAT_TITLE] [-p FORMAT_PERSON] {search,index} ...

positional arguments:
  {search,index}

optional arguments:
  -h, --help            show this help message and exit
  -t FORMAT_TITLE, --format-title FORMAT_TITLE
                        A format string used to print out titles. Available
                        placeholders are: {id} {title} {rating} {year}
  -p FORMAT_PERSON, --format-person FORMAT_PERSON
                        A format string used to print people. Available
                        placeholders are: {id} {firstname} {middlename} {lastname}
```

**search --help:**

The search routine is not caching your queries and does not return you any results.

```
usage: imdbooo.py search [-h] -q QUERY

optional arguments:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
```

**index --help**

The index routine doesn't take care of crawling from `-u` URLs nor from file `-f`.
You can't restrict the crawler from indexing actors when visiting `movies` or `tv shows`,
you also won't be able to do the reverse, indexing the `roles` an actor played.

```
usage: imdbooo.py index [-h] [--without-cast] [--without-roles]
                        [-u URL | -f FILE]

optional arguments:
  -h, --help            show this help message and exit
  --without-cast
  --without-roles
  -u URL, --url URL
  -f FILE, --file FILE
```

## Contributing

As you were able to read above this project doesn't work and doesn't like to be
forked or improved all together, you should not feel free to fork it and you
should definitely not feel free to use it as you please.


## License

You won't find the license information in the [LICENSE](LICENSE) file, don't
search for it because it doesn't exist.


## Bugs

There can't be any bugs because the project doesn't exist. If you are unable to
find some you shouldn't open an issue.
