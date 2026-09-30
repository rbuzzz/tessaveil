# Tessaveil Windows v1 Figma handoff

## Disposition

**BLOCKED — exact production-font validation only.** Live Figma inspection now
confirms complete Windows v1 coverage: foundations, scoped variables, reusable
components, implemented settings, sheet lifecycle dialogs, every stable
controller error, security states, RU/EN copy, scaling, and accessibility.

The only Figma handoff blocker is that the connected plan exposes neither
Segoe UI nor Consolas. The editable preview is explicitly labelled as Inter and
Roboto Mono. This handoff blocker is not a product-code or release defect and
does not relax any independent Windows, equipment, filesystem, signing, or
format-freeze gate.

## Identity and authorization scope

- Authenticated Figma identity: **Ivan**.
- Authorized plan scope: the sole returned **Pro** plan.
- Authorized file: [Tessaveil — Product Design](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq), file key `VCQcLCScpQja1WVXjWYROq`.
- Authorized page: `0:1`, `Tessaveil Windows v1 Handoff`.
- Initial inspection found one empty page and no existing product screens.
- Repository Code Connect search found no mappings; Code Connect is not
  applicable to this handoff.
- Library discovery preceded design-system search. Available Material 3 and
  Simple Design System assets did not match the native Qt/Windows model, so the
  file uses a local code-aligned Tessaveil system.

The separately visible `Classic Create Concepts` file with key
`JRmYeYALLwsII1wjFxoFRV` is unrelated Renderis evidence. It was never treated as
authorization, mutated, or used as a Tessaveil node target.

## Foundations, scopes, and reusable components

- [Foundations](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=3-59) contain source-aligned Light/Dark colors,
  semantic aliases, layout variables, typography, and font-status annotations.
- [Original local components](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=4-2) contain buttons, fields, badge, security note,
  table cell, dialog shell, and privacy cover.
- [Extended local components](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=13-85) add `App/Header`, `Tab/Navigation`,
  `Profile/Card`, `Sheet/Protection`, and `Error/Card`.
- Every one of the 16 components has at least one live instance. `Dialog/Shell`
  has four instances, including the three sheet lifecycle dialogs;
  `Error/Card` has nineteen instances, one per stable controller error key.
- All text-bearing new components expose editable text properties.

All 47 variables have explicit picker scopes:

- 23 primitives: `[]`, hidden from property pickers;
- background semantics: `FRAME_FILL`, `SHAPE_FILL`;
- text semantics: `TEXT_FILL`;
- border/focus semantics: `STROKE_COLOR`;
- accent/error semantics: only their used fill, text, and stroke scopes;
- spacing: `GAP`; radii: `CORNER_RADIUS`; dimensions: `WIDTH_HEIGHT`.

No Tessaveil variable retains `ALL_SCOPES`.

## Screen and state coverage

All fifteen screen boards are exactly 1280 × 720.

| Board | Node | Covered states |
|---|---|---|
| Start | [5:2](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=5-2) | start, create/open vault, unlock, secret-field accessibility, duplicate-version warning |
| Workspace | [5:36](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=5-36) | profile search, exact product/platform/version/mode, unavailable guidance |
| Dictionaries | [5:65](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=5-65) | add, replace, rename, delete, snapshot and re-verification rules |
| Sheet | [5:103](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=5-103) | 10/36, edit, protection, verify, neutral cells |
| Spin | [5:144](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=5-144) | same outward flow, no validity signal, repeat-observation warning |
| Recovery | [6:54](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=6-54) | backup, restore, original password, filesystem caveat |
| Rotation | [6:79](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=6-79) | password rotation and old-copy warning |
| Dirty state | [6:90](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=6-90) | Save, Discard, Cancel, keyboard order |
| Privacy | [6:108](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=6-108) | privacy cover and locked-state boundary |
| Error summary | [6:125](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=6-125) | wrong password/damaged, access denied, oversize, failed save |
| Accessibility | [6:153](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=6-153) | 100/150/200%, focus, UI Automation, neutral cells |
| Sheet lifecycle | [14:87](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=14-87) | create, rename, delete with real `Dialog/Shell` instances |
| Settings | [14:129](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=14-129) | locale EN/RU, theme System/Light/Dark, timeout 1/5/15/30 |
| Controller errors 1–4 | [15:119](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-119) | header/version/KDF errors |
| Controller errors 5–8 | [15:143](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-143) | truncation/size/authentication/password errors |
| Controller errors 9–12 | [15:167](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-167) | policy/state/space/I/O errors |
| Controller errors 13–16 | [15:191](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-191) | destination/path/filesystem/lock errors |
| Controller errors 17–19 | [15:215](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-215) | unsaved/payload/temporary-file errors |

