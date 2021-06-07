from flask import Flask
import requests
import json

app = Flask(__name__)

@app.route('/api/stars', methods=['GET'])
def get_star_ranks():
    # query highest starred repos from github api
    response = requests.get('https://api.github.com/search/repositories?q='
                            'stars:>0&sort=stars')
    if response.status_code == 200:
        # filter top 10 if query successful
        json_data = json.loads(response.text)
        repos = json_data['items'][:10]

        # filter owner name, avatar and # of stars
        ranks = []
        for repo in repos:
            ranks += [{'name': repo['owner']['login'], 
                    'avatar': repo['owner']['avatar_url'],
                    'score': repo['stargazers_count']}]

        return json.dumps(ranks)
    else:
        raise ValueError('Failed to retrieve star ranks')

@app.route('/api/forks', methods=['GET'])
def get_fork_ranks():
    # collect top 10 most forked repos from github api
    response = requests.get('https://api.github.com/search/repositories?q='
                            'forks:>0&sort=forks')
    if response.status_code == 200:
        # filter top 10 if query successful
        json_data = json.loads(response.text)
        repos = json_data['items'][:10]

        # filter owner name, avatar and # of forks
        ranks = []
        for repo in repos:
            ranks += [{'name': repo['owner']['login'], 
                    'avatar': repo['owner']['avatar_url'],
                    'score': repo['forks']}]

        return json.dumps(ranks)
    else:
        raise ValueError('Failed to retrieve fork rank')

if __name__ == '__main__':
    app.run(debug=True)