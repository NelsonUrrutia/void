# Edit & Deactivate Activities (modal + undo toast)

## Context
The Activities tab (`void/views/activities.py`) currently only supports creating and listing active activities — there's no edit or deactivate flow yet, even though the `activities` table already has an `is_active` flag (and a partial unique index on `(name, category_id) WHERE is_active = 1`) built for exactly this. The DB plumbing (`Connection.execute`) already supports UPDATE, it's just unused. This plan wires up editing and deactivating an activity through a modal dialog, per the user's choice: selecting a row opens an edit modal (Name input + Category select, prefilled), and that modal also offers a "Deactivate" action. Deactivating is immediate but shows an undo toast ("Deactivated 'X' — press U to undo") rather than a confirm step, matching the app's existing no-confirmation style (create has no confirm either) while still giving a safety net.

## Approach

### 1. Surface `id` through the read path
`Activity.get_active_activities()` (`void/models/activity.py`) and `ActivityController.get_activities()` (`void/controllers/activity.py`) currently return `(name, category)` tuples — no id. Extend the SELECT and the tuple shape to `(id, name, category)`.

### 2. New model methods — `void/models/activity.py`
Add alongside the existing `create_activity`:
- `update_activity(self, activity_id, name, category_id)` — `UPDATE activities SET name = ?, category_id = ? WHERE id = ?` via `self.conn.execute(...)`.
- `set_active(self, activity_id, is_active: bool)` — `UPDATE activities SET is_active = ? WHERE id = ?`. Used for both deactivate (`False`) and undo/reactivate (`True`) — one method, not two, since it's the same statement.

Both should catch `sqlite3.IntegrityError` (the partial unique index) the same way `create_activity` presumably already does, and let it propagate/be handled the same way so the view can `notify(..., severity="error")` consistently.

### 3. Controller — `void/controllers/activity.py`
Add thin passthroughs: `update_activity(self, activity_id, name, category_id)` and `set_activity_active(self, activity_id, is_active)`.

### 4. Row keys in the table — `void/views/activities.py`
In `init_table()` / `update_activities()`, when calling `table.add_row(name, category)`, pass `key=str(id)` (id no longer displayed, just used as the row key). This lets `DataTable.RowSelected` tell us which activity id was picked without a separate id-mapping dict.

### 5. Edit modal — new `void/views/modals.py`
`EditActivityModal(ModalScreen)`, constructed with the selected activity's `(id, name, category_id)` and the category options (reuse whatever call currently populates `#category_select` in the create flow). Layout: `Input` prefilled with name, `Select` prefilled with category, three buttons: `Save`, `Deactivate`, `Cancel`. Same inline-validation style as the existing create flow (`self.notify(..., severity="error")` for empty name / missing category, no separate dialog for that). On Save/Deactivate/Cancel, `self.dismiss(result)` where `result` is `None` (cancel) or a small dict/tuple describing the action taken.

### 6. Wire it up in `ActivitiesView` — `void/views/activities.py`
- `@on(DataTable.RowSelected, "#activities_table")` handler: look up the row's id (from the event's row key) and current name/category, then `self.app.push_screen(EditActivityModal(...), self.on_edit_dismissed)`.
- `on_edit_dismissed(self, result)`:
  - `save` → `ctrl.update_activity(id, name, category_id)`, `update_activities()`.
  - `deactivate` → `ctrl.set_activity_active(id, False)`, store `self._last_deactivated = (id, name)`, `self.notify(f'Deactivated "{name}" — press U to undo', severity="warning")`, `update_activities()`.
  - `None`/cancel → no-op.
- Add `BINDINGS = [("u", "undo_deactivate", "Undo")]` (or an `on_key` check) on `ActivitiesView`; `action_undo_deactivate` — if `self._last_deactivated` is set, `ctrl.set_activity_active(id, True)`, clear it, `update_activities()`, `self.notify(f'Restored "{name}"')`. No timeout tracking needed — pressing U when there's nothing to undo is just a no-op.

## Files touched
- `void/models/activity.py` — `update_activity`, `set_active`; extend `get_active_activities` to include `id`.
- `void/controllers/activity.py` — `update_activity`, `set_activity_active`; extend `get_activities` return shape.
- `void/views/activities.py` — row keys on `add_row`, `RowSelected` handler, modal dismiss handler, undo binding.
- `void/views/modals.py` (new) — `EditActivityModal`.

## Verification
- Extend the existing unittest module for the activity model (`void/tests/models/test_activity.py`, run via `python -m unittest void.tests.models.test_activity -v`) with cases for `update_activity` and `set_active`, including the partial-unique-index conflict case (renaming/reactivating into a name collision with an active row should raise, matching `create_activity`'s existing behavior).
- Run the app (`void`), go to the Activities tab, and manually check: select a row → modal opens prefilled → Save updates the table; select a row → Deactivate removes it from the list and shows the toast; press `u` → row reappears; try renaming into a colliding active name → inline error, consistent with create's validation.
