"""
=====================================================================
 SECURITY INCIDENT REPORT GENERATOR
 Topics covered: Decorators | classmethod | Magic Methods (dunder)
=====================================================================
Author: SANKY

This program shows the same 3 Python OOP concepts using a
security-incident theme instead of a generic report: logging
findings for a case (like "Suspicious sender", "Malicious link")
under an incident report.

Concept 1: DECORATORS
   - A decorator is a function that adds extra work around
     another function, without changing that function's code.

Concept 2: CLASSMETHOD
   - A classmethod works on the CLASS itself (cls), so it can
     create objects in a special way, or store data shared by
     ALL objects of that class.

Concept 3: MAGIC METHODS (dunder methods)
   - Special methods Python calls automatically when we use
     print(), len(), indexing, +, == etc. on our own class.
=====================================================================
"""


# =====================================================================
# PART 1: DECORATORS
# =====================================================================

def uppercase(func):
    """Makes the text returned by func() become UPPERCASE."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper


def tag_alert(func):
    """Wraps the text with [ALERT] markers front and back."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return "[ALERT] " + result + " [ALERT]"
    return wrapper


def add_border(func):
    """Adds a line of '=' characters above and below the text."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        border = "=" * 40
        return border + "\n" + result + "\n" + border
    return wrapper


# =====================================================================
# PART 2: THE INCIDENT REPORT CLASS
# =====================================================================

class IncidentReport:
    """An incident report made up of a case id and a list of findings."""

    # CLASS VARIABLE - shared by ALL IncidentReport objects.
    # Stores reusable playbooks (list of expected finding titles).
    playbooks = {}

    def __init__(self, case_id, analyst="Unassigned"):
        self.case_id = case_id
        self.analyst = analyst
        self.findings = []          # list of (title, detail) pairs

    # CLASSMETHOD 1 - saves a playbook shared by the whole class
    @classmethod
    def add_playbook(cls, name, finding_titles):
        cls.playbooks[name] = finding_titles
        print(f"Playbook '{name}' saved with findings: {finding_titles}")

    # CLASSMETHOD 2 (Alternate Constructor) - builds a report
    # directly from an already saved playbook.
    @classmethod
    def create_from_playbook(cls, playbook_name, case_id, analyst="Unassigned"):
        new_report = cls(case_id, analyst)
        for title in cls.playbooks[playbook_name]:
            new_report.log_finding(title, "pending investigation")
        return new_report

    def log_finding(self, title, detail):
        self.findings.append((title, detail))

    def update_finding(self, title, detail):
        """Update the detail of a finding that already exists."""
        for i in range(len(self.findings)):
            if self.findings[i][0] == title:
                self.findings[i] = (title, detail)
                return True
        return False

    # Wrapped with TWO decorators. Decorators apply bottom-up:
    #   1. add_border runs first -> adds the '=' lines
    #   2. tag_alert runs next -> adds [ALERT] markers
    @tag_alert
    @add_border
    def summary(self):
        return f"Case: {self.case_id} | Analyst: {self.analyst} | Findings: {len(self.findings)}"

    # =================================================================
    # MAGIC METHODS
    # =================================================================

    def __str__(self):
        # Called automatically when we do: print(report_object)
        text = f"INCIDENT REPORT: {self.case_id} (Analyst: {self.analyst})\n"
        for title, detail in self.findings:
            text += f" - {title}: {detail}\n"
        return text

    def __len__(self):
        # Called automatically when we do: len(report_object)
        return len(self.findings)

    def __getitem__(self, index):
        # Called automatically when we do: report_object[0]
        return self.findings[index]

    def __add__(self, other):
        # Called automatically when we do: report1 + report2
        combined = IncidentReport(self.case_id + " + " + other.case_id, self.analyst)
        combined.findings = self.findings + other.findings
        return combined

    def __eq__(self, other):
        # Called automatically when we do: report1 == report2
        return self.case_id == other.case_id and self.findings == other.findings


# =====================================================================
# PART 3: DEMO CODE
# =====================================================================
if __name__ == "__main__":

    # ---- Using classmethod to save a playbook ----
    IncidentReport.add_playbook("phishing", ["Suspicious sender", "Malicious link", "User action taken"])

    # ---- Using classmethod as an alternate constructor ----
    r1 = IncidentReport.create_from_playbook("phishing", "CASE-101", "SANKY")
    r1.update_finding("Suspicious sender", "Spoofed domain mimicking IT support")
    r1.update_finding("Malicious link", "Credential harvesting page")
    r1.update_finding("User action taken", "User reset password immediately")

    # ---- Creating a second report normally ----
    r2 = IncidentReport("CASE-102", "SANKY")
    r2.log_finding("Unusual login", "Login from unrecognized country")

    # ---- Magic methods in action ----
    print("---- print(r1) uses __str__ ----")
    print(r1)

    print("---- len(r1) uses __len__ ----")
    print(len(r1))

    print("---- r1[0] uses __getitem__ ----")
    print(r1[0])

    print("---- r1 + r2 uses __add__ ----")
    combined = r1 + r2
    print(combined)

    print("---- r1 == r1 uses __eq__ ----")
    print(r1 == r1)

    # ---- Decorators in action ----
    print("---- summary() with @tag_alert and @add_border decorators ----")
    print(r1.summary())