# Krita Kosha (कृत कोश): Agent Operational Protocol & Directives

This document is the operational contract for AI assistants (Antigravity, Gemini, Claude, etc.) interacting with **Krita Kosha**. It defines how to query the database, perform CRUD transactions, resolve data conflicts, and generate ATS-compliant (target score ≥ 95) resumes and academic CVs.

---

## 1. Core Operating Principles

1. **Single Source of Truth**: The database files within `krita-kosha/` represent the canonical truth of Vinayak Gupta's career. Never fabricate unrecorded employment dates, metrics, degrees, or publications.
2. **LLM-Native Generation**: No Python generator script or external build runner is required. The AI agent acts as the compiler—reading TOML files, applying tailoring algorithms, budgeting vertical lines, and emitting production-grade LaTeX directly into target files.
3. **Strict Sandboxing**: Do not traverse directories outside `krita-kosha/` unless the user explicitly provides an external repository path.
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

### Step 2: Score & Select Projects
- Read `projects/index.toml`.
- Calculate matching score based on `languages` and `tags` overlap with JD requirements.
- Select top 2 to 4 projects:
  - For **Systems / Compilers**: Select `vks_compiler`, `god_format`, `bahi_khata`, `http_server_c`.
  - For **Backend / Distributed**: Select `zundrath`, `vichar_abhivyakti`, `bahi_khata`, `techasoft`.
  - For **Linux / Desktop / Automation**: Select `tism_games`, `dotfiles`, `sauce_nvim`, `techasoft`.
  - For **Creative / Web / Publishing**: Select `kalam_abhivyakti`, `rang_abhivyakti`, `public_abhivyakti`.

### Step 3: Work Experience Bullet Selection
- Always include all primary professional companies (`techasoft`, `medoc`, `appable`).
- For a **1-page resume**: Select 2–3 highest-impact bullets per role that reflect the target JD's required competencies.
- For a **multi-page CV**: Include all 3–5 bullets per role.

### Step 4: Strict Vertical Line Budgeting (1-Page Resume)
To guarantee that a 1-page resume never overflows onto page 2:

| Resume Section | Allocated Line Count | Notes |
| :--- | :--- | :--- |
| **Header** | 3–4 lines | Name, Location, Phone, Email, GitHub, LinkedIn |
| **Professional Summary** | 3–4 lines | Direct from `profile.toml` tailored archetype |
| **Technical Skills** | 4–5 lines | Languages, Frameworks, Developer Tools, Databases, Protocols |
| **Work Experience** | 15–18 lines | 3 companies; Techasoft (4-5 lines), Medoc (6-7 lines), Appable (3-4 lines) |
| **Key Projects** | 8–10 lines | 2–3 selected projects with 1–2 bullets each |
| **Education** | 2–3 lines | Degree, University, CGPA, Graduation Year |
| **Total Body Lines** | **≤ 40 lines** | Fits comfortably on 1 page with 1.2cm margins at 10pt |

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

---

## 5. LaTeX Generation Instructions

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
