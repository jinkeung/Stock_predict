import logging
from logging.handlers import TimedRotatingFileHandler
import datetime

# 현재 날짜
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

# TimedRotatingFileHandler 설정
handler = TimedRotatingFileHandler(filename=f'SA_Log_{current_date}.log', when='midnight', interval=1, backupCount=1)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# 로거 설정
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
