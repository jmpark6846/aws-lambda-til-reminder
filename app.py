# -*- coding:utf-8 -*-
import random
from chalice import Chalice
from github import Github
from chalicelib import secret

app = Chalice(app_name='til-reminder')

@app.route('/')
def reminder():
  # github connection 
  g = Github(secret.account['id'], secret.account['password'])
  repo = g.get_repo('jmpark6846/til')

  file = pick_random_markdown_file_in_repo(repo)
#   content = str(file.decoded_content, encoding='utf-8')
  return { 'path' : file.path }


def pick_random_markdown_file_in_repo(repo, path='/'):
  file_contents = repo.get_file_contents(path=path)
  
  if isinstance(file_contents, list) : # 폴더 인 경우 폴더 내에서 재탐색
    return pick_random_markdown_file_in_repo(repo, "/" + random.choice(file_contents).path)
  elif file_contents.name.split('.')[-1] != 'md' or file_contents.name.lower() == 'readme.md': # 다른 확장자 혹은 리드미 파일 인 경우 상위 디렉토리에서 재탐색
    return pick_random_markdown_file_in_repo(repo, '/')
  else:
    return file_contents
# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
