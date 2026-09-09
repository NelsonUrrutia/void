# Improvements

## Error handling
Instead of crashing the program, show an alert to indicate the issue.
For example, if a user adds an activity with the same name in the 
the same category - the app crashes. 
Also with the unique date of the void note when user tries to add
a note in the same day.

## Success messages
Add success alerts to the user when adding, updating data.


## Cross-view refresh via message bubbling

`NoteView` needs to know when `ActivitiesView` adds/updates/suspends an
activity or adds a category, since `TabbedContent` mounts every `TabPane`
up front — tab switching doesn't recompose the views, so `NoteView` won't
see the change on its own.

Currently solved with a direct call from `ActivitiesView` into
`NoteView` via `self.app.query_one(NoteView)`. That's fine for now, but
it couples `ActivitiesView` to `NoteView`'s existence.

If more views end up needing to react to activity/category changes,
switch to Textual's message bubbling instead: `ActivitiesView` posts a
message with no knowledge of who's listening, and it bubbles up to the
shared ancestor (`VoidApp`), which relays it to whichever views care.

```python
# activity.py
class DataChanged(Message):
    pass
...
def on_add_activity(self) -> None:
    ...
    self.post_message(self.DataChanged())
```

```python
# main.py
def on_activities_view_data_changed(self, message: ActivitiesView.DataChanged) -> None:
    self.query_one(NoteView).update_activities()
```

Trigger to implement: a second view (or more) needs the same refresh,
making the direct `query_one` calls multiply.
