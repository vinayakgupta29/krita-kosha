#!/usr/bin/env python3
"""
dump_data.py - Krita Kosha Data Consolidation Engine

Dynamically reads all modular TOML files across Krita Kosha, resolves child records
referenced in each section's index.toml, and serializes the complete, loss-free catalog
into a single consolidated TOML file (default: dump.toml).

Zero third-party dependencies. Compatible with Python 3.11+ standard library.
"""

import os
import sys
import argparse
import tomllib
import re
from datetime import datetime, timezone
from pathlib import Path


def quote_key(key: str) -> str:
    """Quote TOML key if it contains characters outside [A-Za-z0-9_-]."""
    if re.match(r'^[A-Za-z0-9_-]+$', key):
        return key
    escaped = key.replace('\\', '\\\\').replace('"', '\\"')
    return f'"{escaped}"'


def serialize_scalar(val, indent='  ') -> str:
    """Serialize a scalar value (or list of scalars) to a TOML-compliant string."""
    if isinstance(val, bool):
        return 'true' if val else 'false'
    elif isinstance(val, int):
        return str(val)
    elif isinstance(val, float):
        return str(val)
    elif isinstance(val, str):
        if '\n' in val:
            # Multiline string in TOML
            # Escape backslashes and triple-quotes
            escaped = val.replace('\\', '\\\\').replace('"""', '\\"\\"\\"')
            return f'"""\n{escaped}"""'
        else:
            escaped = (
                val.replace('\\', '\\\\')
                .replace('"', '\\"')
                .replace('\t', '\\t')
                .replace('\r', '\\r')
            )
            return f'"{escaped}"'
    elif isinstance(val, list):
        if not val:
            return '[]'
        if all(isinstance(x, (str, int, float, bool)) for x in val):
            formatted_items = [serialize_scalar(x) for x in val]
            single = '[' + ', '.join(formatted_items) + ']'
            if len(single) < 80 and not any('\n' in str(x) for x in val):
                return single
            lines = ['[\n']
            for item in formatted_items:
                lines.append(f'{indent}  {item},\n')
            lines.append(f'{indent}]')
            return ''.join(lines)
        elif all(isinstance(x, list) for x in val):
            lines = ['[\n']
            for item in val:
                lines.append(f'{indent}  {serialize_scalar(item, indent + "  ")},\n')
            lines.append(f'{indent}]')
            return ''.join(lines)
        else:
            return '[]'
    return '""'


def is_dict_list(val) -> bool:
    """Check if value is a non-empty list of dictionaries (array of tables)."""
    return isinstance(val, list) and len(val) > 0 and all(isinstance(x, dict) for x in val)


def dump_toml_dict(data: dict) -> str:
    """
    Pure Python TOML serializer for nested dictionaries and arrays of tables.
    Guarantees that within each table, scalar key-values are emitted first,
    followed by subtables, followed by arrays of tables.
    """
    lines = []

    def write_table(t_dict: dict, current_prefix: str = ''):
        # 1. Scalar key-values first
        for k, v in t_dict.items():
            if not isinstance(v, dict) and not is_dict_list(v):
                lines.append(f'{quote_key(k)} = {serialize_scalar(v)}')

        # 2. Subtables (dict values)
        for k, v in t_dict.items():
            if isinstance(v, dict):
                sub_prefix = f'{current_prefix}.{quote_key(k)}' if current_prefix else quote_key(k)
                lines.append(f'\n[{sub_prefix}]')
                write_table(v, sub_prefix)

        # 3. Array of tables (list of dicts)
        for k, v in t_dict.items():
            if is_dict_list(v):
                sub_prefix = f'{current_prefix}.{quote_key(k)}' if current_prefix else quote_key(k)
                for item in v:
                    lines.append(f'\n[[{sub_prefix}]]')
                    write_table(item, sub_prefix)

    # Top-level sections in organized sequence
    section_order = [
        'meta',
        'profile',
        'research_interests',
        'formatting',
        'taxonomy',
        'education',
        'work_experience',
        'projects',
        'publications',
        'schemas'
    ]

    # Process ordered sections first
    processed_keys = set()
    for sec_key in section_order:
        if sec_key in data:
            processed_keys.add(sec_key)
            sec_val = data[sec_key]
            if is_dict_list(sec_val):
                for item in sec_val:
                    lines.append(f'\n[[{quote_key(sec_key)}]]')
                    write_table(item, quote_key(sec_key))
            elif isinstance(sec_val, dict):
                lines.append(f'\n[{quote_key(sec_key)}]')
                write_table(sec_val, quote_key(sec_key))
            else:
                lines.append(f'{quote_key(sec_key)} = {serialize_scalar(sec_val)}')

    # Process any remaining custom sections
    for sec_key, sec_val in data.items():
        if sec_key not in processed_keys:
            if is_dict_list(sec_val):
                for item in sec_val:
                    lines.append(f'\n[[{quote_key(sec_key)}]]')
                    write_table(item, quote_key(sec_key))
            elif isinstance(sec_val, dict):
                lines.append(f'\n[{quote_key(sec_key)}]')
                write_table(sec_val, quote_key(sec_key))
            else:
                lines.append(f'{quote_key(sec_key)} = {serialize_scalar(sec_val)}')

    return '\n'.join(lines).strip() + '\n'


