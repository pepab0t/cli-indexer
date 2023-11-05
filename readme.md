# CLI Indexer

CLI application for indexing and searching filesystem.

## Requirements
- python 3.10+

## Instalation
Application does not use any 3rd party library.
1. clone the project:
```bash
git clone https://github.com/pepab0t/cli-indexer.git
```
2. go to project directory
```bash
cd cli-indexer
```
3. In case of UNIX based OS, you can make `main.py` executable:
```bash
chmod +x main.py
```
```bash
# this way is possible to execute script without calling python interpreter
./main.py
```

## Get started
Run script without any argument or with just `help` argument to print manual. There are few alternatives:
```bash
python3 main.py help
python3 main.py
./main.py help
./main.py
```

This CLI can first create index of filesystem and use it for searching dirs, files and content, or it can search in runtime directly (based on command arguments).

### Example
> __Note:__ Colors in terminal might not work in powershell or windows cmd

Create index with
```bash
./main.py index ./file_struct
```
File `index.pkl` is created.\
Than use this index for searching:
```bash
./main.py info "xxx" -i index.pkl
```
You can see output in your terminal.\
Alternative to this approach is to search runtime:
```bash
./main.py info "xxx" ./file_struct
```
To display white text only add `--no-colors` option:
```bash
./main.py --no-colors info "xxx" ./file_struct
```


## More examples
Search for file content using index.pkl "xxx" in file that contains ".ext" in his path.
```bash
./main.py searchfdi "xxx" ".ext" -i index.pkl
```
Same but search runtime through directory ./file_struct:
```bash
./main.py searchfdi "xxx" ".ext" ./file_struct
```
Search using index.pkl for paths that contains "gmge":
```bash
./main.py searchfd "gmge" -i index.pkl
```
Alternative search runtime through ./file_struct filesystem:
```bash
./main.py searchfd "gmge" ./file_struct
```

## Indexing
Index models are located in app/index.py.\
For purpose of this application was used simple indexing method that pairs file path and file content in dictionary.\
Searching is performed as looping through keys and values of dictionary.\
Since this is the CLI application, index is stored in `.pkl` file.

### Other approach
Other approach was based on creating `.sqlite` database for indexing.\
This approach is not fully completed, but in `IndexDB` class is shown some methodic, how this could be implemented. Advantage of this approach would be faster searching, than looping dictionary. Continue reading to know the reason, why first approach was prefered.

Important to note, that storing index in database avoid holding all data in memory, compare to dictionary index. Assuming small example filesystem like `./file_struct`, we can relatively ignore this fact.

### Comparison
Comparison was performed on creating index for example filesystem `./file_struct`.
```
index.pkl took around 28 ms to create.
index.db  took around 56 ms to create.
```
```
search index.pkl took around 1 ms.
search index.db  took around 1 ms.
```
```
index.pkl needs around 150kB of storage (but also loaded to RAM).
index.db  needs around 300kB of storage.
```

As a result, database index needs more time to create, needs more storage, but for this example case does not offer significant benefits in terms of searching. This is the reason why I decided not to implement database index for all functionality.


## Compare index and runtime searching
Runtime searching is memory friendly and is suitable for process, when searching is performed once or there are not requirements for runtime.\
Meanwhile searching through index is significatly faster, but require additional storage to save index, which could have high impact, when indexing huge filesystems.

Benchmark performed on example filesystem `./file_struct`:
```
search runtime took around 65 ms
search index   took around  2 ms
```

## Developer notes
The core of application is `Indexer` and `SearchEngine` in module `app/core.py`. I decided to separate searching and indexing processes.\
Main part is `CLIApplication`, that can parse inputs, register and execute command.\
Several commands in `app.commands` submodule depends on core objects, that are accessed through Depencency injection, which happens in `main()` function. Individual commands does not depend on specific core objects implementation. This is done through `typing.Protocol` interfaces. Dependency injection and protocols allow code to be well testable. It's possible to test commands (if they setup execution and present results correctly) and core object functionality (searching and indexing logic) independently.\
There are also some entities (such as `OutputInfo` and `Occurance`) that ensures united output from searching processes. They also contain format methods to be able to represent outputs to the user.

### Testing notes
Commands are directly printing outputs to the terminal. In order to test those output, you can change default `sys.stdout` to other `TextIO`.

#### example output to file
```python
import sys

with open("foo.txt", "w") as f:
    sys.stdout = f
    print("baz bar")
```
This way `print` is writing to file, so `foo.txt` will contain "baz bar".

#### example output to string
```python
import sys
from io import StringIO

sio = StringIO()

sys.stdout = sio
print("bar baz")

content = sio.getvalue()

# change stdout to default
sys.stdout = sys.__stdout__

print(content)
# output: bar baz
```
This way, `content` contains what was printed.

## Limitations
App is not restricted to specific max directory size (in bytes), so it's highly recommended not to index large directories (like `~/Documents`). In case of searching through large dirs, prefer runtime searching that completely runs using iterators and runtime memory is not influenced by size of the target.

## Possible improvements
- use some CLI library for better, smarter and prettier implementation of CLI applications (such as [Typer](https://typer.tiangolo.com/))
- use better techniques, data structures and algorithms for indexing and searching
