# Contributing to [Project Name]

Welcome to the [Project Name] repository! Since we are working as a team of ~ 15 collaborators, we will be pushing branches directly to the main repository and using pull requests for code reviews and integration. Please follow these guidelines to ensure a smooth and efficient workflow.

## Workflow

### Creating a New Branch


1. **Sync with Main Branch:** Before creating a new branch, ensure your local main branch is up-to-date with the remote repository.

```bash
git checkout main
git pull origin main
```

2. **Create a New Branch:** Create a new branch for your changes. Use a descriptive name for your branch that reflects the nature of your work (e.g., fix-typo-in-readme or add-login-feature).

```bash
git checkout -b <branch-name>
```

### Making Changes

1. **Implement Your Changes:** Make your changes in the new branch. Follow the project's coding standards and best practices.

2. **Test Your Changes:** Run all relevant tests to ensure your changes do not introduce new issues or break existing functionality.

### Committing and Pushing

1. **Commit Your Changes:** Write clear and concise commit messages. Use the format: `[TYPE]: Brief description` (e.g., `Fix: Correct typo in README`).

```bash
git add .
git commit -m "Your commit message"
```

2. **Push to Remote:** Push your branch to the remote repository.

```bash
git push origin <branch-name>
```

### Creating a Pull Request

1. **Open a Pull Request:** Go to the Pull Requests section of the repository and create a new pull request from your branch.

2. **Provide Details:** In the pull request description, provide a summary of the changes, link to any relevant issues, and explain any additional context necessary for review.

3. **Assign Reviewers:** Assign at least one other team member as a reviewer for your pull request.

### Code Review

1. **Review Guidelines:** When reviewing pull requests, check that the code adheres to the project’s coding standards, is well-documented, and does not introduce new bugs.

2. **Provide Constructive Feedback:** Offer constructive feedback and suggestions for improvement. Be clear and respectful in your comments.

3. **Approve or Request Changes:** Approve the pull request if everything looks good, or request changes if further modifications are needed.

### Coding Standards

1. **Code Style:** Try your best to adhere to best practices outlined in the [Python Style Guide](https://peps.python.org/pep-0008/) and to the [Zen of Python](https://peps.python.org/pep-0020/).

2. **Documentation:** Ensure your code is well-documented with comments and that any new features or changes are reflected in the documentation.

### Testing

1. **Run Tests:** Ensure all tests pass before submitting a pull request. Add new tests if your changes introduce new functionality or modify existing behavior.

2. **Maintain Test Coverage:** Strive to maintain or improve test coverage as appropriate.


Thank you for contributing to [Project Name]!
