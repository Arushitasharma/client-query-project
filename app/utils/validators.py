import re


# USERNAME VALIDATION
def validate_username(username):

    if len(username) < 4 or len(username) > 15:

        return (
            False,
            "Username must be between 4 and 15 characters"
        )

    if " " in username:

        return (
            False,
            "Username cannot contain spaces"
        )

    if not username.isalnum():

        return (
            False,
            "Username must contain only letters and numbers"
        )

    return True, ""


# PASSWORD VALIDATION
def validate_password(password):

    if len(password) < 6:

        return (
            False,
            "Password must be at least 6 characters long"
        )

    if not re.search(r"[A-Z]", password):

        return (
            False,
            "Password must contain an uppercase letter"
        )

    if not re.search(r"[a-z]", password):

        return (
            False,
            "Password must contain a lowercase letter"
        )

    if not re.search(r"\d", password):

        return (
            False,
            "Password must contain a number"
        )

    return True, ""


# QUERY TITLE VALIDATION
def validate_query_title(title):

    if len(title.strip()) < 5:

        return (
            False,
            "Query title is too short"
        )

    if len(title.strip()) > 100:

        return (
            False,
            "Query title is too long"
        )

    return True, ""


# QUERY MESSAGE VALIDATION
def validate_query_message(message):

    if len(message.strip()) < 10:

        return (
            False,
            "Query description is too short"
        )

    return True, ""