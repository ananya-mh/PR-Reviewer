from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# GitHub token (to authenticate API requests)
GITHUB_TOKEN = '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'

# Your repository name and owner (from GitHub)
REPO_OWNER = 'ananya-mh'
REPO_NAME = 'PR-Reviewer'


@app.route('/webhook', methods=['POST'])
def handle_pr():
    # Get the payload from the webhook
    data = request.json
    
    # Check if this is a pull request event
    if data.get('action') == 'opened' and 'pull_request' in data:
        pr_title = data['pull_request']['title']
        pr_url = data['pull_request']['html_url']
        
        # Post a comment on the PR
        comment = f"Thanks for your PR: {pr_title}! We will review it soon. {pr_url}"
        pr_number = data['pull_request']['number']
        
        # Send the comment to the GitHub API
        comment_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{pr_number}/comments'
        headers = {'Authorization': f'token {GITHUB_TOKEN}'}
        payload = {'body': comment}
        
        response = requests.post(comment_url, json=payload, headers=headers)
        
        if response.status_code == 201:
            return jsonify({'message': 'Comment posted successfully!'}), 201
        else:
            return jsonify({'error': 'Failed to post comment.'}), 500
    return jsonify({'message': 'Not a PR opened event.'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
