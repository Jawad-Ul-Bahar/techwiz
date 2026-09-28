# AssureX Claim Engine — Manual Test Guide

> **Who is this for?** A non-technical tester clicking through the live app in Chrome.
> **What is it?** A step-by-step checklist of every feature that is actually built and working right now.
> Features that do **not exist yet** in the code are clearly marked **NOT YET AVAILABLE** — do not look for them; the app is not broken, they are just not built.

---

## 1. SETUP — Starting the App

### Step 1 — Start the server

Double-click the file **`run_app.bat`** in the project root folder.
A black terminal window will open. Wait until you see this line printed:

`[startup] All models ready — total X.XXs`

> WARNING: The first startup can take **30–90 seconds** because the AI models load in the background. The browser may open automatically. If it does, wait on the login page until the terminal shows ''All models ready'' before submitting any claim.

### Step 2 — Open Chrome

Navigate to: **`http://127.0.0.1:8000`**

If the server is not ready yet, Chrome will show ''This site can not be reached''. Wait 10 more seconds and refresh.

### Step 3 — Login Credentials

These four accounts are pre-seeded in the database automatically when the app first starts.

| Role | Email | Password | What this role can do |
|---|---|---|---|
| **Customer** | customer@assurex.com | customer123 | Submit claims, view their own claim dossiers |
| **Service Center** | service@assurex.com | service123 | Submit claims on behalf of customers |
| **Reviewer** | reviewer@assurex.com | reviewer123 | See Review Queue, approve/reject flagged claims |
| **Admin** | admin@assurex.com | admin123 | Everything above + Analytics dashboard |

**Which account to use for each section:**
- Sections A, B, C, D, E, F (Login, Claim submission, rules) → use **Customer**
- Section G (Reviewer Queue, Override) → use **Reviewer**
- Section H (Analytics, Admin View) → use **Admin**

---

## 2. STEP-BY-STEP TEST CHECKLIST

---

### SECTION A — Login / Logout / Registration / Role Access

**A1 — Login page loads**
- [ ] Go to `http://127.0.0.1:8000/login`
- **What you should see:** A dark-themed page titled ''AssureX Claim Engine'' with Email and Password fields and a Sign In button.
- **If broken:** Page is white/blank, or Chrome says ''Connection refused''.

**A2 — Login with wrong password**
- [ ] On login page: Email = `customer@assurex.com`, Password = `wrongpass`, click **Sign In**
- **What you should see:** Same page reloads with error: *''Invalid email or password. Please try again.''*
- **If broken:** You get logged in anyway, or a 500 error.

**A3 — Login as Customer**
- [ ] Email: `customer@assurex.com`, Password: `customer123`, click **Sign In**
- **What you should see:** Land on Claims Dashboard at `http://127.0.0.1:8000/`. Top nav shows: **Dashboard**, **New Claim**, name ''John Customer'' with a red ''customer'' badge, and **Logout** button. Four metric tiles: Total Claims, Likely Valid, Likely Invalid, Manual Review.
- **If broken:** 500 error, or you stay on the login page.

**A4 — Customer cannot access Reviewer Queue (403 test)**
- [ ] While logged in as Customer, go to `http://127.0.0.1:8000/reviewer/queue`
- **What you should see:** Dark page with heading **''403 — Access Denied''** and text *''Role '''customer'' is not authorized to access this route.''*
- **If broken:** You can see the reviewer queue.

**A5 — Customer cannot access Admin Analytics (403 test)**
- [ ] While logged in as Customer, go to `http://127.0.0.1:8000/admin/analytics`
- **What you should see:** Same **403 Access Denied** page.
- **If broken:** You can see the analytics page.

**A6 — Register a new account**
- [ ] Go to `http://127.0.0.1:8000/register`
- [ ] Full Name = `Test Tester`, Email = `tester@test.com`, Password = `test1234`, Role = `customer`
- [ ] Click **Register**
- **What you should see:** Automatically logged in and redirected to Dashboard as ''Test Tester''.
- **If broken:** Error page, or form reloads without a message.

**A7 — Cannot register with duplicate email**
- [ ] Logout, go to /register, try registering again with `tester@test.com`
- **What you should see:** Error: *''Email address '''tester@test.com'' is already registered.''*
- **If broken:** A second account is created, or 500 error.

