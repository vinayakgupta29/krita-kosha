# Krita Kosha (कृत कोश): Agent Operational Protocol & Directives

This document is the operational contract for AI assistants (Antigravity, Gemini, Claude, etc.) interacting with **Krita Kosha**. It defines how to query the database, perform CRUD transactions, resolve data conflicts, and generate ATS-compliant (target score ≥ 95) resumes and academic CVs.

---

## 1. Core Operating Principles

1. **Single Source of Truth**: The database files within `krita-kosha/` represent the canonical truth of Vinayak Gupta's career. Never fabricate unrecorded employment dates, metrics, degrees, or publications.
2. **LLM-Native Generation**: No Python generator script or external build runner is required. The AI agent acts as the compiler—reading TOML files, applying tailoring algorithms, budgeting vertical lines, and emitting production-grade LaTeX directly into target files.
3. **Strict Sandboxing & Clean Database Invariant**: Strictly **NEVER** write generated resumes, CVs, cover letters, or build artifacts inside the `krita-kosha/` directory unless explicitly specified by the user. `krita-kosha/` is the canonical database and template repository; it MUST remain pristine. All generated documents must be written to their designated external target directories (`../${COMPANY_NAME}/` or `../schools/${SCHOOL_OR_UNI_NAME}/`).
4. **Zero-Null & Canonical Taxonomy**: All technical skills must reference canonical IDs from `taxonomy/` (`langs.*`, `fw.*`, `tools.*`, `db.*`, `proto.*`). If a new technology is introduced, add it to `taxonomy/` first.

---

## 2. Database CRUD Transaction Protocol

### 2.1. Ingesting New Work Experience
1. **Taxonomy Verification**: Check `taxonomy/*.toml` for all used tools/languages. Add missing entries with canonical IDs.
2. **Write Child File**: Create `work_exp/<company_id>.toml` following `schemas/work_exp.schema.toml`. Each bullet point MUST adhere to:
   $$\text{[Strong Action Verb]} + \text{[Technical Tool / Architecture]} + \text{[Problem Solved]} + \text{[Measurable Metric]}$$
3. **Synchronize Index**: Append a summary record to `work_exp/index.toml` with the relative path `./work_exp/<company_id>.toml`.

### 2.2. Ingesting New Projects
1. **Taxonomy Verification**: Ensure all languages and frameworks are present in `taxonomy/`.
2. **Write Project Record**: Create `projects/<project_id>.toml` adhering to `schemas/project.schema.toml`. Include:
   - Metadata (`id`, `title`, `category`, `tagline`, `repo_url`, `deployed_url`)
   - Canonical `languages` and `technologies`
   - Detailed `readme_summary` (for major systems/compilers)
   - Bullet impact statements and `keywords`
3. **Synchronize Project Index**: Add entry to `projects/index.toml`.

### 2.3. Conflict Resolution Flow
If a contradiction arises between source documents (e.g. diverging dates, differing metrics, or conflicting titles):
1. **Never guess or choose silently.**
2. Present both versions side-by-side to the user with exact source filenames and line numbers.
3. Request explicit confirmation on which figure to commit to Krita Kosha.
4. Update the affected files only after user confirmation.

---

## 3. Job Description (JD) Tailoring Pipeline

When the user asks to generate a resume or CV for a specific job description:

```
┌─────────────────┐     ┌──────────────────────┐     ┌────────────────────────┐
│ Target Job Desc │ ──▶ │ Tag & Keyword Extr.  │ ──▶ │ Score Projects & Exp   │
└─────────────────┘     └──────────────────────┘     └────────────────────────┘
                                                                 │
                                                                 ▼
┌─────────────────┐     ┌──────────────────────┐     ┌────────────────────────┐
│ Emitted LaTeX   │ ◀── │ Vertical Line Budget │ ◀── │ Pick Best Archetype &  │
│ (Target ATS≥95) │     │ (Max 40 body lines)  │     │ Bullet Filtering       │
└─────────────────┘     └──────────────────────┘     └────────────────────────┘
```

### Step 1: Extract JD Keywords & Archetype
- Identify target title (e.g. "Systems Software Engineer", "Backend Go Engineer", "Compiler Engineer", "Full-Stack Engineer").
- Extract required skills and protocols (e.g. Go, Rust, PostgreSQL, Docker, LLVM, Modbus, Concurrency).
- Determine matching profile archetype from `profile.toml`:
  - `backend_systems`
  - `systems_compiler`
  - `fullstack_agentic`
  - `academic_masters`
- **Mandatory Summary Keyword Invariant**: Regardless of the target archetype, industry, or role, the `Professional Summary` in every generated resume or CV MUST explicitly incorporate the keyword **`Fast Learner`**.

### Step 2: Score & Select Projects
- Read `projects/index.toml`.
- Calculate matching score based on `languages` and `tags` overlap with JD requirements.
- Select top 2 to 4 projects:
  - For **Systems / Compilers**: Select `vks_compiler`, `god_format`, `bahi_khata`, `http_server_c`.
  - For **Backend / Distributed**: Select `zundrath`, `vichar_abhivyakti`, `bahi_khata`, `techasoft`.
  - For **Linux / Desktop / Automation**: Select `tism_games`, `dotfiles`, `sauce_nvim`, `techasoft`.
  - For **Creative / Web / Publishing**: Select `kalam_abhivyakti`, `rang_abhivyakti`, `public_abhivyakti`.

