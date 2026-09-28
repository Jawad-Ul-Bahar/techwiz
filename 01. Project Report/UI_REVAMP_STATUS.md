# AssureX UI revamp — first implementation

Date: 2026-09-26

## Second polish pass

- Reduced sidebar group spacing and brand padding; account/sign-out actions now share a compact bottom row.
- Added height-aware laptop menu density. All 13 admin navigation links fit without scrolling at 1366×768 and 1366×650.
- Concealed the sidebar scrollbar while preserving wheel, touch and keyboard scrolling on shorter screens. At 1024×600, keyboard focus reached the bottom links correctly.
- Softer active navigation, tighter topbar, consistent card/table padding and restrained shadows.
- Added explicit accessible names to icon-rail links and checked the mobile drawer at 390×844, with no settled horizontal page overflow.
- Rechecked all 18 page form contracts and 78 route/render cases; no backend changes.

## Completed

- Replaced the top link bar with a navy sidebar, collapsible icon rail and compact account topbar. Existing role visibility and route destinations are retained.
- Added mobile overlay navigation, Escape handling, focus cycling, active navigation and saved desktop sidebar preference.
- Applied a light canvas, white panels, restrained blue accent and readable status colours throughout all 18 page templates, including the shared shell.
- Moved embedded page styles into `static/css/dashboard.css`; added presentation behaviour in `static/js/dashboard.js`.
- Replaced remote icon-font assets with local SVG icons. Typography uses the system font stack; the UI no longer needs external font/icon requests.
- Restyled dashboard metrics, filters, tables, claim intake sections and upload controls, dossier model comparison, rules and reviewer actions.
- Updated shared presentation for products, registration, warranties/detail, alerts, document upload/OCR verification, repair lists/forms, reviewer queue, audit trail, analytics, policy editor and profile.
- Added claim-form section links, mobile table scrolling, associated form labels, focus outlines, skip link and reduced-motion support.
- Created separate branded login/registration layouts; styled errors, empty states and access-denied screen.
- Preserved existing form methods/actions, field names/values, validation attributes, backend code, models, policies and database contents.

There are 19 template files: one shared base and 18 page templates. Some pages receive their redesign through shared components rather than a full structural rewrite.

## Verified

- Existing suite: 18 passed, with 3 non-failing warnings, using an isolated in-memory database.
- 76 authenticated route/role checks plus login and registration. These include existing access-denied responses and the service role's expected 404 for a customer-owned document.
- Form-contract comparison against original sources passed for all 18 page templates.
- Browser checks: desktop layout, 390px mobile layout across 12 main screens, sidebar collapse persistence, drawer open/Escape close, table overflow containment and form labels.
- Preview data is synthetic and isolated. Preview does not validate real model inference or document OCR accuracy.

The installed Starlette test client required `httpx2`; this was installed only in the existing virtual environment, with its `httpcore2` and `truststore` dependencies. Project dependency manifests were not changed.

## Remaining / deliberately not included in this UI pass

- User review of the new visual direction and any specific page refinements.
- Advanced additions in the earlier plan: reviewer modal/action drawer, repair timeline view, document hash-copy control, evidence drag-and-drop/live previews and richer analytics charts.
- New filters or workflows beyond existing functionality; define these separately before changing business behaviour.
- PDF/Excel exports. The existing claim report endpoint returns Markdown, while the existing CSV export is preserved.
- Live health/model badge: omitted until its intended behaviour is agreed; no static “models online” claim is shown.
- Full live inference/OCR end-to-end verification. The environment reports TensorFlow missing; this is pre-existing and remains outside the UI changes.
- The existing `run_app.bat` ampersand message issue remains unchanged, outside UI scope.

## Review / recovery

Use the existing app launcher and refresh the browser to see the new UI.

Original template sources are saved in `scratch/ui_original_templates.json` because this checkout had no Git commits. It is a recovery reference, not an automatic rollback script.

Run isolated verification from the project root:

```powershell
.\.venv\Scripts\python.exe scratch\verify_ui.py
```

`scratch/verify_ui.py --serve` starts a test-only, GET-only preview on port 8011. It uses synthetic records and does not submit forms or operate on the project database; use the actual application for normal work.
