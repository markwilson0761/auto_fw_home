import pandas as pd
from sqlalchemy.orm import sessionmaker
from app.models.models import RuleSet, SecurityZone, engine, SessionLocal
from app.utils.logger import logger
from datetime import datetime, timedelta
from app.config import MATRIX_FILE_PATH as file_path

# 创建 session
Session = sessionmaker(bind=engine)
session = SessionLocal()


def get_gmt8_time():
    """ 获取当前 GMT+8 时间，并去掉秒和毫秒 """
    utc_now = datetime.utcnow()  # 获取 UTC 时间
    gmt8_now = utc_now + timedelta(hours=8)  # 转换为 GMT+8
    return gmt8_now.replace(second=0, microsecond=0)  # 返回 datetime 对象，精确到分钟


def get_zone_id(zone_name):
    """ 获取安全域 ID，如果不存在返回 None """
    zone_id = session.query(SecurityZone.id).filter(SecurityZone.name == zone_name).scalar()
    if not zone_id:
        logger.error(f"安全域不存在: {zone_name}")
    return zone_id


def update_database_from_excel():
    """ 从 Excel 读取防火墙规则并更新数据库 """
    logger.info(f"开始从 Excel 文件 {file_path} 读取数据")

    try:
        df = pd.read_excel(file_path, index_col=0)  # 第一列是 src_zone，第一行是 dst_zone
        df = df.reset_index().melt(id_vars=df.index.name, var_name='dst_zone', value_name='action')

        # 清空旧数据，防止重复
        session.query(RuleSet).delete()
        session.commit()
        logger.info("已清空旧规则数据")

        valid_rules = 0  # 统计成功写入的规则数

        for _, row in df.iterrows():
            # 检查策略是否符合要求
            if row['action'] not in ['allow', 'restrict']:
                logger.warning(f"非法策略，跳过: {row['src_zone']} -> {row['dst_zone']} action: {row['action']}")
                continue

            # 获取安全域 ID，若不存在则跳过
            src_zone_id = get_zone_id(row['src_zone'])
            dst_zone_id = get_zone_id(row['dst_zone'])

            if src_zone_id is None or dst_zone_id is None:
                logger.warning(f"跳过规则: {row['src_zone']} -> {row['dst_zone']}，因为安全域未定义")
                continue

            # 插入规则
            rule = RuleSet(
                src_zone_id=src_zone_id,
                dst_zone_id=dst_zone_id,
                action=row['action'],
                updated_at=get_gmt8_time(),
                changed_by='manual'
            )
            session.add(rule)
            valid_rules += 1

        session.commit()
        logger.info(f"成功导入 {valid_rules} 条规则")

    except Exception as e:
        session.rollback()  # 出错时回滚
        logger.error(f"处理 Excel 数据时出错: {e}")
        raise  # 终止程序

    finally:
        session.close()
        logger.info("数据库连接已关闭")


if __name__ == "__main__":
    update_database_from_excel()