### Step 3: Work Experience Bullet Selection
- Always include all primary verified professional companies (`techasoft`, `medoc`).
- **Appable Exclusion Note**: **Ignore `appable`** in resumes and CVs. The company refused to provide experience/relieving certificates, meaning no official proof of employment can be provided. Unless the user explicitly directs otherwise, omit Appable from all production resumes and CVs.
- For a **1-page resume**: Select 3–4 highest-impact bullets per role across the two verified companies (`techasoft` and `medoc`) that reflect the target JD's required competencies.
- For a **multi-page CV**: Include all bullets for verified roles.

### Step 4: Strict Vertical Line Budgeting (1-Page Resume)
To guarantee that a 1-page resume never overflows onto page 2:

| Resume Section | Allocated Line Count | Notes |
| :--- | :--- | :--- |
| **Header** | 3–4 lines | Name, Location, Phone, Email, GitHub, LinkedIn, Portfolio |
| **Professional Summary** | 3–4 lines | Direct from `profile.toml` tailored archetype (must include **Fast Learner**) |
| **Technical Skills** | 4–5 lines | Languages, Frameworks, Developer Tools, Databases, Protocols |
| **Work Experience** | 12–15 lines | 2 verified companies; Techasoft (5-6 lines), Medoc (7-9 lines). Appable omitted |
| **Key Projects** | 10–12 lines | 2–3 selected projects with 1–2 bullets each (e.g. VKS, GOD, PBKE/Bahi Khata) |
| **Education** | 2–3 lines | Degree, University, CGPA, Graduation Year |
| **Total Body Lines** | **≤ 40 lines** | Fits comfortably on 1 page with 1.15cm margins at 10pt |

---

## 4. ATS Compliance Rules (Score ≥ 95)

1. **Single-Column Architecture**: Multi-column tables, visual sidebars, and nested minipages confuse ATS parsers. Keep the layout 100% linear.
2. **Clean Standard Section Headings**:
   - `Professional Summary`
   - `Technical Skills`
   - `Work Experience`
   - `Key Projects`
   - `Education`
   - `Certifications & Languages` (if applicable)
3. **No Embedded Graphics or Tables for Body Text**: Avoid `tabular` environments for descriptions and bullet items. Use standard `itemize` with zero label indentation.
4. **Searchable Plain Text**: Always compile with standard Type-1/OTF fonts (`lmodern`, `Computer Modern`, or `TeX Gyre Heros`) with valid unicode mapping.
5. **No Visual Progress Bars or Star Ratings**: Represent skill levels through years of experience, production deployments, or specific certifications.
6. **Mandatory "Fast Learner" Keyword**: Every `Professional Summary` must prominently feature the exact keyword **`Fast Learner`** to signal candidate adaptability and rapid technical ramp-up.


---

## 5. Document Generation & Directory Architecture

### 5.1. Target Output Directories & Strict Sandboxing
**STRICT RULE**: AI agents must **NEVER** write generated `.tex`, `.pdf`, `.txt` files, or build artifacts inside the canonical `krita-kosha/` directory unless the user explicitly instructs otherwise. All generated artifacts must be written into their designated external peer directories:

| Document Type | Target Directory Pattern | Source LaTeX / Text File | Compiled PDF Name |
| :--- | :--- | :--- | :--- |
| **Industry Resume** | `../${COMPANY_NAME}/` | `vinayak_gupta_${JOB_TITLE}.tex` | `vinayak_gupta_${JOB_TITLE}.pdf` |
| **Cover Letter** | `../${COMPANY_NAME}/` | `vinayak_gupta_cover_letter_${JOB_TITLE}.txt` | N/A (Plaintext) |
| **Academic CV** | `../schools/${SCHOOL_OR_UNI_NAME}/` | `${DEPARTMENT}_${COURSE}_cv.tex` | `${DEPARTMENT}_${COURSE}_cv.pdf` |
| **Academic Statement** | `../schools/${SCHOOL_OR_UNI_NAME}/` | `vinayak_gupta_cover_letter_${COURSE}.txt` | N/A (Plaintext) |

#### Variable Semantic Tokens
AI agents (Gemini, Claude, Codex, etc.) should parse and populate variables using these canonical definitions:
- `${COMPANY_NAME}` (or `{{COMPANY_NAME}}`): Slugified lowercase name of the target company (e.g. `shebaz`, `techasoft`, `google`).
- `${JOB_TITLE}` (or `{{JOB_TITLE}}`): Slugified lowercase job title (e.g. `sr_node_js_engineer`, `backend_developer`, `full_stack_developer`).
- `${SCHOOL_OR_UNI_NAME}` (or `{{SCHOOL_OR_UNI_NAME}}`): Slugified lowercase university or school name (e.g. `cmu`, `stanford`, `tum`).
- `${DEPARTMENT}` (or `{{DEPARTMENT}}`): Slugified academic department (e.g. `cs`, `eecs`, `mathematics`).
- `${COURSE}` (or `{{COURSE}}`): Slugified degree or program name (e.g. `ms_cs`, `phd_systems`).

