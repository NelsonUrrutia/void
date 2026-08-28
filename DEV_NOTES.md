# Dev notes
Install (just once)
- `pip install -e .`

Run the project
- `void`
- `python -m void.main`
- `python void/main.py`

Debugging
1. Terminal 1 `textual console`
2. Terminal 2 `textual run --dev  void/main.py`

How to run unittest 
`python -m unittest void.tests.models.test_activity -v`

How to run specific functions
`python -c "from void.controllers.activity import ActivityController; ActivityController().get_activities()`

How to use breakpoint()
- p <expr> — print any variable/expression (e.g. p result, p result[0]["name"])
- n — run the next line
- s — step into a function call
- c — continue running until the next breakpoint (or the program ends)
- l — show the source code around where you're stopped
- q — quit the debugger entirely
