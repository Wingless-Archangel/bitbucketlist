import requests
import urllib.parse
URL = "https://api.bitbucket.org/2.0/repositories?role=member&pagelen=100"
HEADERS = {'content-type': 'application/json'}
REPO_LIST = {}

def main():
    """make the api to Bitbucket, TODO remove hardcoded secrets """
    global URL

    while True:
        next_result = ''
        response_list = api_call(URL)
        result_list = response_list['values']
        parse_result(result_list)


        try:
            next_result = urllib.parse.unquote(response_list['next'])
            print(f"Next URL is {next_result}")

            if next_result == '' or next_result == URL:
                break

            URL = next_result

        except KeyError as err:
            print(f"Error : {err} is missing")
            break

    with open('result.csv', 'w') as file:
        file.write("repository, created on, last updated\n")
        for repo, date in REPO_LIST.items():
            file.write(f"{repo}, {date[0]}, {date[1]}\n")


def api_call(conn):
    req = requests.get(conn, headers=HEADERS, auth=('user', 'pass'))
    result = req.json()
    return result


def parse_result(result_list):
    """result is in the list format so we need to iterate to get the interesting information """

    for result in result_list:
        REPO_LIST[result['full_name']] = [result['created_on'], result['updated_on']]


if __name__ == '__main__':
    main()
