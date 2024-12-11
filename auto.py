import requests,os
BASE_URL = 'https://api.github.com/users/peme969'
following_url = f'{BASE_URL}/following'
followers_url = f'{BASE_URL}/followers'
GITHUB_TOKEN = os.environ['Github_Token']
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}
def fetch_all(url):
    results = []
    while url:
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            results.extend(response.json())
            url = response.links.get('next', {}).get('url')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            break
    return results
def follow_user(username):
    url = f'https://api.github.com/user/following/{username}'
    try:
        response = requests.put(url, headers=HEADERS)
        if response.status_code == 204:
            print(f'\033[1;32mSuccessfully followed {username}.\033[0m')
        else:
            print(f'\033[1;31mFailed to follow {username}. {response.json()}\033[0m')
    except requests.exceptions.RequestException as e:
        print(f'\033[1;31mError following {username}: {e}\033[0m')
def unfollow_user(username):
    url = f'https://api.github.com/user/following/{username}'
    try:
        response = requests.delete(url, headers=HEADERS)
        if response.status_code == 204:
            print(f'\033[1;32mSuccessfully unfollowed {username}.\033[0m')
        else:
            print(f'\033[1;31mFailed to unfollow {username}. {response.json()}\033[0m')
    except requests.exceptions.RequestException as e:
        print(f'\033[1;31mError unfollowing {username}: {e}\033[0m')
following_data = fetch_all(following_url)
followers_data = fetch_all(followers_url)
following = [user['login'].lower() for user in following_data]  
followers = [user['login'].lower() for user in followers_data] 
not_followers = [user for user in following if user not in followers]
not_following_back = [user for user in followers if user not in following]
for user in not_followers:
    print(f'\033[1;33mYou follow {user}, but they don\'t follow you back.\033[0m')
    unfollow_user(user)
for user in not_following_back:
    print(f'\033[1;36m{user} follows you, but you don\'t follow them back.\033[0m')
    follow_user(user)
print("\033[1;34mProcessing complete!\033[0m")
print(f'\033[1;34m📊 Summary:\033[0m')
print(f'\033[1;33m🔴 {len(not_followers)} user(s) you follow but don\'t follow you back.\033[0m')
print(f'\033[1;36m🟢 {len(not_following_back)} user(s) follow you but you don\'t follow back.\033[0m')
