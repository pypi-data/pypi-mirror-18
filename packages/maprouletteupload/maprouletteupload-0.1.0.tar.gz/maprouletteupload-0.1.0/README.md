# maprouletteupload

Simply upload a GeoJSON file of tasks to [Maproulette](http://maproulette.org/).

## Installation

```
pip install git+git://github.com/ebrelsford/maprouletteupload.git
```

## Usage

Use via the command line:

```
Usage: maprouletteupload [OPTIONS]

  Upload a GeoJSON file of tasks to Maproulette.

Options:
  --api-key TEXT          Your API key, via Maproulette.
  --challenge-id INTEGER  The challenge ID these tasks should be added to.
  --geojson-file TEXT     A GeoJSON file of tasks to upload. Alternatively,
                          you can provide this file via stdin.
  --identifier TEXT       The name of the property to use as the identifier.
                          Default: "identifier".
  --instruction TEXT      The name of the property to use as the instruction.
                          Default: "instruction".
  --name TEXT             The name of the property to use as the name.
                          Default: "name".
  --version               Show the version and exit.
  --help                  Show this message and exit.

```

A task is made for each GeoJSON feature and the tasks are bulk uploaded to Maproulette.


## License

MIT.