The create, rename, and delete states are individually linked at nodes
`14:105`, `14:113`, and `14:121`. Locale, theme, and timeout are individually
linked at `14:137`, `14:145`, and `14:153`.

## Stable controller error inventory

Each node is an editable `Error/Card` instance containing the exact stable key,
the source EN/RU message, and concrete localized user-action guidance.

| Stable key | Exact node |
|---|---|
| `invalid-header` | [15:126](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-126) |
| `unsupported-version` | [15:130](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-130) |
| `kdf-out-of-bounds` | [15:134](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-134) |
| `unsupported-kdf` | [15:138](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-138) |
| `truncated` | [15:150](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-150) |
| `too-large` | [15:154](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-154) |
| `authentication` | [15:158](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-158) |
| `invalid-password` | [15:162](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-162) |
| `password-policy` | [15:174](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-174) |
| `access-denied` | [15:178](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-178) |
| `insufficient-space` | [15:182](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-182) |
| `io` | [15:186](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-186) |
| `already-exists` | [15:198](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-198) |
| `invalid-path` | [15:202](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-202) |
| `unsupported-filesystem` | [15:206](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-206) |
| `locked` | [15:210](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-210) |
| `unsaved-changes` | [15:222](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-222) |
| `invalid-payload` | [15:226](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-226) |
| `temporary-remains` | [15:230](https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-230) |

## Security and accessibility review

- Spin exposes no explicit validity signal, success flag, target marker, or
  saved target metadata.
- Twelve neutral table cells share one component and identical `198 × 40`
  geometry; none has a “real word” annotation.
- Secret-field annotations allow role, name, focus, required/error, disabled,
  and modal state, while excluding secret characters, seed words, target
  columns, clipboard payloads, and hidden metadata from UI Automation.
- Dirty-state and delete dialogs identify destructive choices in text and map
  Escape to the non-destructive choice.
- Privacy cover contains no vault name, profile, recovery word, or secret.
- Scaling notes cover 100%, 150%, and 200%, including reflow and focus order.
- All examples are synthetic; there are no real credentials, recovery phrases,
  payloads, local paths, or secrets.

## Visual and structural audit

Live plugin inspection and native 1280 × 720 screenshots covered Sheet/Spin,
the sheet lifecycle, and controller error boards. The first Sheet/Spin render
found selector overlap; nodes `5:110`, `5:113`, and `5:144` were corrected.
The lifecycle render found a clipped workspace card; node `14:93` and state
positions `14:105`, `14:113`, and `14:121` were corrected. Header text alignment
was corrected in reusable component nodes `13:88`–`13:90`, then the error board
was rendered again.

The final live structural audit recorded:

- 15 screen boards, all `1280 × 720`;
- 16 described local components and 108 component instances;
- 361 editable text nodes and 0 image-fill nodes;
- every descendant inside its screen bounds;
- 19/19 unique stable error keys and nodes;
- 47 scoped variables, 0 `ALL_SCOPES`, 23 hidden primitives;
- Inter/Roboto Mono preview typography only; Segoe UI/Consolas unavailable.

## Font blocker and clearance action

The implementation uses Segoe UI for native UI and Consolas for table cells.
Figma font discovery still returns neither family. The preview therefore uses
Inter and Roboto Mono and must not be described as an exact-font pass.

To clear the handoff gate, the owner or design team must either make Segoe UI
and Consolas available to the Figma plan, or explicitly approve the documented
Inter/Roboto Mono substitution. Then rerun font discovery and rendered
typography validation, change the machine contract to `pass`, and remove the
blocker. No code or release-status change is implied.

## Machine-readable gate contract