class KritaKoshaConsolidator:
    def __init__(self, root_dir: Path, verbose: bool = True):
        self.root_dir = root_dir.resolve()
        self.verbose = verbose
        self.loaded_files = set()

    def log(self, msg: str):
        if self.verbose:
            print(f'[kosha-dump] {msg}')

    def load_toml(self, path: Path) -> dict:
        """Safely load and parse a TOML file."""
        resolved = path.resolve()
        self.loaded_files.add(resolved)
        with open(resolved, 'rb') as f:
            return tomllib.load(f)

    def resolve_child_path(self, parent_folder: Path, ref_path: str) -> Path | None:
        """
        Dynamically resolve relative paths given in index.toml.
        Tries relative to kosha root, relative to section folder, and basename.
        """
        candidates = [
            (self.root_dir / ref_path.lstrip('./')).resolve(),
            (parent_folder / ref_path.lstrip('./')).resolve(),
            (parent_folder / Path(ref_path).name).resolve()
        ]
        for cand in candidates:
            if cand.exists() and cand.is_file():
                return cand
        return None

    def collect_profile(self) -> dict:
        """Load profile.toml."""
        profile_file = self.root_dir / 'profile.toml'
        if profile_file.exists():
            self.log('Loading profile from profile.toml')
            return self.load_toml(profile_file)
        return {}

    def collect_research_interests(self) -> dict:
        """Load research_interests.toml."""
        rf = self.root_dir / 'research_interests.toml'
        if rf.exists():
            self.log('Loading research interests from research_interests.toml')
            return self.load_toml(rf)
        return {}

    def collect_formatting(self) -> dict:
        """Load formatting.toml."""
        ff = self.root_dir / 'formatting.toml'
        if ff.exists():
            self.log('Loading formatting specifications from formatting.toml')
            return self.load_toml(ff)
        return {}

    def collect_taxonomy(self) -> dict:
        """Dynamically load all taxonomy/*.toml files."""
        tax_dir = self.root_dir / 'taxonomy'
        taxonomy = {}
        if not tax_dir.exists():
            return taxonomy

        for p in sorted(tax_dir.glob('*.toml')):
            stem = p.stem
            self.log(f'Loading taxonomy module: {stem} ({p.name})')
            content = self.load_toml(p)
            taxonomy[stem] = content
        return taxonomy

    def collect_schemas(self) -> dict:
        """Dynamically load all schemas/*.schema.toml files."""
        schemas_dir = self.root_dir / 'schemas'
        schemas = {}
        if not schemas_dir.exists():
            return schemas

        for p in sorted(schemas_dir.glob('*.toml')):
            # e.g. project.schema.toml -> project
            key = p.name.replace('.schema.toml', '').replace('.toml', '')
            self.log(f'Loading schema specification: {key} ({p.name})')
            schemas[key] = self.load_toml(p)
        return schemas

    def collect_projects(self) -> list:
        """
        Dynamically load all projects.
        Reads projects/index.toml if present, resolves each path, merges child files,
        and also picks up any unindexed .toml files in projects/.
        """
        proj_dir = self.root_dir / 'projects'
        if not proj_dir.exists():
            return []

        projects_list = []
        indexed_files = set()
        index_file = proj_dir / 'index.toml'

        if index_file.exists():
            self.log('Processing projects/index.toml')
            index_data = self.load_toml(index_file)
            entries = index_data.get('projects', [])

            for entry in entries:
                ref_path = entry.get('path', '')
                child_file = self.resolve_child_path(proj_dir, ref_path) if ref_path else None
                
                project_record = {}
                if child_file and child_file.exists():
                    indexed_files.add(child_file.resolve())
                    self.log(f'  Resolved project [{entry.get("id")}]: {child_file.name}')
                    child_data = self.load_toml(child_file)
                    
                    # Extract project table
                    proj_inner = child_data.get('project', {})
                    project_record.update(proj_inner)

                    # Merge child top-level metadata (references, reference_urls, local_ref_path, etc.)
                    for k, v in child_data.items():
                        if k != 'project' and k not in project_record:
                            project_record[k] = v
                else:
                    self.log(f'  Notice: child file not found for project [{entry.get("id")}], using index data')

                # Merge any missing index metadata (e.g. tags, path)
                for k, v in entry.items():
                    if k not in project_record:
                        project_record[k] = v

                projects_list.append(project_record)

        # Check for unindexed project .toml files
        for p in sorted(proj_dir.glob('*.toml')):
            if p.name == 'index.toml' or p.resolve() in indexed_files:
                continue
            self.log(f'  Dynamically discovered unindexed project file: {p.name}')
            child_data = self.load_toml(p)
            proj_inner = child_data.get('project', {})
            rec = dict(proj_inner) if proj_inner else dict(child_data)
            for k, v in child_data.items():
                if k != 'project' and k not in rec:
                    rec[k] = v
            rec['source_file'] = p.name
            projects_list.append(rec)

        return projects_list

    def collect_work_experience(self) -> dict:
        """
        Dynamically load work experience.
        Reads work_exp/index.toml if present, resolves each company path,
        merges roles and metadata, and checks for unindexed files.
        """
        work_dir = self.root_dir / 'work_exp'
        if not work_dir.exists():
            return {}

        companies_list = []
        indexed_files = set()
        index_file = work_dir / 'index.toml'

        if index_file.exists():
            self.log('Processing work_exp/index.toml')
            index_data = self.load_toml(index_file)
            entries = index_data.get('companies', [])

            for entry in entries:
                ref_path = entry.get('path', '')
                child_file = self.resolve_child_path(work_dir, ref_path) if ref_path else None

                company_record = {}
                if child_file and child_file.exists():
                    indexed_files.add(child_file.resolve())
                    self.log(f'  Resolved company [{entry.get("id")}]: {child_file.name}')
                    child_data = self.load_toml(child_file)

                    comp_inner = child_data.get('company', {})
                    company_record.update(comp_inner)

                    for k, v in child_data.items():
                        if k != 'company' and k not in company_record:
                            company_record[k] = v
                else:
                    self.log(f'  Notice: child file not found for company [{entry.get("id")}], using index data')

                for k, v in entry.items():
                    if k not in company_record:
                        company_record[k] = v

                companies_list.append(company_record)

        # Check for unindexed company files
        for p in sorted(work_dir.glob('*.toml')):
            if p.name == 'index.toml' or p.resolve() in indexed_files:
                continue
            self.log(f'  Dynamically discovered unindexed work experience file: {p.name}')
            child_data = self.load_toml(p)
            comp_inner = child_data.get('company', {})
            rec = dict(comp_inner) if comp_inner else dict(child_data)
            for k, v in child_data.items():
                if k != 'company' and k not in rec:
                    rec[k] = v
            rec['source_file'] = p.name
            companies_list.append(rec)

        return {'companies': companies_list}

    def collect_education(self) -> dict:
        """
        Dynamically load education, degrees, certifications, and languages.
        Reads education/index.toml if present, resolves paths, and merges children.
        """
        edu_dir = self.root_dir / 'education'
        if not edu_dir.exists():
            return {}

        degrees_list = []
        certifications_list = []
        languages_dict = {}
        indexed_files = set()
        index_file = edu_dir / 'index.toml'

        if index_file.exists():
            self.log('Processing education/index.toml')
            index_data = self.load_toml(index_file)

            # Process degrees
            for entry in index_data.get('degrees', []):
                ref_path = entry.get('path', '')
                child_file = self.resolve_child_path(edu_dir, ref_path) if ref_path else None
                deg_rec = {}
                if child_file and child_file.exists():
                    indexed_files.add(child_file.resolve())
                    self.log(f'  Resolved degree [{entry.get("id")}]: {child_file.name}')
                    c_data = self.load_toml(child_file)
                    deg_rec.update(c_data.get('education', {}))
                    for k, v in c_data.items():
                        if k != 'education' and k not in deg_rec:
                            deg_rec[k] = v
                for k, v in entry.items():
                    if k not in deg_rec:
                        deg_rec[k] = v
                degrees_list.append(deg_rec)

            # Process certifications
            for entry in index_data.get('certifications', []):
                ref_path = entry.get('path', '')
                child_file = self.resolve_child_path(edu_dir, ref_path) if ref_path else None
                if child_file and child_file.exists():
                    indexed_files.add(child_file.resolve())
                    self.log(f'  Resolved certifications file: {child_file.name}')
                    c_data = self.load_toml(child_file)
                    # c_data may have [[certifications]] and [languages]
                    if 'certifications' in c_data:
                        for cert in c_data['certifications']:
                            if cert not in certifications_list:
                                certifications_list.append(cert)
                    if 'languages' in c_data:
                        languages_dict.update(c_data['languages'])
                else:
                    certifications_list.append(dict(entry))

        # Check for unindexed files in education
        for p in sorted(edu_dir.glob('*.toml')):
            if p.name == 'index.toml' or p.resolve() in indexed_files:
                continue
            self.log(f'  Dynamically discovered unindexed education file: {p.name}')
            c_data = self.load_toml(p)
            if 'education' in c_data:
                degrees_list.append(c_data['education'])
            elif 'certifications' in c_data:
                certifications_list.extend(c_data['certifications'])
            if 'languages' in c_data:
                languages_dict.update(c_data['languages'])

        res = {
            'degrees': degrees_list,
            'certifications': certifications_list
        }
        if languages_dict:
            res['languages'] = languages_dict
        return res

    def collect_publications(self) -> dict:
        """
        Dynamically load publications (books, patents, manuscripts).
        Reads publications/index.toml if present, resolves paths, and merges children.
        """
        pub_dir = self.root_dir / 'publications'
        if not pub_dir.exists():
            return {}

        books_list = []
        patents_list = []
        manuscripts_list = []
        indexed_files = set()
        index_file = pub_dir / 'index.toml'

        if index_file.exists():
            self.log('Processing publications/index.toml')
            index_data = self.load_toml(index_file)

            # Books
            for entry in index_data.get('books', []):
                ref_path = entry.get('path', '')
                child_file = self.resolve_child_path(pub_dir, ref_path) if ref_path else None
                rec = {}
                if child_file and child_file.exists():
                    indexed_files.add(child_file.resolve())
                    self.log(f'  Resolved book [{entry.get("id")}]: {child_file.name}')
                    c_data = self.load_toml(child_file)
                    rec.update(c_data.get('publication', {}))
                    for k, v in c_data.items():
                        if k != 'publication' and k not in rec:
                            rec[k] = v
                for k, v in entry.items():
                    if k not in rec:
                        rec[k] = v
                books_list.append(rec)

            # Patents
            for entry in index_data.get('patents', []):
                ref_path = entry.get('path', '')
                child_file = self.resolve_child_path(pub_dir, ref_path) if ref_path else None
                rec = {}
                if child_file and child_file.exists():
                    indexed_files.add(child_file.resolve())
                    self.log(f'  Resolved patent [{entry.get("id")}]: {child_file.name}')
                    c_data = self.load_toml(child_file)
                    rec.update(c_data.get('patent', {}))
                    for k, v in c_data.items():
                        if k != 'patent' and k not in rec:
                            rec[k] = v
                for k, v in entry.items():
                    if k not in rec:
                        rec[k] = v
                patents_list.append(rec)

            # Manuscripts
            for entry in index_data.get('manuscripts', []):
                ref_path = entry.get('path', '')
                # Special check: if path points to root research_interests.toml, don't duplicate full file
                if 'research_interests' in ref_path:
                    manuscripts_list.append(dict(entry))
                    continue
                child_file = self.resolve_child_path(pub_dir, ref_path) if ref_path else None
                rec = {}
                if child_file and child_file.exists():
                    indexed_files.add(child_file.resolve())
                    self.log(f'  Resolved manuscript [{entry.get("id")}]: {child_file.name}')
                    c_data = self.load_toml(child_file)
                    rec.update(c_data.get('manuscript', {}))
                    for k, v in c_data.items():
                        if k != 'manuscript' and k not in rec:
                            rec[k] = v
                for k, v in entry.items():
                    if k not in rec:
                        rec[k] = v
                manuscripts_list.append(rec)

        # Unindexed publication files
        for p in sorted(pub_dir.glob('*.toml')):
            if p.name == 'index.toml' or p.resolve() in indexed_files:
                continue
            self.log(f'  Dynamically discovered unindexed publication file: {p.name}')
            c_data = self.load_toml(p)
            if 'publication' in c_data:
                books_list.append(c_data['publication'])
            elif 'patent' in c_data:
                patents_list.append(c_data['patent'])
            elif 'manuscript' in c_data:
                manuscripts_list.append(c_data['manuscript'])
            else:
                books_list.append(c_data)

        return {
            'books': books_list,
            'patents': patents_list,
            'manuscripts': manuscripts_list
        }

    def collect_other_directories(self) -> dict:
        """
        Dynamically scan for any other custom subdirectories in krita-kosha
        that contain .toml files (e.g. awards, volunteering, etc.).
        """
        known_dirs = {
            'taxonomy', 'schemas', 'projects', 'work_exp',
            'education', 'publications', '.git', '.tmp-refs',
            'templates', 'scratch', '__pycache__'
        }
        extra_sections = {}
        for child in sorted(self.root_dir.iterdir()):
            if child.is_dir() and child.name not in known_dirs:
                toml_files = sorted(child.glob('*.toml'))
                if not toml_files:
                    continue
                self.log(f'Discovered custom section directory: {child.name}')
                # Check for index.toml
                idx = child / 'index.toml'
                if idx.exists():
                    extra_sections[child.name] = self.load_toml(idx)
                else:
                    section_data = {}
                    for tf in toml_files:
                        section_data[tf.stem] = self.load_toml(tf)
                    extra_sections[child.name] = section_data
        return extra_sections

    def consolidate(self) -> dict:
        """Execute full dynamic collection across all modules without information loss."""
        self.log(f'Starting consolidation of Krita Kosha from: {self.root_dir}')

        profile = self.collect_profile()
        research_interests = self.collect_research_interests()
        formatting = self.collect_formatting()
        taxonomy = self.collect_taxonomy()
        education = self.collect_education()
        work_experience = self.collect_work_experience()
        projects = self.collect_projects()
        publications = self.collect_publications()
        schemas = self.collect_schemas()
        custom_sections = self.collect_other_directories()

        # Meta catalog information
        meta = {
            'title': 'Krita Kosha - Consolidated Master Resume & Portfolio Knowledge Base',
            'generator': 'dump_data.py (Krita Kosha Data Consolidation Engine)',
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'version': '1.0.0',
            'author': 'Vinayak Gupta',
            'source_repository': 'vinayakgupta29/krita-kosha',
            'summary': (
                'Consolidated single-file export containing complete profile, research interests, '
                'education, work experience, projects, publications, canonical taxonomy, and formatting rules.'
            ),
            'stats': {
                'total_source_files_ingested': len(self.loaded_files),
                'total_projects': len(projects),
                'total_companies': len(work_experience.get('companies', [])),
                'total_degrees': len(education.get('degrees', [])),
                'total_certifications': len(education.get('certifications', [])),
                'total_books': len(publications.get('books', [])),
                'total_patents': len(publications.get('patents', [])),
                'total_manuscripts': len(publications.get('manuscripts', []))
            }
        }

        consolidated = {
            'meta': meta,
            'profile': profile,
            'research_interests': research_interests,
            'formatting': formatting,
            'taxonomy': taxonomy,
            'education': education,
            'work_experience': work_experience,
            'projects': projects,
            'publications': publications,
            'schemas': schemas
        }

        # Add any custom sections
        for k, v in custom_sections.items():
            consolidated[k] = v

        self.log(f'Consolidation complete: {meta["stats"]["total_source_files_ingested"]} files ingested.')
        return consolidated


