![Street Ninja logo](logo.png)

# Street Ninja [![LIVE](https://img.shields.io/badge/status-LIVE-brightgreen)](https://streetninja.ca)

**🚧 Street Ninja is live and improving.**  
We continue to refine the system and welcome feedback to help it better serve people on the street.

Street Ninja is an SMS-based app that helps homeless people in Vancouver access critical resources like **food**, **shelter**, **drinking fountains**, **toilets**, and **free WiFi**. It’s fast, practical, and works from any phone that can send a text—no app, no data, no hassle.

Try it: [streetninja.ca](https://streetninja.ca/try-it-out)


## How It Works

1. **Send a text**  
   Example:  
   - `FOOD 222 main st`  
   - `SHELTER main & hastings`  
   - `kitsilano toilet`

2. **Street Ninja parses your message**  
   - It figures out what resource you need and where you are.
   - Handles typos, slang, and weird phrasing with a custom rule-based parser.

3. **You get a list of results, ordered by what's closest to you**  
   Street Ninja replies with the closest options and what they offer.  

   Example response for inquiry `food 222 main st`:  
   ```
   FOOD PROGRAMS
   1) 0km Food on the Corner: meals (Free) 

   2) 0.1km La Boussole - Foodbank: hampers (Free) 

   3) 0.1km Salvation Army - Harbour Light, Meal Program: meals (Free) 

   4) 0.2km Muslim Care Centre - Meal Program: meals (Free), takeout 

   More? 'MORE' | Help? 'HELP'
   Details? '# INFO' | Maps? '# DIRECTIONS'
   ```

4. **Follow-up inquiries**  
   - Reply `INFO` to get more details  
   - Reply `MORE` to see more options  
   - Reply `DIRECTIONS` to get walking directions

   Users can reply with `MORE` to see more results, or ask for `INFO` or `DIRECTIONS` about a specific one (e.g., `3 INFO` for more information about the Salvation Army's Harbour Light meal program).


## Technical Overview

Street Ninja is a full-stack system designed for speed, fault tolerance, and real-world usage. Key components:

- **Backend**: Django REST Framework with PostGIS for geospatial filtering
- **Frontend**: [Next.js + Tailwind CSS](https://github.com/firstflush/website_street_ninja) — responsive site for trying out the SMS experience
- **Location Parsing**: Custom rule engine to extract locations from freeform text
- **SMS Gateway**: Twilio integration with webhook authentication
- **Session Cache**: Redis to support multi-step conversations via follow-ups (`INFO`, `MORE`, etc.)
- **Task Queue**: Celery + Celery Beat for async tasks and scheduled jobs (e.g., periodic resource sync)
- **Containerized**: Docker setup with PostgreSQL + Redis + Gunicorn
- **CI/CD**: CI pipeline with GitHub Actions to run tests using pytest


## Hire Me

I'm currently looking for remote developer roles: full-time, contract, or part-time.

I took Street Ninja from idea to production, including system architecture, branding, logo concept, infrastructure, testing, and deployment. This project reflects not just my code, but my judgment, initiative, and follow-through.

If you're looking for someone who can design, build, and ship real software for real users, I'm available and would love the opportunity to work. Street Ninja is live, and I’m proud of what it represents: practical tools that solve real problems. 

✉️ [Email](mailto:michaelpearce@streetninja.ca)
🔗 [LinkedIn](https://www.linkedin.com/in/michael-pearce-340279286/)
🌐 [Portfolio](https://michaelpearce.tech)


## Why SMS?

Most street folks don’t have reliable access to data plans or app stores. But many have basic phones with texting capabilities. Street Ninja is built around that reality:  
- No app to download  
- No login or tracking  
- No judgment—just help


## Philosophy

- Street Ninja belongs to the street people. It is built with the understanding that being homeless is like having a full-time job—always on the go, always needing to navigate immediate challenges. This app isn’t about deciding what’s “best” for its users; it’s about meeting them where they are and giving them the tools they need.

- The guiding principle is **immediate usefulness**. Street Ninja focuses on providing quick, actionable information that users can rely on in the moment.


## Service Area

Right now, Street Ninja operates in **Vancouver, BC**—especially around the Downtown Eastside.  
I'm hoping to expand the program to other cities once it proves effective in Vancouver.


## What’s Ahead

- **Expanding Resource Types**:  
  We want to go beyond food and shelter—to include medical care, legal help, clothing programs, hygiene access, and more. The goal is to make Street Ninja a true pocket guide to anyone who's down and out.

- **Building Data Partnerships**:  
  We're looking to connect with organizations that have reliable info on essential services—especially medical clinics, legal help, clothing programs, and hygiene resources. The more accurate and deep the data, the more useful Street Ninja becomes.

- **Securing Sustainable Funding**:  
  We’re exploring ways to cover SMS and hosting costs long-term—whether through grants, sponsorships, or community support. The system is lean and already live; the right support can help it grow.


## How to Contribute

- **Developers**: See [CONTRIBUTING.md](CONTRIBUTING.md)  
- **Nonprofit Folks**: I’m a dev, not a nonprofit person. If you know the nonprofit industry and can help with navigating issues like funding or outreach, I'd really like to hear from you.


## 🕸 Street Ninja Ecosystem

- [Streetlight API](https://github.com/FirstFlush/streetlight-api) — Public API for homelessness resources (UNDER CONSTRUCTION)
- [Ninja Crawl](https://github.com/FirstFlush/ninja_crawl) — Python-based scraping engine (HTML/PDF → JSON)
- [Street Ninja SMS App (you are here)](https://github.com/FirstFlush/street_ninja) — SMS assistant for accessing resources by text
- [Street Ninja Website](https://github.com/FirstFlush/website_street_ninja) — Try out the SMS assistant and explore the project


## License

Street Ninja is open source under the Apache License 2.0.  
See [`LICENSE`](LICENSE) for full details.


## ☕ Support Street Ninja

Street Ninja is fully self-hosted and independently maintained.
If you’d like to support the project, [buy me a coffee](https://www.buymeacoffee.com/firstflush).


---


Built by [Michael Pearce](mailto:michaelpearce@streetninja.ca) • Founder & Lead Developer  
[michaelpearce.tech](https://michaelpearce.tech)