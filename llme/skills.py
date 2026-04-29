"""
Agent Skills support for llme.
Based on https://agentskills.io/specification
"""
import os
import re
import logging
from pathlib import Path

import yaml

logger = logging.getLogger('llme')


# XDG Base Directory Specification paths for skills
SKILL_SEARCH_PATHS = [
    Path.home() / ".config" / "llme" / "skills",
    Path(__file__).parent / "skills",
    Path.cwd() / "skills",
]


class Skill:
    def __init__(self, name, desc, dirpath, meta):
        self.name = name
        self.desc = desc
        self.dirpath = dirpath
        self.meta = meta


def validate_skill_name(name: str) -> bool:
    """
    Validate skill name against Agent Skills spec:
    - 1-64 characters
    - lowercase alphanumeric and hyphens only
    - Must not start or end with hyphen
    - No consecutive hyphens
    """
    if not name or len(name) > 64:
        return False
    # Regex: starts with alnum, ends with alnum, allows hyphens in between, no consecutive hyphens
    pattern = r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$'
    if not re.match(pattern, name):
        return False
    if '--' in name:
        return False
    return True


def parse_skill_md(content: str) -> tuple[dict, str]:
    """
    Parse a SKILL.md file. Returns (frontmatter_dict, body_string).
    """
    if not content.startswith('---'):
        return {}, content

    try:
        end_marker = content.index('---', 3)
        yaml_block = content[3:end_marker]
        body = content[end_marker+3:].strip()
        
        # safe_load handles standard YAML spec correctly
        metadata = yaml.safe_load(yaml_block)
        if not isinstance(metadata, dict):
            metadata = {}
            
        return metadata, body
    except yaml.YAMLError as e:
        logger.warning(f"Failed to parse YAML frontmatter in SKILL.md: {e}")
        return {}, content

def prompt_for_skills(skills):
    lines = [
            "## Skills\n",
            "The following skills provide specialized instructions for specific tasks.",
            "Use the read tool to load a skill's file when the task matches its description.",
            "When a skill file references a relative path, resolve it against the skill directory (parent of SKILL.md / dirname of the path) and use that absolute path in tool commands.",
            "",
        ]

    for name, s in skills.items():
        lines.append(f"Name: {s.name}\nDescription: {s.desc}\nFile: {s.dirpath}/SKILL.md\n")
    return '\n'.join(lines)


def discover_skills(directories):
    skills = {}
    for basedir in directories:
        base_dir = Path(basedir)
        if base_dir.is_dir():
            pass
        else:
            base_dir = Path.home() / ".config" / "llme" / "skills_store" / basedir
            if base_dir.is_dir():
                pass
            else:
                logger.warning("skill directory %s not found", basedir)
                continue
        skills.update(discover_skills_rec(base_dir))
    return skills


def discover_skills_rec(directory):
    """
    Scan standard paths for valid Agent Skills directories.
    Returns dict: { dir_name: skill_data }
    """
    skills = {}
    logger.debug("[skills] check %s", directory)
    for entry in sorted(os.listdir(directory)):
        skill_file = directory / entry
        
        if skill_file.is_dir():
            # Recursive search
            skills.update(discover_skills_rec(skill_file))
            continue

        if entry != "SKILL.md":
            continue

        logger.debug("[skills] found %s", skill_file)

        try:
            raw_content = skill_file.read_text(encoding="utf-8")
        except OSError:
            continue
        
        meta, body = parse_skill_md(raw_content)
        skill_name = meta.get('name', '')
        
        # Validation
        if not validate_skill_name(skill_name):
            logger.debug(f"Skipping {entry}: invalid skill name '{skill_name}'")
            continue
        
        # Spec: name must match directory name
        if skill_name != directory.name:
            logger.debug(f"Skipping {entry}: name field '{skill_name}' != directory '{directory.name}'")
            continue

        # Spec: description must exist and be < 1024 chars
        desc = meta.get('description', '')
        if not desc or len(desc) > 1024:
            logger.warning(f"Skipping {skill_name}: invalid or missing description")
            continue

        # Discover optional directories for context
        context_files = []
        for subdir in ["references", "assets"]:
            sub_path = directory / subdir
            if sub_path.is_dir():
                for fname in sorted(os.listdir(sub_path)):
                    fpath = sub_path / fname
                    if fpath.is_file():
                        context_files.append(str(fpath))

        skills[skill_name] = Skill(
                skill_name.strip(),
                desc.strip(),
                str(directory),
                meta,
        )

    return skills


def list_skills(skills):
    """List all discoverable agent skills."""
    if not skills:
        print("No skills found.")
        return
    
    for name, s in skills.items():
        print(f"{name}: {s.desc} ({s.dirpath})")