def detect_kosha_root(hint_dir: str | None = None) -> Path:
    """Auto-detect the krita-kosha directory."""
    if hint_dir:
        p = Path(hint_dir).resolve()
        if p.exists() and p.is_dir():
            return p
        raise FileNotFoundError(f'Specified directory does not exist: {hint_dir}')

    # Check candidates
    candidates = [
        Path.cwd(),
        Path.cwd() / 'krita-kosha',
        Path(__file__).resolve().parent,
        Path(__file__).resolve().parent / 'krita-kosha'
    ]
    for c in candidates:
        if (c / 'profile.toml').exists() and (c / 'projects').exists():
            return c.resolve()

    # Fallback to cwd
    return Path.cwd().resolve()


def main():
    parser = argparse.ArgumentParser(
        prog='dump_data.py',
        description='Consolidate Krita Kosha modular database into a single, unified TOML file without loss of information.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Examples:
  python dump_data.py
  python dump_data.py -o dump.toml
  python dump_data.py --output /path/to/my_resume_catalog.toml
  python dump_data.py -d ./krita-kosha -o master_dump.toml
        '''
    )
    parser.add_argument(
        '-o', '--output',
        dest='output',
        help='Path or filename for the consolidated output TOML file (default: dump.toml)'
    )
    parser.add_argument(
        '-d', '--dir',
        dest='dir',
        help='Path to the krita-kosha root directory (default: auto-detected)'
    )
    parser.add_argument(
        '--no-verify',
        action='store_true',
        help='Skip self-verification pass using tomllib parser'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress progress output'
    )

    args = parser.parse_args()

    # Determine kosha root directory
    try:
        kosha_dir = detect_kosha_root(args.dir)
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)

    # Determine output path
    out_name = args.output
    if not out_name:
        # Check if stdin is interactive
        if sys.stdin.isatty():
            try:
                user_input = input('Enter output TOML filename [default: dump.toml]: ').strip()
                out_name = user_input if user_input else 'dump.toml'
            except (KeyboardInterrupt, EOFError):
                print('\nOperation cancelled.')
                sys.exit(0)
        else:
            out_name = 'dump.toml'

    out_path = Path(out_name)
    if not out_path.is_absolute():
        # Place relative to current working directory
        out_path = Path.cwd() / out_path

    consolidator = KritaKoshaConsolidator(kosha_dir, verbose=not args.quiet)
    consolidated_data = consolidator.consolidate()

    # Serialize to TOML
    if not args.quiet:
        print(f'[kosha-dump] Serializing to TOML...')
    toml_str = dump_toml_dict(consolidated_data)

    # Verify parsing unless disabled
    if not args.no_verify:
        if not args.quiet:
            print('[kosha-dump] Running self-verification with tomllib parser...')
        try:
            verified_data = tomllib.loads(toml_str)
            assert 'meta' in verified_data
            assert 'profile' in verified_data
            assert 'projects' in verified_data
            assert len(verified_data['projects']) == len(consolidated_data['projects'])
            if not args.quiet:
                print(f'[kosha-dump] Verification successful! ({len(verified_data["projects"])} projects verified)')
        except Exception as e:
            print(f'Error: Self-verification failed: {e}', file=sys.stderr)
            sys.exit(1)

    # Write output file
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(toml_str)
        if not args.quiet:
            size_kb = out_path.stat().st_size / 1024
            print(f'[kosha-dump] Consolidated catalog written to: {out_path} ({size_kb:.1f} KB)')
    except Exception as e:
        print(f'Error writing output file {out_path}: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
