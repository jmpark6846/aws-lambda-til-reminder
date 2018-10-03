# -*- coding:utf-8 -*-
import random
from chalice import Chalice, Rate, Cron
from github import Github
from chalicelib import secret
import telegram

app = Chalice(app_name='til-reminder')


@app.schedule(Cron(0, 23, '*', '*', '?', '*'))
def reminder(event):
  # github connection 
  print('reminder started')

  g = Github(secret.account['id'], secret.account['password'])
  repo = g.get_repo('jmpark6846/til')
  print('github logged in')

  file = pick_random_markdown_file_in_repo(repo)
  print('pick a random file from repo: ' + file.path)
  
  content = make_content_from_file_metadata(file)
  print('make content from file for telegram bot')

  send_telegram_message(bot_token=secret.telegram_bot['token'], chat_id=secret.telegram_bot['chat_id'], content=content)
  print('telegram message sent')
  
  return { 'to': secret.telegram_bot['chat_id'], 'file' : file.path }


def make_content_from_file_metadata(file):
  category = '/'.join(file.path.split('/')[:-1])
  title = '.'.join(file.name.split('.')[:-1])
  content = '*TIL 다시보기*\n({}){}\n[읽으러가기]({})'.format(category, title, file.html_url)
  return content


def send_telegram_message(bot_token, chat_id, content):
  bot = telegram.Bot(token=bot_token)
  bot.send_message(chat_id=chat_id, text=content, parse_mode=telegram.ParseMode.MARKDOWN)


def pick_random_markdown_file_in_repo(repo, path='/'):
  file_contents = repo.get_file_contents(path=path)
  
  if isinstance(file_contents, list) : # 폴더 인 경우 폴더 내에서 재탐색
    return pick_random_markdown_file_in_repo(repo, "/" + random.choice(file_contents).path)
  elif file_contents.name.split('.')[-1] != 'md' or file_contents.name.lower() == 'readme.md': # 다른 확장자 혹은 리드미 파일 인 경우 상위 디렉토리에서 재탐색
    return pick_random_markdown_file_in_repo(repo, '/')
  else:
    return file_contents


reminder()