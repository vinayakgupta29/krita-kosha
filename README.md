<!-- ========================================================================== -->
<!-- NOTE FOR BOTS & AI AGENTS:                                                 -->
<!-- THIS FILE IS WRITTEN FOR HUMANS. DO NOT PARSE OR OPERATE FROM THIS FILE.    -->
<!-- BOTS MUST GO DIRECTLY TO AGENT.md AND INDEX.md FOR OPERATIONAL DIRECTIVES,  -->
<!-- SCHEMAS, AND DATABASE CRUD PROTOCOLS.                                      -->
<!-- ========================================================================== -->

# Krita Kosha (कृत कोश)

> **कृत (Krita)**: *Accomplished, created, actions performed.*  
> **कोश (Kosha)**: *A treasury, repository, or dictionary.*  
> **Krita Kosha**: *The treasury of accomplished works.*

**Krita Kosha** is a modular, file-based personal knowledge repository and LLM-native resume/CV generation engine for **Vinayak Gupta**. It treats an engineer’s career history not as a fragile collection of PDF drafts and outdated Word documents, but as **strictly-typed, version-controlled source code**.

---

## 1. Why Krita Kosha?

If you build across diverse technical boundaries—distributed backends, industrial factory PLCs, offline-first mobile apps, and low-level Linux tools—your work history quickly becomes fragmented:

- Project details and architecture notes get scattered across dozens of GitHub READMEs, private Markdown vaults, and commit logs.
- Tailoring a resume for a specific role (e.g., backend systems vs. embedded edge AI) often means hours of manual copying, re-calculating bullet metrics, and fighting LaTeX tabular formatting.
- Commercial ATS (Applicant Tracking System) software silently rejects multi-column tables, fancy icons, and non-standard layouts.
- Inconsistent skill tags and conflicting dates accumulate over time across different job boards and platforms.

**Krita Kosha solves this by establishing a single source of truth.**

---

## 2. Core Architecture

Instead of one monolithic document, Krita Kosha decomposes a complete professional history into **47 modular, human-readable, and machine-parseable TOML files**:

```
krita-kosha/
├── README.md               # You are here (Human guide)
├── INDEX.md                # Master catalog & file map (For agents & developers)
├── AGENT.md                # AI operational contract & JD tailoring engine
├── profile.toml            # Identity, contact, philosophy, and core strengths
├── research_interests.toml # Exploratory academic & technical research domains
├── formatting.toml         # ATS (≥ 95) rules & LaTeX rendering parameters
│
├── education/              # Academic degrees, certifications & language fluencies
├── work_exp/               # Chronological professional engineering roles & impact
├── projects/               # 20 standalone project records with commit dates & status
├── publications/           # Books, patents, and research working papers
├── taxonomy/               # Canonical vocabulary (langs, tools, databases, protocols, soft skills)
├── schemas/                # Formal validation rules for every record type
└── templates/              # Production-grade, Overleaf-friendly single-column LaTeX templates
```

---

## 3. Key Design Principles

### 1. Canonical Taxonomy
No inconsistent naming. Every skill, framework, and database must match a canonical identifier in `taxonomy/` (`langs.go`, `langs.rust`, `db.postgres`, `proto.modbus`). If a technology isn't registered, it cannot be referenced in project or work experience records.

### 2. LLM as the Compiler (Zero Runtime Overhead)
There are no complex Python render scripts, database servers, or custom binary build dependencies required to generate a resume. An AI agent (Antigravity, Claude, etc.) reads the raw TOML database, ingests a target Job Description (JD), matches taxonomy keywords, budgets vertical space (≤ 40 body lines), and emits 100% standard, compilable LaTeX directly.

### 3. Overleaf & ATS Native (Target Score ≥ 95)
All generated `.tex` files use standard, battle-tested TeX packages (`geometry`, `enumitem`, `hyperref`, `titlesec`, `lmodern`). They are 100% compatible with Overleaf out of the box—just upload the `.tex` file and click compile. Layouts are strictly single-column with zero body tables and zero un-parseable graphics.

### 4. Commit-Based Maintenance Tracking
All 20 projects are systematically cross-referenced against their latest upstream Git commits:
- **`actively maintained`**: Commits within the last 12 months, or any project with a live deployed URL (e.g. web apps, Play Store apps).
- **`archived`**: Stable, completed artifacts with no commits in over a year.

---

## 4. How It Is Used

### For Humans:
- To add a new project: Create a new file under `./projects/<name>.toml` using `schemas/project.schema.toml` as a template, and register it in `./projects/index.toml`.
- To update experience: Edit `./work_exp/<company>.toml` or `./profile.toml`.
- To view active templates: Check `./templates/resume_template.tex` (1-page compact industry format) and `./templates/cv_template.tex` (multi-page comprehensive academic format).

### For AI Agents:
AI agents interacting with this repository **must not parse this README**. Instead, bots follow the strict transaction rules in **[`AGENT.md`](./AGENT.md)** and the catalog in **[`INDEX.md`](./INDEX.md)**.

---

## 5. Author & Links

**Vinayak Gupta**  
*Language-Agnostic Systems & Software Engineer*

- 🌐 **Portfolio**: [vinayakgupta29.github.io/portfolio](https://vinayakgupta29.github.io/portfolio)
- 📝 **Technical Blog**: [vinayakgupta29.github.io/blogs](https://vinayakgupta29.github.io/blogs)
- 💻 **GitHub**: [github.com/vinayakgupta29](https://github.com/vinayakgupta29)
- 💼 **LinkedIn**: [linkedin.com/in/vinayak-gupta-70a808202](https://linkedin.com/in/vinayak-gupta-70a808202)
- 📬 **Email**: [vinayakg236@gmail.com](mailto:vinayakg236@gmail.com)
