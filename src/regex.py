import re

standard = r"((?:[a-zA-Z]|\.){2,})"
username = standard

domain = r"((?:[a-zA-Z]|\.)+\w+)"
dot_domain = r"(?: dot | dt |\.|\;)" + domain

extension = r"((?:[a-zA-Z]|\.)+(?:\w|\;)+)"
dot_extension = r"(?: dot | dt |\.|\;)" + extension

end_email = r"(?:(?!(dot|dt)).)*(?<!\;)$"

email_patterns = [
    (
        re.compile(username + r"\s*(?:\(at\)|@|&#x40;|\(followed by.*@)\s*" + domain),
        "{0}@{1}",
    ),
    (
        re.compile(username + r" at " + domain + dot_extension + end_email),
        "{0}@{1}.{2}",
    ),
    (
        re.compile(
            username + r" at " + domain + dot_domain + dot_extension + end_email
        ),
        "{0}@{1}.{2}.{3}",
    ),
    (
        re.compile(username + r" WHERE " + domain + r" DOM " + domain),
        "{0}@{1}.{2}",
    ),
    (
        re.compile(r"obfuscate\('" + domain + "','" + username),
        "{1}@{0}",
    ),
]

phone_format = "{0}-{1}-{2}"

phone_patterns = [
    re.compile(r"(\d{3})(?:-|&thinsp;|s+)(\d{3})(?:-|&thinsp;|s+)(\d{4})"),
    re.compile(r"\((\d{3})\)\s*(\d{3})(?:-|s+)(\d{4})"),
]


def extract(fileName, line):
    emails = extract_emails(fileName, line)
    phones = extract_phones(fileName, line)

    return emails + phones


def extract_emails(fileName, line):
    emails = []
    for (pat, fmt) in email_patterns:
        matches = re.findall(pat, line)
        for m in matches:
            emails.append((fileName, "e", fmt.format(*m)))

    return emails


def extract_phones(fileName, line):
    phones = []
    for pat in phone_patterns:
        matches = re.findall(pat, line)
        for m in matches:
            phones.append((fileName, "p", phone_format.format(*m)))

    return phones