**A8 — Logout**
- [ ] Click the **Logout** button in the top nav bar
- **What you should see:** Redirected to `http://127.0.0.1:8000/login`. Your name no longer appears in the nav.
- **If broken:** Clicking Logout does nothing.

---

### SECTION B — Claim Submission (Normal / Likely Valid Claim)

> Log in as **Customer** (customer@assurex.com / customer123). Make sure terminal shows ''All models ready''.

**B1 — Claim form loads**
- [ ] Click **New Claim** in the nav bar, or the blue **Submit Claim** button on the dashboard
- **What you should see:** URL = `http://127.0.0.1:8000/claims/new`. Form with 3 sections: ''1. Product and Purchase Information'', ''2. Fault Incident Details'', ''3. Attach Proof of Purchase''.
- **If broken:** 403 error, or blank page.

**B2 — Submit a Likely Valid claim (copy these values exactly)**

| Field | Value to type |
|---|---|
| Product Name | Samsung Galaxy S24 Ultra |
| Category | Electronics |
| Brand | Samsung |
| Model Number | SM-S928B |
| Serial Number | SN-TEST-001 |
| Purchase Date | 2025-03-01 |
| Purchase Price | 1199.99 |
| Retailer | Amazon |
| Fault Category | Motherboard / Board Failure |
| Damage / Exclusions | None (Standard Defect) |
| Fault Occurrence Date | 2026-01-15 |
| Previous Repair Count | 0 |
| Description | Device stopped powering on after normal use. |
| Receipt Upload | leave blank |

- [ ] Click **Submit Claim**
- **What you should see:** After 1-5 seconds, redirected to Dossier page at a URL like `http://127.0.0.1:8000/claims/view/CLM-2026-0001`. A green badge reading **''Likely Valid''** in the top right.
- **If broken:** 503 error (models still loading), 500 error, or nothing happens.

**B3 — Claim Summary Card image is displayed**
- [ ] On the Dossier page, look at the right panel titled **''Claim Summary Card''**
- **What you should see:** A visual card image — a coloured rectangle with claim data printed on it (serial number, dates, fault category). This is what the Vision AI model analysed.
- **If broken:** Broken image icon (grey square with X), or empty panel.

**B4 — Dual AI model predictions and confidence scores**
- [ ] On the Dossier page, look at the left panel titled **''Dual-Model Evaluation''**
- **What you should see:**
  - Left column ''Tabular ML Model'': Predicted class in blue text (e.g. ''Valid Claim''), confidence % (e.g. ''Conf: 87.3%''), three coloured progress bars for Valid / Invalid / Review.
  - Right column ''Vision Summary Model'': Same layout in purple text.
  - Top of panel: Consistency Status (e.g. ''Strong Match'') and a Gap decimal number.
- **If broken:** Both columns show ''None'' or 0%, or panel is missing.

**B5 — Warranty Rule Results panel**
- [ ] Scroll down to panel **''Warranty Policy and Decision Analysis''**
- **What you should see (for this valid claim):** Green checkmarks for: ''Warranty Coverage Active'', ''Damage Type Eligible'', ''No Unauthorized Repair History'', ''Fault Reported Within Allowable Period'', ''Serial Number Match Verified''. No red X items.
- **If broken:** Rule list is blank, or all rules show as failed.

