from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
# GitHub token (to authenticate API requests)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
CLASSIC_TOKEN = os.getenv("CLASSIC_TOKEN")
print('Classic', CLASSIC_TOKEN)

# Your repository name and owner (from GitHub)
REPO_OWNER = 'ananya-mh'
REPO_NAME = 'PR-Reviewer'


@app.route('/webhook', methods=['POST'])
def handle_pr():
    data = request.json
    print("Received webhook payload:")
    print(data)

    # Check if this is a pull request event
    if data.get('action') == 'opened' and 'pull_request' in data:
        pr_title = data['pull_request']['title']
        pr_url = data['pull_request']['html_url']
        pr_number = data['pull_request']['number']
        author = data['pull_request']['user']['login']
        pr_branch = data['pull_request']['head']['ref']

        # Add this line to log specific PR info
        print(f"New PR opened: #{pr_number} '{pr_title}' by {author}")
        print(f"🔗 PR URL: {pr_url}")

        # Post a comment
        comment = f"Thanks for your PR: {pr_title}! We will review it soon. {pr_url}"
        comment_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{pr_number}/comments'
        headers = {'Authorization': f'token {CLASSIC_TOKEN}'}
        payload = {'body': comment}

        response = requests.post(comment_url, json=payload, headers=headers)

        if response.status_code == 201:
            print("Comment posted successfully!")
            # return jsonify({'message': 'Comment posted successfully!'}), 201
        else:
            print("Failed to post comment.")
            print("Status:", response.status_code)
            print("Response:", response.text)
            print(headers)
            return jsonify({'error': 'Failed to post comment.'}), 500
        
        changed_files = get_pr_files(REPO_OWNER, REPO_NAME, pr_number, CLASSIC_TOKEN)
        for file in changed_files:
            filename = file['filename']
            print(f"Opened file: {filename}")

            content_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filename}?ref={pr_branch}"
            headers = {
                "Authorization": f"token {CLASSIC_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }

            file_response = requests.get(content_url, headers = headers)
            if file_response.status_code == 200:
                content_data  = file_response.json()
                if content_data.get('encoding') == 'base64':
                    import base64
                    decoded_content = base64.b64decode(content_data['content']).decode('utf-8')
                    directory = os.path.dirname(f"saved_pr_files/{filename}")
                    if directory:
                        os.makedirs(directory, exist_ok=True)
                    with open(f"saved_pr_files/{filename}", 'w', encoding = 'utf-8') as f:
                        f.write(decoded_content)
                    print(f"Saved {filename}")
    

    print("Not a PR 'opened' event.")
    return jsonify({'message': 'Not a PR opened event.'}), 200

def get_pr_files(repo_owner, repo_name, pr_number, token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