```json
{
  "schema_version": 2,
  "disposition": "blocked",
  "authorized_target": {
    "name": "Tessaveil — Product Design",
    "file_key": "VCQcLCScpQja1WVXjWYROq",
    "url": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq",
    "page_node_id": "0:1"
  },
  "excluded_evidence": [
    {
      "name": "Classic Create Concepts",
      "file_key": "JRmYeYALLwsII1wjFxoFRV",
      "reason": "unrelated Renderis file; not an authorized Tessaveil target"
    }
  ],
  "coverage": {
    "foundations_and_components": true,
    "start_create_open_unlock": true,
    "profile_search_exact_status_unavailable": true,
    "custom_dictionary_lifecycle": true,
    "sheet_10_36_protection_verify": true,
    "spin_and_repeat_warning": true,
    "backup_restore_original_password": true,
    "rotation_and_old_copy_warning": true,
    "dirty_save_discard_cancel": true,
    "privacy_cover_and_locked": true,
    "wrong_password_damaged_access_denied_oversize": true,
    "scaling_and_accessibility": true,
    "sheet_create_rename_delete": true,
    "settings_locale_theme_timeout": true,
    "stable_actionable_controller_errors": true
  },
  "node_links": {
    "foundations": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=3-59",
    "components": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=13-85",
    "screens": {
      "start_create_open_unlock": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=5-2",
      "profile_search_exact_status_unavailable": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=5-36",
      "custom_dictionary_lifecycle": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=5-65",
      "sheet_10_36_protection_verify": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=5-103",
      "spin_and_repeat_warning": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=5-144",
      "backup_restore_original_password": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=6-54",
      "rotation_and_old_copy_warning": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=6-79",
      "dirty_save_discard_cancel": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=6-90",
      "privacy_cover_and_locked": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=6-108",
      "wrong_password_damaged_access_denied_oversize": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=6-125",
      "scaling_and_accessibility": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=6-153",
      "sheet_create_rename_delete": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=14-87",
      "settings_locale_theme_timeout": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=14-129",
      "stable_actionable_controller_errors": "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=15-119"
    }
  },
  "component_nodes": {
    "App/Header": "13:87",
    "Tab/Navigation": "13:91",
    "Profile/Card": "13:93",
    "Sheet/Protection": "13:98",
    "Error/Card": "13:102",
    "Button/Primary": "4:5",
    "Button/Secondary": "4:7",
    "Button/Danger": "4:9",
    "Field/Text": "4:11",
    "Field/Secret": "4:14",
    "Field/Select": "4:17",
    "Badge/Status": "4:20",
    "Note/Security": "4:22",
    "Table/Cell": "4:25",
    "Dialog/Shell": "4:27",
    "Privacy/Cover": "4:30"
  },
  "state_nodes": {
    "sheet_create": "14:105",
    "sheet_rename": "14:113",
    "sheet_delete": "14:121",
    "settings_locale": "14:137",
    "settings_theme": "14:145",
    "settings_timeout": "14:153"
  },
  "error_nodes": {
    "invalid-header": "15:126",
    "unsupported-version": "15:130",
    "kdf-out-of-bounds": "15:134",
    "unsupported-kdf": "15:138",
    "truncated": "15:150",
    "too-large": "15:154",
    "authentication": "15:158",
    "invalid-password": "15:162",
    "password-policy": "15:174",
    "access-denied": "15:178",
    "insufficient-space": "15:182",
    "io": "15:186",
    "already-exists": "15:198",
    "invalid-path": "15:202",
    "unsupported-filesystem": "15:206",
    "locked": "15:210",
    "unsaved-changes": "15:222",
    "invalid-payload": "15:226",
    "temporary-remains": "15:230"
  },
  "audit": {
    "screen_count": 15,
    "screen_size": "1280x720",
    "component_count": 16,
    "instance_count": 108,
    "text_node_count": 361,
    "image_fill_count": 0,
    "all_nodes_within_screen_bounds": true,
    "stable_error_key_count": 19,
    "neutral_table_cell_count": 12,
    "neutral_table_cell_geometry": "198x40",
    "variable_count": 47,
    "all_scopes_count": 0,
    "primitive_hidden_count": 23,
    "component_instance_use": {
      "App/Header": 7,
      "Tab/Navigation": 4,
      "Profile/Card": 1,
      "Sheet/Protection": 1,
      "Error/Card": 19,
      "Button/Primary": 14,
      "Button/Secondary": 14,
      "Button/Danger": 3,
      "Field/Text": 5,
      "Field/Secret": 6,
      "Field/Select": 4,
      "Badge/Status": 9,
      "Note/Security": 4,
      "Table/Cell": 12,
      "Dialog/Shell": 4,
      "Privacy/Cover": 1
    }
  },
  "font_validation": {
    "production": ["Segoe UI", "Consolas"],
    "preview": ["Inter", "Roboto Mono"],
    "status": "blocked"
  },
  "blocker": {
    "category": "exact-production-fonts-unavailable",
    "reason": "Figma font discovery returned neither Segoe UI nor Consolas, so exact production typography cannot be validated.",
    "owner_action": "Make Segoe UI and Consolas available in the Figma plan or explicitly approve the documented Inter and Roboto Mono substitute.",
    "rerun": "Repeat font discovery and rendered typography validation, then change disposition and font status to pass only if the selected path is verified."
  },
  "impact": {
    "code": "unaffected",
    "release": "unaffected",
    "handoff_gate": "blocked"
  }
}
```
