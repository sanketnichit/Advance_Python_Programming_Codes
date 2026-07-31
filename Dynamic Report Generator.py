"""
SECURITY INCIDENT REPORT GENERATOR
OOP Practical: Decorators | classmethod | Magic (dunder) methods
Author: SANKY
"""

import functools
from datetime import datetime


# =====================================================================
# 1. DECORATORS
# =====================================================================

def log_action(func):
    """Prints a start/end trace line whenever a decorated method runs."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[TRACE] {func.__name__}() invoked")
        result = func(*args, **kwargs)
        print(f"[TRACE] {func.__name__}() completed")
        return result
    return wrapper


def redact(*sensitive_words):
    """Decorator FACTORY: masks any given word in the returned text."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            for word in sensitive_words:
                text = text.replace(word, "#" * len(word))
            return text
        return wrapper
    return decorator


def severity_banner(level):
    """Decorator FACTORY: wraps text in a banner whose marker character
    depends on the severity level passed in."""
    markers = {"LOW": "-", "MEDIUM": "*", "HIGH": "#", "CRITICAL": "!"}
    marker = markers.get(level.upper(), "-")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            content = func(*args, **kwargs)
            line = marker * 50
            return f"{line}\n[{level.upper()}]\n{content}\n{line}"
        return wrapper
    return decorator


def timestamped(func):
    """Prefixes the returned text with the current date/time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{stamp}] {func(*args, **kwargs)}"
    return wrapper


# =====================================================================
# 2. FINDING (helper class held inside a report)
# =====================================================================

class Finding:
    def __init__(self, title, detail, severity="LOW"):
        self.title = title
        self.detail = detail
        self.severity = severity.upper()

    def __str__(self):
        return f"[{self.severity}] {self.title}: {self.detail}"

    def __repr__(self):
        return f"Finding({self.title!r}, severity={self.severity!r})"

    def __eq__(self, other):
        return (isinstance(other, Finding) and self.title == other.title
                and self.detail == other.detail and self.severity == other.severity)


# =====================================================================
# 3. INCIDENT REPORT (core class)
# =====================================================================

class IncidentReport:
    _playbooks = {}  # class-level registry shared by every instance

    def __init__(self, case_id, analyst="Unassigned"):
        self.case_id = case_id
        self.analyst = analyst
        self.findings = []
        self.opened_on = datetime.now()

    # ---- classmethods: playbook management + alternate constructor ----
    @classmethod
    def register_playbook(cls, name, finding_titles):
        cls._playbooks[name] = finding_titles
        print(f"[PLAYBOOK] '{name}' registered -> {finding_titles}")

    @classmethod
    def from_playbook(cls, name, case_id, analyst="Unassigned"):
        if name not in cls._playbooks:
            raise ValueError(f"Playbook '{name}' has not been registered")
        report = cls(case_id, analyst)
        for title in cls._playbooks[name]:
            report.log_finding(title, "pending investigation", severity="LOW")
        return report

    @classmethod
    def available_playbooks(cls):
        return list(cls._playbooks.keys())

    # ---- instance methods ----
    def log_finding(self, title, detail, severity="LOW"):
        self.findings.append(Finding(title, detail, severity))
        return self  # allows chaining

    def update_finding(self, title, detail=None, severity=None):
        for f in self.findings:
            if f.title == title:
                if detail is not None:
                    f.detail = detail
                if severity is not None:
                    f.severity = severity.upper()
                return True
        return False

    def highest_severity(self):
        order = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        if not self.findings:
            return "LOW"
        return max((f.severity for f in self.findings), key=order.index)

    @log_action
    @severity_banner("HIGH")
    def executive_summary(self):
        return (f"Case: {self.case_id}\nAnalyst: {self.analyst}\n"
                f"Findings logged: {len(self.findings)}\n"
                f"Highest severity: {self.highest_severity()}\n"
                f"Opened: {self.opened_on:%Y-%m-%d %H:%M}")

    @timestamped
    def case_line(self):
        return f"CASE {self.case_id} — {self.analyst}"

    def confidential_dump(self, *hide_words):
        """Applies redact() dynamically at call time, not with @ syntax,
        to show decorators can also be applied on the fly."""
        raw = str(self)

        @redact(*hide_words)
        def _inner():
            return raw
        return _inner()

    # ---- magic methods ----
    def __str__(self):
        lines = [f"INCIDENT REPORT: {self.case_id}", f"Analyst: {self.analyst}", "=" * 40]
        lines += [str(f) for f in self.findings]
        return "\n".join(lines)

    def __repr__(self):
        return f"IncidentReport(case_id={self.case_id!r}, findings={len(self.findings)})"

    def __len__(self):
        return len(self.findings)

    def __getitem__(self, index):
        return self.findings[index]

    def __iter__(self):
        return iter(self.findings)

    def __contains__(self, title):
        return any(f.title == title for f in self.findings)

    def __add__(self, other):
        if not isinstance(other, IncidentReport):
            return NotImplemented
        merged = IncidentReport(f"{self.case_id}+{other.case_id}", self.analyst)
        merged.findings = self.findings + other.findings
        return merged

    def __eq__(self, other):
        return (isinstance(other, IncidentReport) and self.case_id == other.case_id
                and self.findings == other.findings)

    def __call__(self, formatter=None):
        text = str(self)
        return formatter(text) if formatter else text


# =====================================================================
# 4. DEMO
# =====================================================================
if __name__ == "__main__":
    IncidentReport.register_playbook(
        "phishing", ["Suspicious sender", "Malicious link", "User action taken"])
    print("\nAvailable playbooks:", IncidentReport.available_playbooks())

    r1 = IncidentReport.from_playbook("phishing", case_id="CASE-101", analyst="SANKY")
    r1.update_finding("Suspicious sender", "Spoofed domain mimicking IT helpdesk", severity="MEDIUM")
    r1.update_finding("Malicious link", "Credential harvesting page", severity="HIGH")
    r1.update_finding("User action taken", "User reset password immediately", severity="LOW")

    r2 = IncidentReport("CASE-102", analyst="SANKY")
    r2.log_finding("Unusual login", "Login from unrecognized country", severity="MEDIUM")

    print("\n--- len(r1) ---"); print(len(r1))
    print("\n--- r1[0] ---"); print(r1[0])
    print("\n--- iterate over r1 ---")
    for finding in r1:
        print(" •", finding.title, "-", finding.severity)
    print("\n--- 'Malicious link' in r1 ---"); print("Malicious link" in r1)
    print("\n--- combine r1 + r2 ---"); print(r1 + r2)
    print("\n--- r1 == r1 ---"); print(r1 == r1)

    print("\n--- executive_summary() [banner + traced] ---")
    print(r1.executive_summary())
    print("\n--- case_line() [timestamped] ---")
    print(r1.case_line())
    print("\n--- confidential_dump() redacting a word at call time ---")
    print(r1.confidential_dump("helpdesk"))
    print("\n--- report as callable, UPPERCASE formatter ---")
    print(r1(formatter=str.upper))
    print("\n--- report as callable, default ---")
    print(r2())