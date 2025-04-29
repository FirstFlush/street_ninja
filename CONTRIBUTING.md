# Contributing to Street Ninja

Thanks for your interest in **Street Ninja** — a text-based tool that helps people on the street quickly find food, shelter, jobs, and other essential resources. Contributions are welcome, but please note: the project’s biggest challenges right now are *not just technical*. Getting the word out, improving our data, and securing funding are just as important as writing code.

If you want to help, we’d love to hear from you.

---

## 🔧 How to Contribute

### 1. **Browse the Issues**
- Look for [`help wanted`](https://github.com/FirstFlush/street_ninja/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) or [`good first issue`](https://github.com/FirstFlush/street_ninja/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).
- Comment to claim an issue or ask questions.

### 2. **Share Ideas**
- If you have a feature suggestion or want to improve something, open a [discussion](https://github.com/FirstFlush/street_ninja/discussions).
- We're especially open to:
  - Smarter location parsing
  - Better ways to display results in under 320 characters
  - Low-tech ideas for reaching people who don’t use the app yet

### 3. **Non-Code Help Needed**
- **Outreach** – Street Ninja needs allies: nonprofits, shelters, service workers, and people with lived experience.
- **Funding** – Help us apply to grants or spread the word to potential donors.
- **Data** – Know of a food bank or shelter not listed? Open an issue or PR.

---

## 🧠 Development Notes

### Tech Stack
- **Backend**: Python 3.10+, Django REST Framework, GIS
- **Database**: Postgres
- **SMS**: Twilio
- **Caching**: Redis
- **Frontend**: [Next.js (separate repo)](https://github.com/FirstFlush/website_street_ninja)

### Guidelines
- Keep pull requests small, focused, and aligned with Street Ninja’s vision: **immediate usefulness**.
- If in doubt, open a draft PR or discussion first.

### Testing
- We use `pytest-django`. Not all modules are tested yet, but we’re working toward full coverage. You’re welcome to help.

---

## ✅ Pull Request Process

1. Fork the repo, create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Commit and push:
   ```bash
   git commit -m "Add: description"
   git push origin feature/your-feature-name
   ```
3. Open a pull request. Include:
   - What the change does
   - Why it matters
   - Any caveats or follow-ups

---

## 💬 Questions?

Open a [discussion](https://github.com/FirstFlush/street_ninja/discussions) or reach out to Michael Pearce at michaelpearce@streetninja.ca
