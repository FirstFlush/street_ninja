# Contributing to Street Ninja

Thank you for your interest in contributing to **Street Ninja**! This project is currently in **active development**, and while contributions are welcome, it's important to note that the app's direction and architecture are still evolving. Below are some guidelines to help you get started and align your contributions with the project's goals.


## How to Get Involved

1. **Check the Issues**  
   - Review the [issue tracker](https://github.com/FirstFlush/street_ninja/issues) for tasks labeled `help wanted` or `good first issue`. These are areas where contributions are most needed.
   - If you'd like to work on an issue, comment on it to let us know you're taking it on.

2. **Propose New Ideas**  
   - If you have an idea or feature suggestion, please open a **discussion issue** first. This ensures we align your idea with the project's goals before work begins.
   - Include a clear description of the problem you're solving and how your idea fits within Street Ninja's vision.

3. **Code Contributions**  
   - Before submitting a pull request, please ensure:
     - Your changes align with the project's philosophy of **immediate usefulness** and simplicity.
     - The pull request focuses on a single, clearly defined feature or fix.
   - If you're unsure whether your idea fits, feel free to open a draft pull request or reach out for feedback.


## Development Guidelines

1. **Work in Progress**  
   - Parts of the app (e.g., text message parsing) are still being designed and will become clearer as development progresses. Contributions in these areas may be deferred until a clear direction is established.

2. **Coding Standards**  
   - Use **Python 3.10+** and follow [PEP 8](https://peps.python.org/pep-0008/) for style guidelines.

3. **Testing**  
   - Street Ninja does not yet have a full test suite, but testing will be added in the future using pytest-django.


## Help Improve Location Resolution

The **location resolution system** located in sms/resolvers/location is critical—everything in Street Ninja depends on correctly interpreting user locations. Right now, it is functional but needs improvement and testing.

### Why This Matters
1. **The entire app relies on accurate location parsing.** If we misinterpret where a user's request is coming from, we can't properly help them.
2. **Userbase has low tolerance for nonsense.** If "food 155 Hastings St E" works but "food 155 E Hastings" doesn’t, they'll lose trust and stop using the app.

### Where Help Is Needed
- **Better extraction of addresses, intersections, and landmarks** from unstructured text.  
- **Handling street formatting variations** (e.g., "E Hastings" vs. "Hastings St E").  
- **More robust handling of typos, missing words, and mixed formats.**
- **Handling edge cases** "FOOD" and "WATER" are both keywords a user can search for. But how do we handle it when someone is searching for food on Water St?

If you have experience with **parsing, NLP, or fuzzy matching**, or if you just want to brainstorm, your help would make a huge impact. Open an issue or start a discussion if you have ideas!  


## Submitting a Pull Request

1. Fork the repository and create your branch:
   ```
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and commit them:
   ```
   git commit -m "Add: Description of your feature"
   ```
3. Push your branch and submit a pull request:
   ```
   git push origin feature/your-feature-name
   ```
4. Clearly describe:
   - The problem being solved.
   - How your solution aligns with Street Ninja's goals.
   - Any potential limitations or areas for improvement.


## Things to Keep in Mind

- **Focus on the Vision**: Street Ninja aims to provide fast, actionable information to people in need. Keep this principle in mind when contributing.
- **Collaboration First**: Major changes or new features should always be discussed before implementation. This prevents misalignment and wasted effort.
- **Respect the Process**: Contributions that don't fit the current scope may be deferred or rejected—this isn't personal! It's about keeping the project on track.


## Questions?

If you have any questions or need clarification, please reach out by opening a [discussion issue](https://github.com/FirstFlush/street_ninja/discussions) or contacting [Michael Pearce](mailto:firstflush@protonmail.com).
