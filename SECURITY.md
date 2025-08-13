# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of GPT Gulp seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please send an email to [security@github.com] with the following information:

- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit the issue

### Response Timeline

- We will acknowledge receipt of your vulnerability report within 2 business days
- We will provide a detailed response within 7 business days indicating next steps
- We will notify you when the vulnerability has been fixed

### Safe Harbor

We support safe harbor for security researchers who:

- Make a good faith effort to avoid privacy violations, destruction of data, and interruption or degradation of our services
- Only interact with accounts you own or with explicit permission of the account holder
- Do not access, modify, or delete data belonging to others
- Contact us at the email above to report vulnerabilities

We will not pursue legal action against researchers who follow these guidelines.

## Security Best Practices

When using GPT Gulp:

### Data Privacy

- All conversation data is stored locally by default
- Review configuration files before sharing
- Use environment variables for sensitive paths
- Regularly audit exported conversations for sensitive information

### File System Security

- GPT Gulp monitors file system changes - ensure proper permissions
- Review file paths in configuration
- Use dedicated directories for conversation storage

### Network Security

- Browser extension communicates locally only
- No external API calls by default
- Review any custom integrations

### Configuration Security

- Store configuration files with appropriate permissions
- Use relative paths where possible
- Avoid hardcoding sensitive information

## Reporting Non-Security Issues

For non-security related issues, please use our [GitHub Issues](https://github.com/MarkOpalski/gpt-gulp/issues).
