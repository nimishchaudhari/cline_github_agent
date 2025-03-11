import os
from flask import Flask, request, jsonify
import anthropic
from github import Github
import difflib
import re

app = Flask(__name__)

# Initialize AI client (API key should be set via environment variable)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route('/process-issue', methods=['POST'])
def process_issue():
    data = request.get_json()
    repo_name = data['repository']
    issue_number = data['issue_number']
    issue_title = data['issue_title']
    issue_body = data['issue_body']
    comment = data['comment']
    github_token = data['github_token']

    # Authenticate with GitHub
    g = Github(github_token)
    repo = g.get_repo(repo_name)

    # Example file access - implement dynamic path resolution based on issue
    file_path = "main.js"
    file = repo.get_contents(file_path)
    original_content = file.decoded_content.decode('utf-8')

    # Construct AI prompt
    prompt = f"""
    Issue #{issue_number}: {issue_title}
    Description: {issue_body}
    Comment: {comment}
    File content:
    ```{file_path}
    {original_content}
    ```
    Provide a solution with code modifications and explanation.
    """

    # Get AI response
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse AI response
    ai_response = response.content[0].text
    new_content = ai_response.split("```")[1].strip()
    explanation = ai_response.split("```")[2].strip()

    # Generate diff
    diff = ''.join(difflib.unified_diff(
        original_content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile=f"a/{file_path}",
        tofile=f"b/{file_path}"
    ))

    return jsonify({
        "changes": diff,
        "comment": f"Proposed solution: {explanation}"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
