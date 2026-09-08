# Krita Kosha (कृत कोश): Master Knowledge Index & Catalog

**Krita Kosha** is an autonomous, file-based, LLM-parseable personal database and resume/CV generation engine for **Vinayak Gupta**. It serves as the single source of truth for professional experience, engineering projects, exploratory research interests, academic history, and technical taxonomy.

---

## 1. Directory Structure & File Map

All paths within the database are relative to the root of `krita-kosha/`:

```
krita-kosha/
├── INDEX.md                     # Master catalog and database navigation (this file)
├── AGENT.md                     # Agent operational contract, CRUD protocol & JD tailoring engine
├── profile.toml                 # Candidate identity, contact links, engineering ethos, and summary archetypes
├── research_interests.toml      # Exploratory research interests and academic focus domains
├── formatting.toml              # Global ATS (≥ 95) specifications & LaTeX page profiles (resume & CV)
│
├── education/                   # Academic degrees, certifications, and language proficiencies
│   ├── index.toml               # Summary index of all degrees and certifications
│   ├── btech.toml               # B.Tech in Computer Science & Engineering (LNCT University Bhopal)
│   └── certifications.toml      # Professional certifications (IGTR) and language fluencies
│
├── work_exp/                    # Professional software engineering roles
│   ├── index.toml               # Chronological and queryable work experience index
│   ├── techasoft.toml           # Systems Engineer (Edge AI & Automation) — Techasoft Pvt. Ltd.
│   ├── medoc.toml               # Tech Lead / Systems Engineer / Intern — Medoc Health IT Pvt. Ltd.
│   └── appable.toml             # Freelance Full-Stack Developer — Appable Technologies
│
├── projects/                    # Independent engineering projects and software artifacts
│   ├── index.toml               # 19-project catalog index for rapid candidate matching
│   ├── vks_compiler.toml        # VKS-LLVM Compiler (OCaml Menhir frontend, Rust/LLVM backend)
│   ├── bahi_khata.toml          # Personal Bahi Khata (Embedded ACID Rust engine + Flutter client)
│   ├── god_format.toml          # Grounded Object Data (GOD) null-safe serialization engine
│   ├── zundrath.toml            # Zundrath Key Management System (Go, Echo, sub-2ms latency)
│   ├── http_server_c.toml       # Zero-dependency HTTP/1.1 server in pure C (POSIX sockets)
│   ├── integer_sequences.toml   # Computational discrete mathematics and integer recurrence suite
│   ├── tism_games.toml          # Real-time C++/SFML 2D desktop game collection (Smashers, Velocity)
│   ├── vichar_abhivyakti.toml   # Real-time anonymous discussion board (Go SSR, Cloudflare Workers)
│   ├── kalam_abhivyakti.toml    # Multilingual publishing platform (Ruby, Jekyll, Devanagari/JP typography)
│   ├── rang_abhivyakti.toml     # Hṛdayapāṭaḥ digital art and visual narrative portfolio (Jekyll)
│   ├── public_abhivyakti.toml   # Abhivyakti ecosystem portal hub (Dynamic interactive DOM physics)
│   ├── dotfiles.toml            # Modular Arch Linux & Hyprland Wayland environment configurations
│   ├── noctalia_plugins.toml    # Noctalia Shell desktop plugin for Fcitx5 input method switching
│   ├── sauce_nvim.toml          # Tree-sitter Neovim linter and syntax plugin
│   ├── sddm_slayer.toml         # SDDM login display manager theme in Qt/QML
│   ├── albedo_grub_theme.toml   # Minimalist high-DPI bootloader theme for GNU GRUB
│   ├── plymouth_themes.toml     # Flicker-free boot splash animations for Linux Plymouth subsystem
│   ├── poke_dex.toml            # Cross-platform mobile Pokédex in Flutter (Dart)
│   ├── py_ocr.toml              # Desktop OCR pipeline in Python with standalone containerization
│   └── accounting_inventory.toml# Complete Accounting & Inventory System (Node.js/TS, Flutter, Postgres)
│
├── publications/                # Books, patents, and research working papers
│   ├── index.toml               # Publications, patents, and manuscripts index
│   ├── book_life.toml           # Poetry collection book ('Life', Sangam Publications, 2023)
│   ├── patent_cooking.toml      # Industrial/automation patent ('System for Cooking', IPO 2025)
│   └── draft_encryption.toml    # Working paper ('A Novel approach to Encryption for Data Security')
│
├── taxonomy/                    # Canonical vocabulary for skills, tools, and protocols
│   ├── languages.toml           # Standard programming languages (`langs.*`)
│   ├── frameworks_and_tools.toml# Frameworks (`fw.*`) and Infrastructure Tools (`tools.*`)
│   ├── databases.toml           # Data storage engines (`db.*`)
│   ├── protocols.toml           # Communications, networking, and serialization formats (`proto.*`)
│   └── soft_skills.toml         # Cognitive strengths, leadership, and collaboration taxonomy
│
├── schemas/                     # Structural schemas and required field definitions
│   ├── profile.schema.toml      # Schema for candidate profile and identity
│   ├── work_exp.schema.toml     # Schema for work experience index and company records
│   ├── project.schema.toml      # Schema for project index and individual project records
│   ├── education.schema.toml    # Schema for education, certifications, and language fluencies
│   ├── publication.schema.toml  # Schema for books, patents, and working papers
│   ├── research_interests.schema.toml # Schema for prospective research domains
│   └── formatting.schema.toml   # Schema for ATS rules and rendering profile parameters
│
└── templates/                   # Standardized single-column LaTeX templates
    ├── resume_template.tex      # 1-page compact ATS-compliant resume template (Target ATS ≥ 95)
    └── cv_template.tex          # Multi-page comprehensive technical & academic CV template
```

