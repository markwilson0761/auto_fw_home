import logging
from logging.handlers import RotatingFileHandler

# 配置日志，输出到文件和终端
logging.basicConfig(
    level=logging.DEBUG,  # 记录 DEBUG 及以上级别的日志
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        RotatingFileHandler("app.log", maxBytes=5*1024*1024, backupCount=3),  # 5MB 日志文件大小限制，保留 3 个历史文件
        logging.StreamHandler()  # 输出到终端
    ]
)

# 获取 logger 实例
logger = logging.getLogger(__name__)
logging.disable(logging.CRITICAL)
#logging.disable(logging.NOTSET)
# 示例：用于调试
logger.debug("日志模块已初始化")
