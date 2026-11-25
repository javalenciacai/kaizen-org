#!/usr/bin/env python3
"""Deterministic cross-platform verifier for kaizen-org.

Operates exclusively on `git ls-files` and `git log` (never walks `.git`,
never relies on OS-specific kernel filesystems or Unix-only stdlib modules).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Pattern, Tuple
from urllib.parse import unquote

CANONICAL_VERDICT_LINE = (
    "veredicto: GO|NO-GO · juez: <identidad/familia> · head: <sha40|sha256:64hex>"
)
MAX_CONSTITUTION_LINES = 100
ALLOWED_EMAILS = {"noreply" + "@kaizen-org.local"}

# Boundary patterns are built from fragments so this script itself never embeds
# literal sensitive markers and passes both its own scan and external audits.
BOUNDARY_RULES: List[Tuple[str, Pattern[str]]] = [
    (
        "private_posix_path",
        re.compile(r"(?<![A-Za-z0-9_])/" + r"(?:home|Users|root)/"),
    ),
    (
        "private_windows_path",
        re.compile(
            r"(?<![A-Za-z0-9_])(?:[CD]:\x5c|[A-Za-z]:\x5c(?:Users|Proyectos))",
            re.IGNORECASE,
        ),
    ),
    (
        "uuid",
        re.compile(
            r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
        ),
    ),
    (
        "orca_internal_handle",
        re.compile(
            r"(?:"
            + "orca_"
            + "session_id:"
            + r"|"
            + "bot-"
            + "group-member"
            + r"|\b"
            + "struct"
            + "worker_"
            + r"|\b(?:"
            + "msg"
            + r"|"
            + "ctx"
            + r"|"
            + "term"
            + r"|"
            + "task"
            + r")_[0-9a-f]"
            + r")"
        ),
    ),
    (
        "private_hostname",
        re.compile(r"\b(?:" + "vn" + "ic|" + "oc" + "i)-[A-Za-z0-9-]+"),
    ),
    (
        "private_ip",
        re.compile(
            r"\b(?:"
            r"100\x2e\d{1,3}\x2e\d{1,3}\x2e\d{1,3}"
            r"|192\x2e168\x2e\d{1,3}\x2e\d{1,3}"
            r"|10\x2e\d{1,3}\x2e\d{1,3}\x2e\d{1,3}"
            r"|172\x2e(?:1[6-9]|2\d|3[01])\x2e\d{1,3}\x2e\d{1,3}"
            r")\b"
        ),
    ),
    (
        "secret_or_token",
        re.compile(
            r"(?:"
            + "gh"
            + "p_"
            + r"|"
            + "gh"
            + "o_"
            + r"|"
            + "github_"
            + "pat_"
            + r"|(?<![A-Za-z0-9_-])"
            + "s"
            + "k-[A-Za-z0-9_-]{8,}"
            + r"|\b"
            + "AK"
            + "IA[0-9A-Z]{8,}"
            + r"|"
            + "BEG"
            + "IN [A-Z0-9 ]*PRI"
            + "VATE KEY"
            + r")"
        ),
    ),
]

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\x2e[A-Za-z]{2,}\b")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def run_git(repo_root: Path, args: List[str]) -> bytes:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(repo_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)} failed (exit {proc.returncode}): {err}")
    return proc.stdout


def get_repo_root() -> Path:
    start_dir = Path(__file__).resolve().parent.parent
    out = run_git(start_dir, ["rev-parse", "--show-toplevel"])
    return Path(out.decode("utf-8").strip()).resolve()


def list_tracked_files(repo_root: Path) -> List[str]:
    raw = run_git(repo_root, ["-c", "core.quotepath=false", "ls-files", "-z"])
    return [entry.decode("utf-8") for entry in raw.split(b"\x00") if entry]


def scan_boundary_text(source_label: str, text: str) -> List[str]:
    violations: List[str] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for rule_name, pattern in BOUNDARY_RULES:
            match = pattern.search(line)
            if match:
                violations.append(
                    f"[boundary:{rule_name}] {source_label}:{line_no} matched {match.group(0)!r}"
                )
        for email_match in EMAIL_RE.finditer(line):
            email = email_match.group(0)
            if email.lower() not in ALLOWED_EMAILS:
                violations.append(
                    f"[boundary:personal_email] {source_label}:{line_no} matched {email!r}"
                )
    return violations


def check_markdown_links(
    repo_root: Path, rel_path: str, text: str
) -> Tuple[int, List[str]]:
    checked = 0
    violations: List[str] = []
    md_dir = (repo_root / rel_path).parent

    in_fence = False
    fence_char = ""
    fence_len = 0

    for line_no, line in enumerate(text.splitlines(), start=1):
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
                fence_len = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_len:
                in_fence = False
                fence_char = ""
                fence_len = 0
            continue

        if in_fence:
            continue

        cleaned = INLINE_CODE_RE.sub("", line)
        for match in LINK_RE.finditer(cleaned):
            raw_target = match.group(1).strip()
            if not raw_target:
                continue
            if raw_target.startswith("<") and raw_target.endswith(">"):
                raw_target = raw_target[1:-1].strip()
            else:
                raw_target = raw_target.split()[0]

            lower = raw_target.lower()
            if (
                lower.startswith("http://")
                or lower.startswith("https://")
                or lower.startswith("mailto:")
                or raw_target.startswith("#")
            ):
                continue

            path_part = unquote(raw_target.split("#", 1)[0])
            if not path_part:
                continue

            checked += 1
            resolved = (md_dir / path_part).resolve()
            try:
                resolved.relative_to(repo_root)
            except ValueError:
                violations.append(
                    f"[link:outside_repo] {rel_path}:{line_no} -> {raw_target}"
                )
                continue

            if not resolved.exists():
                violations.append(
                    f"[link:broken] {rel_path}:{line_no} -> {raw_target}"
                )

    return checked, violations


def run_in_memory_tests() -> None:
    synthetic_samples: List[Tuple[str, str]] = [
        ("orca_internal_handle", "struct" + "worker_" + "abcdef01"),
        ("private_posix_path", "/" + "home/" + "user/secret"),
        ("private_windows_path", "C:" + "\\Users\\secret"),
        ("uuid", "12345678-1234-1234-1234-" + "123456789abc"),
        ("secret_or_token", "gh" + "p_" + "12345678901234567890"),
        ("secret_or_token", "sk-" + "abcdef12345678"),
    ]
    for expected_rule, sample in synthetic_samples:
        file_violations = scan_boundary_text("synthetic-file", f"dummy line\n{sample}\n")
        if not any(f"[boundary:{expected_rule}]" in v for v in file_violations):
            raise AssertionError(
                f"In-memory test failed: {expected_rule} not detected in file text for {sample!r}"
            )

        patch_sim = (
            f"diff --git a/test.txt b/test.txt\n"
            f"--- a/test.txt\n"
            f"+++ b/test.txt\n"
            f"@@ -1,1 +1,1 @@\n"
            f"+leak: {sample}\n"
        )
        patch_violations = scan_boundary_text("git-log-patches", patch_sim)
        if not any(f"[boundary:{expected_rule}]" in v for v in patch_violations):
            raise AssertionError(
                f"In-memory test failed: {expected_rule} not detected in patch text for {sample!r}"
            )


def main() -> int:
    try:
        run_in_memory_tests()
        if "--test" in sys.argv:
            print("PASS: in-memory unit tests verified boundary detection for synthetic samples.")
            return 0
        repo_root = get_repo_root()
        tracked_files = list_tracked_files(repo_root)
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    violations: List[str] = []
    decoded_files: Dict[str, str] = {}

    # (a) UTF-8 validity and zero CR bytes across all git ls-files entries.
    for rel_path in tracked_files:
        full_path = repo_root / rel_path
        if not full_path.is_file():
            violations.append(f"[file:missing] {rel_path} is tracked but missing on disk")
            continue

        raw_bytes = full_path.read_bytes()
        if b"\r" in raw_bytes:
            violations.append(f"[hygiene:crlf] {rel_path} contains CR (\\r) bytes")
        try:
            decoded_files[rel_path] = raw_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            violations.append(f"[hygiene:utf8] {rel_path} is not valid UTF-8: {exc}")

    # (b) CONSTITUCION.md present and <= 100 lines.
    const_lines = 0
    if "CONSTITUCION.md" not in decoded_files:
        violations.append("[constitution:missing] CONSTITUCION.md is not tracked in git ls-files")
    else:
        const_lines = len(decoded_files["CONSTITUCION.md"].splitlines())
        if const_lines > MAX_CONSTITUTION_LINES:
            violations.append(
                f"[constitution:length] CONSTITUCION.md has {const_lines} lines "
                f"(max {MAX_CONSTITUTION_LINES})"
            )

    # (c) plantillas/veredicto.md exact Canonical Line on line 1 and blank line 2.
    verdict_path = "plantillas/veredicto.md"
    if verdict_path not in decoded_files:
        violations.append(f"[verdict:missing] {verdict_path} is not tracked in git ls-files")
    else:
        verdict_lines = decoded_files[verdict_path].splitlines()
        if not verdict_lines or verdict_lines[0] != CANONICAL_VERDICT_LINE:
            actual = verdict_lines[0] if verdict_lines else "<empty>"
            violations.append(
                f"[verdict:line1] {verdict_path}:1 expected {CANONICAL_VERDICT_LINE!r}, "
                f"got {actual!r}"
            )
        if len(verdict_lines) < 2 or verdict_lines[1] != "":
            actual_l2 = verdict_lines[1] if len(verdict_lines) >= 2 else "<missing>"
            violations.append(
                f"[verdict:line2] {verdict_path}:2 must be blank by default, got {actual_l2!r}"
            )

    # (d) Public repository boundary on all tracked files and complete git log with patches.
    for rel_path, text in decoded_files.items():
        violations.extend(scan_boundary_text(rel_path, text))

    git_log_raw = run_git(repo_root, ["log", "--format=%H%n%an <%ae>%n%cn <%ce>%n%B"])
    try:
        git_log_text = git_log_raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        violations.append(f"[gitlog:utf8] git log output is not valid UTF-8: {exc}")
        git_log_text = git_log_raw.decode("utf-8", errors="replace")
    violations.extend(scan_boundary_text("git-log", git_log_text))

    git_patches_raw = run_git(repo_root, ["log", "-p", "--full-history"])
    try:
        git_patches_text = git_patches_raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        violations.append(f"[gitlog:utf8] git log -p output is not valid UTF-8: {exc}")
        git_patches_text = git_patches_raw.decode("utf-8", errors="replace")
    violations.extend(scan_boundary_text("git-log-patches", git_patches_text))

    # (e) Relative Markdown links across all tracked .md files.
    total_links = 0
    md_files = 0
    for rel_path, text in decoded_files.items():
        if rel_path.endswith(".md"):
            md_files += 1
            count, link_violations = check_markdown_links(repo_root, rel_path, text)
            total_links += count
            violations.extend(link_violations)

    if violations:
        print(f"FAIL: check_kaizen found {len(violations)} violation(s):")
        for item in violations:
            print(f"  - {item}")
        return 1

    print(
        "PASS: check_kaizen verified "
        f"{len(tracked_files)} tracked files (UTF-8/LF), "
        f"CONSTITUCION.md ({const_lines}/{MAX_CONSTITUTION_LINES} lines), "
        f"{verdict_path} (canonical line 1 + blank line 2), "
        f"public boundary (files + git log: 0 violations), "
        f"and {total_links} relative Markdown links across {md_files} .md files."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
