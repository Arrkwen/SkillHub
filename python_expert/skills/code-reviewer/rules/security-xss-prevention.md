---
title: XSS Prevention
impact: CRITICAL
category: security
tags: xss, security, html, django, fastapi
---

# Cross-Site Scripting (XSS) Prevention

Do not place unsanitized user input into HTML. Django templates and any other HTML renderer must keep auto-escaping on. A FastAPI app that returns JSON does not build HTML from that input.

## Why This Matters

XSS runs an attacker's script in another user's browser. That can steal session cookies, rewrite the page, or submit actions as the victim.

## ❌ Incorrect

```python
# Django: treats user input as trusted HTML
return mark_safe(request.GET["q"])

# Django template
# <h1>Results for {{ query|safe }}</h1>
# {% autoescape off %}{{ query }}{% endautoescape %}

# FastAPI: reflects input into an HTML body
return HTMLResponse(f"<h1>Results for {query}</h1>")
```

## ✅ Correct

```django
{# Escaped by default. Do not add |safe for user content. #}
<h1>Results for {{ query }}</h1>
```

```python
# FastAPI JSON response. The client renders it as data.
return {"query": query}
```

If the service must serve HTML, use a template with auto-escaping left on. Sanitize user HTML only when rich text is an explicit requirement, and do not mark the result safe unless that sanitizer is the one the project already trusts.

A pure JSON API still has HTML on error pages and docs. Those pages follow the same rule: no string-built HTML from request data.

## Checklist

- [ ] Django templates do not use `|safe`, `mark_safe`, or `autoescape off` on user-controlled values
- [ ] FastAPI handlers that accept user input return JSON or an escaped template, not an f-string `HTMLResponse`
- [ ] Uploaded HTML or SVG is not served inline from a static directory
- [ ] HTML responses that include user content send a Content-Security-Policy

## References

- [Django security: cross site scripting](https://docs.djangoproject.com/en/stable/topics/security/#cross-site-scripting-xss-protection)
- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
