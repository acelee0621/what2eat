import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.base_model import Base, DateTimeMixin
from src.dishes.model import Dish
from src.core.database import get_db


realistic_funny_dishes = [
    # ===== 欢乐硬菜区 =====
    {
        "name": "佛跳墙",
        "description": "台风天锁门独享，狂风在外，福气在罐。"
    },
    {
        "name": "鲍汁百灵菇",
        "description": "初雪落地时吃，鲜掉眉毛，暖到心底。"
    },
    {
        "name": "龙虾刺身船",
        "description": "高温预警日，上船即入海，一口降温5℃。"
    },
    {
        "name": "红烧大鲍翅",
        "description": "寒潮蓝色预警，让鲍翅给你加一层保暖内衣。"
    },
    {
        "name": "清蒸东星斑",
        "description": "春雷第一声，蒸条“星”运，一年红红火火。"
    },
    {
        "name": "黑松露北京烤鸭",
        "description": "霜降当天，鸭皮脆到像踩碎薄冰，仪式感拉满。"
    },
    {
        "name": "金汤花胶鸡",
        "description": "回南天湿到发“霉”，花胶帮你把皮肤拉回满水位。"
    },
    {
        "name": "蒜蓉粉丝蒸帝王蟹",
        "description": "极光夜加餐，蟹腿比筷子长，吃完抬头继续追光。"
    },
    {
        "name": "葱烧海参",
        "description": "沙尘暴出门难，海参先给你把肺润成绿洲。"
    },
    {
        "name": "麻辣牛油火锅（和牛版）",
        "description": "冰雹噼啪响，屋内牛油翻滚，冰火两重天。"
    },

    # ===== 家常小确幸区 =====
    {
        "name": "番茄炒蛋",
        "description": "小雨淅沥，红黄配色像窗外彩虹被搬进锅里。"
    },
    {
        "name": "青椒土豆丝",
        "description": "大雾天能见度低，咔嚓一口脆响，开路！"
    },
    {
        "name": "可乐鸡翅",
        "description": "闷热午后，甜咸气泡在舌尖打雷，比空调先降温。"
    },
    {
        "name": "麻婆豆腐",
        "description": "雷暴夜，一勺麻辣闪电，瞬间劈开味蕾。"
    },
    {
        "name": "糖醋排骨",
        "description": "冻雨路滑，酸甜平衡帮你找回身体的重心。"
    },
    {
        "name": "蒜蓉空心菜",
        "description": "干旱日一口绿，咔嚓脆响，像给嗓子浇了一场及时雨。"
    },
    {
        "name": "腊肉炒蒜苗",
        "description": "暴风雪夜，腊肉烟熏味把屋子瞬间变成小木屋。"
    },
    {
        "name": "酸辣土豆丝",
        "description": "秋老虎发威，酸爽比电扇先抵达灵魂。"
    },
    {
        "name": "紫菜蛋花汤",
        "description": "晴空万里，喝口“海”的味道，把蓝天装进胃里。"
    },
    {
        "name": "葱油拌面",
        "description": "梅雨季晾不干衣服，却晾得干一碗热腾腾的灵魂。"
    }
]


async def create_realistic_funny_dishes(db_session: AsyncSession):
    """创建有趣但更贴近现实的菜品数据"""
    try:
        created_count = 0

        for dish_data in realistic_funny_dishes:
            # 检查是否已存在（根据名称判断）
            existing = await db_session.execute(
                Dish.__table__.select().where(Dish.name == dish_data["name"])
            )

            if not existing.first():
                dish = Dish(**dish_data)
                db_session.add(dish)
                created_count += 1

        await db_session.commit()
        print(f"成功创建 {created_count} 道新菜品！")

        # 显示部分菜品
        result = await db_session.execute(Dish.__table__.select().limit(3))
        dishes = result.fetchall()

        print("\n示例菜品预览：")
        for dish in dishes:
            print(f"- {dish.name}: {dish.description[:60]}...")

    except Exception as e:
        await db_session.rollback()
        print(f"创建菜品时出错: {e}")
        raise


# 主函数
async def main():
    """主函数：运行菜品数据初始化"""
    async for db in get_db():
        await create_realistic_funny_dishes(db)
        break


if __name__ == "__main__":
    # 运行脚本
    asyncio.run(main())