**B6 — Decision Rationale**
- [ ] In the same panel, look at the **''Decision Rationale''** box on the right
- **What you should see:** ''Supporting Factors:'' section with bullet points (e.g. ''Python ML model and Vision Classifier both predict Valid Claim with strong confidence.''). ''Opposing Factors:'' section showing ''None.''
- **If broken:** Both sections blank, or box missing.

**B7 — Reviewer Override panel is visible**
- [ ] Scroll to bottom panel: **''Reviewer Action and Override''**
- **What you should see:** A text box ''Reviewer Comments'' and two buttons: green **Approve** and red **Reject**.
- **If broken:** Panel is missing entirely.

**B8 — Dashboard updates after submission**
- [ ] Click **Dashboard** in the top nav
- **What you should see:** ''Total Claims'' tile shows at least 1. The claim appears in the ''Recent Claim Submissions'' table with columns: Claim ID (blue link), Fault Category, Python ML Result, Vision Model Result, Consistency, Final Decision badge, View button.
- **If broken:** Dashboard still shows 0, or claim missing from table.

---

### SECTION C — Hard-Fail Claim (Likely Invalid — Expired Warranty)

**C1 — Submit a claim with an expired warranty**

| Field | Value |
|---|---|
| Product Name | LG Refrigerator WM3500 |
| Category | Appliances |
| Brand | LG |
| Model Number | WM3500CW |
| Serial Number | SN-EXPIRED-999 |
| Purchase Date | 2021-01-01 |
| Purchase Price | 750.00 |
| Retailer | Best Buy |
| Fault Category | Compressor Failure |
| Damage / Exclusions | None (Standard Defect) |
| Fault Occurrence Date | 2026-09-01 |
| Previous Repair Count | 0 |
| Description | Compressor stopped working. |

- [ ] Click **Submit Claim**
- **What you should see:** Red **''Likely Invalid''** badge. Red X rule: **''Warranty Expired: Claim submitted X days post-coverage.''** Opposing Factors explain the reason.
- **If broken:** Claim returns as ''Likely Valid'' despite 5+ year old product with 24-month warranty.

**C2 — Submit a claim with excluded damage (liquid spill)**

| Field | Value |
|---|---|
| Product Name | Dell XPS 15 Laptop |
| Brand | Dell |
| Model Number | XPS-9530 |
| Serial Number | SN-LIQUID-001 |
| Purchase Date | 2025-06-01 |
| Fault Category | Motherboard / Board Failure |
| Damage / Exclusions | **Liquid Damage (Excluded)** |
| Fault Occurrence Date | 2026-08-01 |

