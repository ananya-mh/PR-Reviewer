# PR Reviewer Bot

This is a Python-based project that uses Flask to handle GitHub pull request events via webhooks. It posts automated comments to pull requests when they are opened and integrates with a code linting service to provide feedback on PR files.

## Features

- **Webhook Integration**: Responds to pull request events (PR opened) from GitHub.
- **Automated Comments**: Posts a thank you comment to the pull request when opened.
- **Code Linting**: Integrates `pylint` for reviewing the code in pull requests and generating linting reports.
- **AI Integration**: Utilize models like CodeLlama for analyzing or suggesting improvements to code in pull requests.

## Setup

### Prerequisites

- Python 3.x+
- GitHub Personal Access Token (for interacting with GitHub API)
- Required libraries (listed in `requirements.txt`)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/PR-Reviewer.git
   cd PR-Reviewer