### 5.2. LaTeX Generation Instructions

When emitting LaTeX from the database:
1. Use `templates/resume_template.tex` or `templates/cv_template.tex` as structural reference.
2. Substitute placeholder macros with selected data from `profile.toml`, `work_exp/`, `projects/`, and `education/`.
3. Escape all special LaTeX characters in bullet text:
   - `%` $\rightarrow$ `\%`
   - `&` $\rightarrow$ `\&`
   - `_` $\rightarrow$ `\_`
   - `#` $\rightarrow$ `\#`
   - `$` $\rightarrow$ `\$`
   - `^` $\rightarrow$ `\textasciicircum{}`
   - `~` $\rightarrow$ `\textasciitilde{}`
4. Ensure hyperlinks use `\href{url}{display_text}` and remain clean and clickable in PDF output.

### 5.3. Local Compilation Protocol (`build-latex`) & Mandatory Cleanup

To compile LaTeX documents to PDF locally, always execute the user's custom `build-latex` CLI tool within the target document's directory. **Never** run `pdflatex` or raw compiler commands directly, and do not attempt to read the script source code.

#### Syntax & Commands:
```bash
build-latex [SOURCE] [OPTIONS]
```
- `build-latex .` : Compiles using the default source (`main.tex`).
- `build-latex clean` : Cleans temporary build artifacts (`.latex-build/`).
- `build-latex <file>.tex` : Compiles the designated `.tex` file.
- `build-latex <file>.tex -o <output>.pdf` : Compiles to a custom output PDF filename.
- `build-latex -h` / `build-latex --help` : Displays CLI help.

#### Compilation & Verification Workflow:
1. Navigate to the document directory (e.g. `../${COMPANY_NAME}`).
2. Compile and verify page constraints in a single chained command execution:
   ```bash
   build-latex vinayak_gupta_${JOB_TITLE}.tex -o vinayak_gupta_${JOB_TITLE}.pdf && pdfinfo vinayak_gupta_${JOB_TITLE}.pdf | grep "Pages:"
   ```
3. **Mandatory Post-Build Artifact Cleanup**: Immediately after successful compilation, the agent **MUST** run:
   ```bash
   build-latex clean
   ```
   This ensures that `.latex-build/` and transient files are eradicated, preserving a pristine directory containing only the finalized `.tex`, `.pdf`, and `.txt` files.

---

## 6. Single-File Export & Catalog Consolidation (dump_data.py)

For external pipelines, backups, single-prompt LLM ingestion, or offline analysis, Krita Kosha provides an automated, zero-dependency Python CLI tool: [`dump_data.py`](./dump_data.py).

### 6.1. Dynamic Resolution Architecture
When executed, `dump_data.py`:
1. Dynamically inspects each section directory (`projects/`, `work_exp/`, `education/`, `publications/`, `taxonomy/`, `schemas/`).
2. Reads the section's `index.toml` (e.g. `projects/index.toml`, `work_exp/index.toml`) to discover all registered child files via their `path` attribute.
3. Automatically ingests new child files added to any section if they are registered in the section's `index.toml`.
4. Dynamically scans for any additional or unindexed `.toml` files in each folder, ensuring zero information loss.
5. Ingests root-level knowledge files (`profile.toml`, `research_interests.toml`, `formatting.toml`) and any new root files.
6. Serializes all modules into a single, standardized TOML file (`dump.toml` by default) with clean section hierarchies and runs an internal validation pass via `tomllib`.

### 6.2. CLI Usage & Options
```bash
# Print help menu and options
python dump_data.py --help

# Generate default dump.toml (prompts for name if interactive, defaults to dump.toml)
python dump_data.py

# Specify custom output path
python dump_data.py -o dump.toml
python dump_data.py --output /path/to/my_resume_catalog.toml

# Specify custom Krita Kosha root directory
python dump_data.py -d ./krita-kosha -o dump.toml
```

### 6.3. Consolidated Output Structure
The generated `dump.toml` file contains the following primary sections:
- `[meta]`: Export timestamp, generator version, source repo info, and dynamic entity statistics.
- `[profile]`: Identity, contact URLs, philosophy, tailored summaries, and core strengths.
- `[research_interests]`: Exploratory research areas (applied statistics in AI, cognitive diversity, formal languages).
- `[formatting]`: ATS rules, line budgeting parameters, and LaTeX profile configurations.
- `[taxonomy]`: Standardized programming languages, frameworks, developer tools, databases, protocols, and soft skills.
- `[education]`: Degree records, professional certifications, and language fluencies.
- `[work_experience]`: Companies and comprehensive role records with achievement impact bullets.
- `[[projects]]`: Complete catalog of 22 engineered projects with repo links, tags, and detailed architectural README summaries.
- `[publications]`: Books, industrial patents, and manuscript research drafts.
- `[schemas]`: Structural data schemas for all entity types.