---

## 2. Canonical Taxonomy Namespaces

When specifying technologies across `work_exp/` and `projects/`, agents MUST reference entities using their canonical namespaced ID from `taxonomy/`:

| Namespace | Source File | Description | Examples |
| :--- | :--- | :--- | :--- |
| `langs.*` | `taxonomy/languages.toml` | Programming & markup languages | `langs.go`, `langs.rust`, `langs.c`, `langs.cpp`, `langs.ocaml`, `langs.python`, `langs.dart`, `langs.typescript`, `langs.javascript`, `langs.html`, `langs.css`, `langs.ruby`, `langs.lua`, `langs.bash`, `langs.sql` |
| `fw.*` | `taxonomy/frameworks_and_tools.toml` | Application frameworks & runtime libs | `fw.django`, `fw.echo`, `fw.tauri`, `fw.flutter`, `fw.node`, `fw.express`, `fw.react`, `fw.jekyll` |
| `tools.*` | `taxonomy/frameworks_and_tools.toml` | Tools, platforms, compilers & systems | `tools.llvm`, `tools.docker`, `tools.aws`, `tools.git`, `tools.linux`, `tools.ci_cd`, `tools.html_templating`, `tools.cloudflare_workers` |
| `db.*` | `taxonomy/databases.toml` | Persistence & caching engines | `db.postgres`, `db.sqlite`, `db.mongodb`, `db.redis` |
| `proto.*` | `taxonomy/protocols.toml` | Protocols, network & data formats | `proto.modbus`, `proto.rest`, `proto.grpc`, `proto.pbke`, `proto.god` |

---

## 3. Strict Relative Path Invariant

To guarantee that `krita-kosha` can be cloned, transferred, or embedded anywhere across operating systems without broken references:
1. **Never use absolute paths** (e.g. `/home/zoro/...`) inside any TOML files.
2. All file references must begin with `./` relative to the `krita-kosha/` root directory (e.g., `./taxonomy/languages.toml`, `./projects/god_format.toml`).
