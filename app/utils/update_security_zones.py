import pandas as pd
from sqlalchemy.orm import sessionmaker
from app.models.models import SecurityZone, SessionLocal
from app.utils.logger import logger
from datetime import datetime, timedelta
from app.config import ZONE_FILE_PATH

# 创建 session
session = SessionLocal()  # 使用 SessionLocal() 来创建数据库会话
zonefile = ZONE_FILE_PATH

def get_gmt8_time():
    """ 获取当前 GMT+8 时间，并去掉秒和毫秒 """
    utc_now = datetime.utcnow()  # 获取 UTC 时间
    gmt8_now = utc_now + timedelta(hours=8)  # 转换为 GMT+8
    return gmt8_now.replace(second=0, microsecond=0)  # 返回 datetime 对象，精确到分钟


def update_security_zones_from_excel():
    """ 从 Excel 更新安全域数据表 """
    logger.info(f"开始从 Excel 文件 {ZONE_FILE_PATH} 更新安全域数据表")

    try:
        # 读取 Excel，假设只有一列是安全域名称
        df = pd.read_excel(ZONE_FILE_PATH)

        # 确保 'zone' 列存在（即包含安全域名称）
        if 'zone' not in df.columns:
            logger.error("Excel 文件中缺少 'zone' 列，无法继续处理")
            return

        # 获取所有安全域名称
        zones = df['zone'].dropna().unique()

        # 遍历每个安全域名称
        for zone_name in zones:
            # 检查 SecurityZone 表中是否已经有这个安全域
            existing_zone = session.query(SecurityZone).filter(SecurityZone.name == zone_name).first()

            if existing_zone:
                logger.info(f"安全域 '{zone_name}' 已存在，跳过")
            else:
                # 如果没有，插入新安全域
                new_zone = SecurityZone(name=zone_name)
                session.add(new_zone)
                session.commit()
                logger.info(f"安全域 '{zone_name}' 已新增")

    except Exception as e:
        session.rollback()  # 出错时回滚
        logger.error(f"处理 Excel 文件时出错: {e}")
        raise  # 抛出异常，终止程序

    finally:
        session.close()
        logger.info("数据库连接已关闭")


if __name__ == "__main__":

    update_security_zones_from_excel()