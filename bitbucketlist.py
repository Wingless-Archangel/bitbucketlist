import requests
import urllib.parse
import json

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
        print(REPO_LIST)

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
        file.write("repository, language, size, created on, last updated\n")
        for key, value in REPO_LIST.items():
            file.write(f"{key}, {value[0]}, {value[1]}, {value[2]}, {value[3]}\n")

    print(json.dumps(REPO_LIST))

    # with open('test_result.json', 'w') as file:
    #     file.write(REPO_LIST)


def api_call(conn):
    req = requests.get(conn, headers=HEADERS, auth=('user', 'pass'))
    result = req.json()
    return result


def parse_result(result_list):
    """result is in the list format so we need to iterate to get the interesting information """

    for result in result_list:
        REPO_LIST[result['full_name']] = [result['language'], result['size'], result['created_on'], result['updated_on']]


if __name__ == '__main__':
    main()
