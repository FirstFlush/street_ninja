# Street Ninja [![In Development](https://img.shields.io/badge/status-IN%20DEVELOPMENT-yellow)](https://github.com/your-repo-link)

**⚠️ This project is currently in active development. Features and documentation are subject to change as we work towards the first MVP release.**

Street Ninja is an SMS-based app designed to help homeless individuals in the city of Vancouver access critical resources like food, shelter, drinking fountains, toilets, and free WiFi. Built with simplicity and practicality in mind, it provides real-time, location-based assistance to users via text messages.

## How It Works

1. **User Interaction**:
   - A user sends an SMS to the Street Ninja number (powered by Twilio).
   - Example: `"FOOD pender st"` or `"SHELTER Main & Hastings"` or `"WIFI oppenheimer park"` 

2. **Processing Requests**:
   - The system parses the message and determines the requested resource.
   - It queries databases (e.g., OpenData API, WiGLE, internal sources) for relevant results.

3. **Response**:
   - Street Ninja sends a formatted SMS with the requested information.
   - Example: `"Closest meal: UGM, 601 Hastings, free lunch 11:30-1:30."`

## Why SMS?

Many homeless individuals are more likely to have access to a basic phone that can send text messages rather than a smartphone with mobile data. Instead of requiring users to download an app, Street Ninja works instantly—just text the number when you need help. No installation or internet connection required.

## Goals

- **Immediate Usefulness**: Provide fast, actionable information with no judgment or complexity.
- **Local Impact**: Focus on serving Vancouver’s Downtown Eastside community initially.
- **Scalability**: Build a framework that can expand to other cities over time.


## Philosophy

- Street Ninja belongs to the street people. It is built with the understanding that being homeless is like having a full-time job—always on the go, always needing to navigate immediate challenges. This app isn’t about deciding what’s “best” for its users; it’s about meeting them where they are and giving them the tools they need.

- Our guiding principle is **immediate usefulness**. Street Ninja focuses on providing quick, actionable information that users can rely on in the moment. There’s no judgment, no lectures—just practical help. Whether it’s finding a meal, a bed, or something else that helps them get through the day, Street Ninja is their tool.


## Current Challenges

1. **Data Collection**:
   - Ensuring up-to-date info on free food, shelters, washrooms, drinking fountains, public WiFi.
2. **Funding**:
   - Covering SMS costs via grants, sponsorships, and partnerships.
3. **Technical Setup**:
   - Scaling APIs and handling concurrent user requests.


## Roadmap

1. Launch MVP.
2. Partner with local nonprofits for accurate resource data.
3. Expand features to include hygiene access and job listings.
4. Test and refine SMS workflows based on user feedback.


## How to Contribute

- **Developers**: Check out [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines and information.
- **Nonprofits**: Partner with us to provide up-to-date resource information.
- **Supporters**: Help cover SMS costs by sponsoring or donating.


## License

Street Ninja is licensed under the MIT License. See `LICENSE` for more information.


## Contact

For inquiries, partnerships, or contributions, contact Michael Pearce at: firstflush@protonmail.com
