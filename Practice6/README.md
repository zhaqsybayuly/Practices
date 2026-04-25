# Practice 6 — File Handling and Built-in Functions

Examples covering Python file I/O, directory management and common built-in functions.

## Structure

```
Practice6/
├── file_handling/
│   ├── write_files.py        # create + append a text file
│   ├── read_files.py         # read(), readline(), readlines()
│   └── copy_delete_files.py  # shutil.copy + os.remove
├── directory_management/
│   ├── create_list_dirs.py   # makedirs, listdir, find by extension, rmdir
│   └── move_files.py         # shutil.copy + shutil.move
└── builtin_functions/
    ├── map_filter_reduce.py        # map, filter, reduce + len/sum/min/max/sorted
    └── enumerate_zip_examples.py   # enumerate, zip, type conversions
```

## Run

Run scripts in order from inside `file_handling/` (the read script needs the file written first):

```bash
cd file_handling
python write_files.py
python read_files.py
python copy_delete_files.py

cd ../directory_management
python create_list_dirs.py
python move_files.py

cd ../builtin_functions
python map_filter_reduce.py
python enumerate_zip_examples.py
```
