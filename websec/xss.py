"""An encoding library to prevent against XSS. 

Implemented the rules described at OWASP Wiki:
  https://www.owasp.org/index.php/XSS_%28Cross_Site_Scripting%29_Prevention_Cheat_Sheet

Not meant for production use. 

"""

# ---------
# Rule #0 
#
# Use a whitelist approach and neverinsert untrusted data without escaping
# ---------

# ---------
# Rule #1 
#
# HTML 
# ---------

def rule1(char):
    rules = {'&': '&amp;',
             '<': '&lt;',
             '>': '&gt;',
             '"': '&quot;',
             "'": '&#x27;',  # &aops; isn't in the html spec
             '/': '&#x2F;'}
    if char in rules:
        return rules[char]
    return char


def html_escape(text):
    encoded = [rule1(c) for c in text]
    return "".join(encoded)


# --------
# Rule #2
# 
# HTML Attributes
# --------

def rule2(char):
    # HTML, escape to &#xHH
    if not char.isalnum() and ord(char) < 256:
        return '&#x%X' % (ord(char), )
    else:
        return char

def html_attributes_escape(text):
    encoded = [rule2(c) for c in text]
    return "".join(encoded)
    

# --------
# Rule #3
#
# JavaScript
# --------

def rule3(char):
    # JavaScript, escape to \xHH
    if not char.isalnum() and ord(char) < 256:
        return '\x%X' % (ord(char), )
    else:
        return char

def javascript_escape(text):
    encoded = [rule3(c) for c in text]
    return "".join(encoded)

# -----------
# Rule #3.1
#
# JSON in HTML
# ----------

def rule3_1(char):
    return rule1(char)

# ------------
# Rule #4
# 
# CSS (Values only)
# -------------

def rule4(char):
    # CSS, escape to \HH
    if not char.isalnum() and ord(char) < 256:
        return '\%X' % (ord(char), )
    else:
        return char


def css_escape(text):
    # IE has an expression property that allows CSS to run JS (wtf)
    # URLs should only start with http and not javascript.
    # Hard to detect what is an URL, removes 'javascript' and 'expression'
    # but doesn't check here if an url starts with 'http'
    encoded = "".join([rule4(c) for c in text])
    disallowed_words = ["expression", "javascript"]
    for word in disallowed_words:
        if encoded.strip().startswith(word):
            start = encoded.index(word) + len(word)
            text = encoded[start:]
    return encoded


# --------
# Rule #5
#
# URL Escape HTML url parameters
# --------

def rule5(char):
    # URL, to %HH
    if not char.isalnum() and ord(char) < 256:
        return r'%' + '%X' % (ord(char), )
    else:
        return char

def url_escape(text):
    encoded = [rule5(c) for c in text]
    return "".join(encoded)


# Skipped rule #6

# -------
# Rule #7
# 
# DOM based XSS
# -------

# TODO


