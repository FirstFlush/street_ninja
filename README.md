
Street Ninja is an SMS-based app designed to help homeless individuals in vulnerable situations access critical resources like food, shelter, drinking fountains, toilets, and free WiFi. Built with simplicity and practicality in mind, it provides real-time, location-based assistance to users via text messages.

---

## How It Works

1. **User Interaction**:
   - A user sends an SMS to the Street Ninja number (powered by Twilio).
   - Example: `"FOOD pender"` or `"SHELTER Main St."`

2. **Processing Requests**:
   - The system parses the message and determines the requested resource.
   - It queries databases (e.g., OpenData API, WiGLE, internal sources) for relevant results.

3. **Response**:
   - Street Ninja sends a formatted SMS with the requested information.
   - Example: `"Closest meal: UGM, 601 Hastings, free lunch 11:30-1:30."`

---

## Goals

- **Immediate Usefulness**: Provide fast, actionable information with no judgment or complexity.
- **Local Impact**: Focus on serving Vancouver’s Downtown Eastside community initially.
- **Scalability**: Build a framework that can expand to other cities over time.

---

## Philosophy

- Street Ninja belongs to the street people. It is built with the understanding that being homeless is like having a full-time job—always on the go, always needing to navigate immediate challenges. This app isn’t about deciding what’s “best” for its users; it’s about meeting them where they are and giving them the tools they need, on their terms.

- Our guiding principle is **immediate usefulness**. Street Ninja focuses on providing quick, actionable information that users can rely on in the moment. There’s no judgment, no lectures—just practical help. Whether it’s finding a meal, a bed, or something else that helps them get through the day, Street Ninja is their tool.

---

## Current Challenges

1. **Data Collection**:
   - Ensuring up-to-date info on free food, shelters, washrooms, drinking fountains, public WiFi.
2. **Funding**:
   - Covering SMS costs via grants, sponsorships, and partnerships.
3. **Technical Setup**:
   - Scaling APIs and handling concurrent user requests.

---

## Roadmap

1. Launch MVP.
2. Partner with local nonprofits for accurate resource data.
3. Expand features to include hygiene access and job listings.
4. Test and refine SMS workflows based on user feedback.

---

## How to Contribute

- **Developers**: Fork the repository and submit pull requests for new features.
- **Nonprofits**: Partner with us to provide up-to-date resource information.
- **Supporters**: Help cover SMS costs by sponsoring or donating.

---

## License

Street Ninja is licensed under the MIT License. See `LICENSE` for more information.

---

## Contact

For inquiries, partnerships, or contributions, contact Michael Pearce at: firstflush@protonmail.com
