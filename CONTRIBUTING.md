# Contributing to Wish Wall

Thank you for your interest in contributing to Wish Wall! We welcome contributions from the community to help improve this project.

## Code of Conduct

Please be respectful and constructive in all interactions with other contributors. We are committed to providing a welcoming and inclusive environment for all.

## How to Contribute

### Reporting Bugs

If you encounter a bug, please create an issue with:
- A clear, descriptive title
- A detailed description of the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python/Node version, etc.)
- Screenshots or error logs if applicable

### Suggesting Enhancements

We love feature suggestions! Please create an issue with:
- A clear title describing the feature
- A detailed description of the proposed enhancement
- Use cases and benefits
- Any additional context or examples

### Submitting Pull Requests

1. **Fork the repository** and create a new branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards:
   - Write clean, readable code
   - Add comments for complex logic
   - Follow existing code style and conventions
   - Write tests for new functionality

3. **Test your changes**
   - Run existing tests to ensure nothing is broken
   - Add new tests for your changes
   - Verify your changes work as expected

4. **Commit your changes**
   ```bash
   git commit -m "Brief description of changes"
   ```
   - Use clear, meaningful commit messages
   - Reference issues when applicable (e.g., "Fixes #123")

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Provide a clear title and description
   - Link related issues
   - Include screenshots or examples if relevant
   - Ensure all CI checks pass

## Development Setup

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Backend Development

```bash
cd backend
bash start.sh
```

## Coding Standards

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for functions and classes
- Format with `black` or similar tool

### JavaScript/Vue (Frontend)
- Use ES6+ syntax
- Follow Vue 3 best practices
- Use meaningful variable and function names
- Add JSDoc comments for complex functions
- Run linter: `npm run lint`

## Testing

- Write unit tests for new features
- Ensure test coverage doesn't decrease
- Run tests before submitting PR

## Documentation

- Update README.md for user-facing changes
- Update comments and docstrings for code changes
- Update CONTRIBUTING.md if contribution process changes

## Getting Help

Have questions? Feel free to:
- Open an issue with the "question" label
- Check existing issues and discussions
- Contact the maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to Wish Wall! 🎉
