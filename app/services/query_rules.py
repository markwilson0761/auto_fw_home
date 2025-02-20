from sqlalchemy.orm import sessionmaker
from app.models.models import RuleSet, SecurityZone, engine, SessionLocal
from app.utils.logger import logger

# 创建数据库会话
Session = sessionmaker(bind=engine)
session = SessionLocal()


def get_zone_id(zone_name):
    """ 获取安全域 ID，如果不存在返回 None """
    zone_id = session.query(SecurityZone.id).filter(SecurityZone.name == zone_name).scalar()
    if not zone_id:
        logger.warning(f"安全域不存在: {zone_name}")
    return zone_id


def query_firewall_rule(src_zone: str, dst_zone: str):
    """
    根据源安全域和目的安全域查询防火墙策略

    :param src_zone: 源安全域名称
    :param dst_zone: 目的安全域名称
    :return: 允许（allow）或限制（restrict），如果规则不存在则返回 None
    """
    logger.info(f"查询防火墙规则: {src_zone} -> {dst_zone}")

    try:
        # 获取安全域 ID
        src_zone_id = get_zone_id(src_zone)
        dst_zone_id = get_zone_id(dst_zone)

        # 如果有安全域不存在，返回 None
        if src_zone_id is None or dst_zone_id is None:
            logger.warning(f"查询失败，安全域不存在: {src_zone} 或 {dst_zone}")
            return None

        # 查询规则
        rule = session.query(RuleSet.action).filter(
            RuleSet.src_zone_id == src_zone_id,
            RuleSet.dst_zone_id == dst_zone_id
        ).scalar()

        if rule:
            logger.info(f"查询结果: {src_zone} -> {dst_zone} 策略: {rule}")
            return rule
        else:
            logger.warning(f"未找到防火墙规则: {src_zone} -> {dst_zone}")
            return None

    except Exception as e:
        logger.error(f"查询防火墙规则时出错: {e}")
        return None

    finally:
        session.close()
        logger.info("数据库连接已关闭")


if __name__ == "__main__":
    # 测试查询
    src = "ENT-DMZ"
    dst = "HRZ-MGT"
    policy = query_firewall_rule(src, dst)
    print(f"防火墙策略: {policy}")
