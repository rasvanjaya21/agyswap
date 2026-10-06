"""Re-vendor `# Method` and `# Reference` of the core skills from addyosmani/agent-skills.

Each skills/agyswap-<verb>/SKILL.md keeps its own agyswap section (everything above
`# Method`); the rest is rebuilt from upstream HEAD: the upstream SKILL.md body with
headings demoted one level, `../../references/*.md` links pointed at the inlined
`# Reference` section, and the referenced checklists appended. The pinned commit is
updated here and in AGENTS.md.

    uv run python scripts/skills.py           # update to upstream HEAD
    uv run python scripts/skills.py --check   # exit 1 if skills/ is behind upstream HEAD
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = "https://github.com/addyosmani/agent-skills"
ROOT = Path(__file__).resolve().parent.parent
SEPARATOR = "\n---\n\n# Method\n"

# agyswap skill -> (upstream skill, inlined references, note appended to the vendoring line)
SKILLS = {
    "agyswap-spec": (
        "spec-driven-development",
        [],
        " — termasuk lokasi file: `architecture/SPEC.md`, bukan `SPEC.md` di root",
    ),
    "agyswap-plan": (
        "planning-and-task-breakdown",
        ["definition-of-done"],
        " — termasuk lokasi file: `architecture/PLAN.md`, bukan `tasks/plan.md` atau `tasks/todo.md`",
    ),
    "agyswap-build": ("incremental-implementation", ["definition-of-done"], ""),
    "agyswap-test": (
        "test-driven-development",
        ["testing-patterns"],
        " — contoh Jest dan React Testing Library di sana diterjemahkan ke pytest",
    ),
    "agyswap-review": ("code-review-and-quality", ["performance-checklist", "security-checklist"], ""),
    "agyswap-ship": (
        "shipping-and-launch",
        ["accessibility-checklist", "definition-of-done", "performance-checklist", "security-checklist"],
        "",
    ),
}


def strip_frontmatter(text: str) -> str:
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[m.end() :] if m else text


def demote(text: str) -> str:
    out, fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
        if not fence and re.match(r"^#{1,5} ", line):
            line = "#" + line
        out.append(line)
    return "\n".join(out)


def build(up: Path, commit: str, skill: str, header: str) -> str:
    upstream, refs, note = SKILLS[skill]
    ref_dir = up / "references"

    def title(name: str) -> str:
        body = strip_frontmatter((ref_dir / f"{name}.md").read_text())
        return re.search(r"^# (.+)$", body, re.M).group(1).strip()

    def link(m: re.Match) -> str:
        if m.group(1) not in refs:
            raise SystemExit(
                f"{skill}: upstream links references/{m.group(1)}.md; add it to SKILLS in scripts/skills.py"
            )
        return f'the **{title(m.group(1))}** section under "Reference" at the end of this file'

    body = strip_frontmatter((up / "skills" / upstream / "SKILL.md").read_text()).strip()
    body = re.sub(r"`\.\./\.\./references/([a-z0-9-]+)\.md(?:#[^`]*)?`", link, demote(body))
    text = (
        header
        + SEPARATOR
        + f"\nProsedur di bawah di-vendor dari `addyosmani/agent-skills` (`skills/{upstream}`) pada commit `{commit}`. "
        + f"Bagian agyswap di atas menang setiap kali keduanya bertentangan{note}.\n\n"
        + body
        + "\n"
    )
    if refs:
        parts = [demote(strip_frontmatter((ref_dir / f"{r}.md").read_text()).strip()) for r in refs]
        text += "\n---\n\n# Reference\n\n" + "\n\n".join(parts) + "\n"
    return text


def main() -> int:
    check = "--check" in sys.argv
    with tempfile.TemporaryDirectory(prefix="agyswap-skills-") as tmp:
        subprocess.run(["git", "clone", "--quiet", "--depth", "1", REPO, tmp], check=True)
        commit = subprocess.run(
            ["git", "rev-parse", "--short=7", "HEAD"], cwd=tmp, check=True, capture_output=True, text=True
        ).stdout.strip()
        stale = []
        for skill in SKILLS:
            path = ROOT / "skills" / skill / "SKILL.md"
            current = path.read_text()
            if SEPARATOR not in current:
                raise SystemExit(f"{path}: missing the `# Method` separator")
            new = build(Path(tmp), commit, skill, current.split(SEPARATOR, 1)[0])
            if new != current:
                stale.append(skill)
                if not check:
                    path.write_text(new)
    if check:
        print(
            f"behind agent-skills@{commit}: {', '.join(stale)}" if stale else f"up to date with agent-skills@{commit}"
        )
        return 1 if stale else 0
    agents = ROOT / "AGENTS.md"
    agents.write_text(
        re.sub(r"(addyosmani/agent-skills` at commit `)[0-9a-f]{7}", rf"\g<1>{commit}", agents.read_text())
    )
    print(f"agent-skills@{commit}: updated {', '.join(stale) or 'nothing'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