- [ ] Click **Submit Claim**
- **What you should see:** Red **''Likely Invalid''** badge. Red X rule: *''Excluded Damage Type: '''liquid_spill_damage'' is excluded from coverage.''*
- **If broken:** Claim passes as valid despite selecting a liquid damage exclusion.

---

### SECTION D — Contradiction Detection (Impossible Date)

**D1 — Submit a claim where fault date is BEFORE purchase date**

| Field | Value |
|---|---|
| Product Name | Sony Bravia KD-65 |
| Brand | Sony |
| Model Number | KD-65X95L |
| Serial Number | SN-CONTRA-001 |
| Purchase Date | 2025-08-01 |
| Fault Occurrence Date | **2025-05-15** (3 months BEFORE purchase) |
| Fault Category | Screen Flicker / Display Fault |
| Damage / Exclusions | None (Standard Defect) |

- [ ] Click **Submit Claim**
- **What you should see:** Yellow **''Manual Review Required''** badge. Opposing Factors: **''Contradiction: Fault Date (2025-05-15) is prior to Purchase Date (2025-08-01).''**
- **If broken:** Contradiction not detected, claim passes normally, or 500 error.

---

### SECTION E — Missing Document Detection

> The form accepts the receipt upload as optional. Missing receipt may or may not trigger ''Manual Review'' depending on the category policy file. This is expected.

**E1 — Submit without uploading a receipt**
- [ ] Click **New Claim**, fill any valid details (use B2 values but Serial Number = `SN-NODOC-001`), but **do not upload any file**
- [ ] Click **Submit Claim**
- **What you should see:** The dossier loads. Check the Rules panel for any yellow warning about missing documentation. Final decision may vary by category policy.
- **If broken:** Form refuses to submit when no file is attached (file is optional in code).

---

### SECTION F — Duplicate Claim Detection (Same Receipt File Twice)

**F1 — Submit the same receipt file twice**
- [ ] Find any small file on your computer (a screenshot, small image, or PDF)
- [ ] Submit a new claim with Serial = `SN-DUP-001`, upload that file as the receipt. Note the Claim ID shown.
- [ ] Click **New Claim** again. Use Serial = `SN-DUP-002` (different), but upload the **exact same file** again.
- [ ] Click **Submit Claim**
- **What you should see on the second dossier:** Yellow **''Manual Review Required''** badge. Opposing Factors: **''Duplicate Document: Identical receipt hash matches previous Claim CLM-2026-XXXX.''**
- **If broken:** Second claim approved as ''Likely Valid'' with no duplicate warning.

---

### SECTION G — Reviewer Queue and Override

> Log in as **Reviewer** (reviewer@assurex.com / reviewer123)

**G1 — Access the Review Queue**
- [ ] Click **Review Queue** in the nav bar, or go to `http://127.0.0.1:8000/reviewer/queue`
- **What you should see:** Page titled ''Manual Review Queue''. A table with columns: Claim ID (link), Product ID, Python ML Class + confidence, Vision Model Class, Consistency badge, blue ''Review Dossier'' button. If the queue is empty, it shows ''Queue is clear. No claims require manual review.''
- **If broken:** 403 error (wrong login role), or queue never shows claims you submitted.

**G2 — Override a claim (Approve)**
- [ ] Click **Review Dossier** on any queue item
- [ ] In the ''Reviewer Action and Override'' panel, type: `Verified documents. Claim is legitimate.`
- [ ] Click green **Approve** button
- **What you should see:** Dossier reloads with a notice at top of panel: **''Overridden by Sarah Adjudicator (Reviewer)''** and your comment below it.
- **If broken:** 403 error on Approve, or page does not reload.

**G3 — Override a claim (Reject)**
- [ ] Go back to /reviewer/queue, pick another ''Manual Review'' claim
- [ ] Type: `Warranty period was expired on inspection. Rejecting.`
- [ ] Click red **Reject** button
- **What you should see:** Dossier shows ''Overridden'' note with your rejection comment.
- **If broken:** Same as G2.

---

### SECTION H — Admin Analytics Dashboard

> Log in as **Admin** (admin@assurex.com / admin123)

**H1 — Access Analytics**
- [ ] Click **Analytics** in the nav bar, or go to `http://127.0.0.1:8000/admin/analytics`
- **What you should see:** Page titled ''System Analytics and Reporting''. Four metric tiles: Total Evaluated, Valid Ratio %, Invalid Ratio %, Disagreement Rate %. Below: ''Full Claims Audit Log'' table with every claim, columns: Claim ID, Submission Date, Python ML Class, Vision Model Class, Conf Diff, Final Decision badge, Status.
- **If broken:** 403 error (not logged in as admin), or all metrics show 0 after submitting claims.

**H2 — Admin can access Review Queue**
- [ ] While logged in as Admin, click **Review Queue**
- **What you should see:** Same reviewer queue page that the Reviewer role sees. Admin has full access.
- **If broken:** Admin gets a 403 on the Review Queue.

**H3 — Admin can submit claims**
- [ ] While logged in as Admin, click **New Claim**
- **What you should see:** Claim intake form loads normally. Admins can submit claims.
- **If broken:** Admin gets a 403 on New Claim.

---

### SECTION I — Health Check

**I1 — API health check endpoint**
- [ ] Go to `http://127.0.0.1:8000/health`
- **What you should see:** JSON response: `{ status: ok, models_ready: true}`. If visited right after startup, models_ready may be `false` — wait 30-60 seconds and refresh.
- **If broken:** 404 or 500 error.

---

## 3. KNOWN GAPS — Features NOT YET BUILT

These are absent from the code. Do not look for them. Their absence is not a bug.

| # | Feature | Verified Status |
|---|---|---|
| 1 | PDF Report Download | NOT YET AVAILABLE — no /claims/report/ route or export button exists |
| 2 | CSV Export | NOT YET AVAILABLE — no CSV download route in app.py, no button on analytics page |
| 3 | Search / Filter claims | NOT YET AVAILABLE — no search box or filter controls on any table |
| 4 | Separate Product Registration page | NOT YET AVAILABLE — products are auto-created during claim submit |
| 5 | Warranty Info / Products page | NOT YET AVAILABLE — no /products/ or /warranty/ route |
| 6 | OCR side-by-side review page | NOT YET AVAILABLE — OCR runs silently during submit, no separate review step |
| 7 | Customer profile / My Account page | NOT YET AVAILABLE — no /profile route |
| 8 | Notifications / Email alerts | NOT YET AVAILABLE — no notification system exists |
| 9 | Multi-entry repair history | NOT YET AVAILABLE — only a single number field for repair count |
| 10 | Model version tracking page | NOT YET AVAILABLE — no /model/version or model info route |
| 11 | Audit log history view | NOT YET AVAILABLE — audit log is written to DB but no page displays it |
| 12 | Customer notification feed | NOT YET AVAILABLE — no in-app notification bell |
| 13 | Warranty duration input field on form | NOT YET AVAILABLE — defaults to 24 months, not changeable in the form UI |
| 14 | Save Draft / Claim draft mode | NOT YET AVAILABLE — submitting always runs full AI pipeline immediately |

---

## 4. SUGGESTED TEST SCENARIOS — Ready-Made Copy-Paste Values

---

### Scenario 1 — Likely Valid

| Field | Value |
|---|---|
| Product Name | Bosch Dishwasher SMS46GI05I |
| Category | Appliances |
| Brand | Bosch |
| Model Number | SMS46GI05I |
| Serial Number | SN-VALID-2025-A |
| Purchase Date | 2025-07-01 |
| Purchase Price | 680.00 |
| Retailer | Carrefour |
| Fault Category | Compressor Failure |
| Damage / Exclusions | None (Standard Defect) |
| Fault Occurrence Date | 2026-04-10 |
| Previous Repair Count | 0 |
| Description | Dishwasher motor stopped mid-cycle. No user damage. |

Expected: Green **Likely Valid** badge. All rules show green checkmarks.

---

### Scenario 2 — Likely Invalid (Expired Warranty)

| Field | Value |
|---|---|
| Product Name | Kenwood Food Processor FP980 |
| Category | Appliances |
| Brand | Kenwood |
| Model Number | FP980 |
| Serial Number | SN-EXPIRED-2019-B |
| Purchase Date | 2019-03-15 |
| Purchase Price | 350.00 |
| Retailer | Jumbo |
| Fault Category | Motherboard / Board Failure |
| Damage / Exclusions | None (Standard Defect) |
| Fault Occurrence Date | 2026-09-01 |
| Previous Repair Count | 0 |
| Description | Device no longer powers on. |

Expected: Red **Likely Invalid** badge. Rule: ''Warranty Expired: Claim submitted X days post-coverage.''

---

### Scenario 3 — Manual Review (No Receipt Uploaded)

| Field | Value |
|---|---|
| Product Name | Philips OLED 65PUS8808 |
| Category | Electronics |
| Brand | Philips |
| Model Number | 65PUS8808 |
| Serial Number | SN-NODOC-2025-C |
| Purchase Date | 2025-05-20 |
| Purchase Price | 950.00 |
| Retailer | Noon |
| Fault Category | Screen Flicker / Display Fault |
| Damage / Exclusions | None (Standard Defect) |
| Fault Occurrence Date | 2026-07-01 |
| Previous Repair Count | 0 |
| Receipt | **Leave blank — do not upload** |
| Description | Screen has intermittent flickering lines. |

Expected: Yellow **Manual Review Required** badge (or Likely Valid if Electronics policy does not hard-require receipt). Check rules panel for warnings.

---

### Scenario 4 — Manual Review (Contradiction: Fault Before Purchase)

| Field | Value |
|---|---|
| Product Name | Apple MacBook Air M3 |
| Category | Electronics |
| Brand | Apple |
| Model Number | MacBook-Air-M3-13 |
| Serial Number | SN-CONTRA-2025-D |
| Purchase Date | 2025-09-01 |
| Purchase Price | 1299.00 |
| Retailer | Apple Store |
| Fault Category | Battery / Power Failure |
| Damage / Exclusions | None (Standard Defect) |
| Fault Occurrence Date | **2025-06-01** (3 months before purchase) |
| Previous Repair Count | 0 |
| Description | Battery does not hold charge. |

Expected: Yellow **Manual Review Required**. Opposing Factors: ''Contradiction: Fault Date (2025-06-01) is prior to Purchase Date (2025-09-01).''

---

### Scenario 5 — Duplicate Claim (Same File Uploaded Twice)

First submission:

| Field | Value |
|---|---|
| Product Name | Samsung Washing Machine WW70T |
| Brand | Samsung |
| Model Number | WW70T4040EE |
| Serial Number | SN-DUP-FIRST-001 |
| Purchase Date | 2025-02-01 |
| Fault Category | Motherboard / Board Failure |
| Damage / Exclusions | None (Standard Defect) |
| Fault Occurrence Date | 2026-06-01 |
| Receipt | Upload **any small file from your computer** |

Second submission (after first completes):

| Field | Value |
|---|---|
| Product Name | Samsung Washing Machine WW70T |
| Brand | Samsung |
| Model Number | WW70T4040EE |
| Serial Number | **SN-DUP-SECOND-002** (different serial) |
| Purchase Date | 2025-02-01 |
| Fault Category | Motherboard / Board Failure |
| Damage / Exclusions | None (Standard Defect) |
| Fault Occurrence Date | 2026-06-01 |
| Receipt | Upload the **exact same file** as the first claim |

Expected on second dossier: Yellow **Manual Review Required**. Opposing Factors: ''Duplicate Document: Identical receipt hash matches previous Claim CLM-2026-XXXX.''

---

## 5. TROUBLESHOOTING

| What you see | What it means | What to do |
|---|---|---|
| ''This site can not be reached'' | Server not started yet | Wait 10 sec, refresh. Check terminal for error messages. |
| Submit Claim hangs for 10+ seconds | Models loading in background (up to 15s wait is built in) | Wait patiently. |
| 503 error after submitting | Models did not load within 15 seconds | Restart run_app.bat, wait for ''All models ready'', resubmit. |
| Claim Summary Card is a broken image | uploads/ folder was deleted or card was not saved | Re-submit the claim. |
| ''Likely Valid'' claim returns as ''Manual Review Required'' | AI models are probabilistic, confidence can vary | Normal. Weak Match or Uncertain Result triggers review. Not a bug. |
| OCR shows no extracted data | OCR (EasyOCR) needs high-res, clear receipt images | Upload a clear photo or PDF for best results. |
| Dashboard shows different numbers for different roles | Customers see only their own claims; others see all | Expected role-based behaviour. |
| Reviewer Queue is empty | No Manual Review Required claims have been submitted yet | Submit Scenario 4 (Contradiction) to add one. |
| run_app.bat closes immediately | Python/uv environment issue | Right-click, Run as Administrator, or run uvicorn manually in terminal. |
