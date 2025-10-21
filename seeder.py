import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.base_model import Base, DateTimeMixin
from src.dishes.model import Dish
from src.core.database import get_db


realistic_funny_dishes = [
    {
        "name": "雨后彩虹蔬菜沙拉",
        "description": "用七种颜色的新鲜蔬菜制作，淋上柠檬蜂蜜酱。适合在小雨转晴的天气享用，让你感受雨后的清新与彩虹的美好。",
    },
    {
        "name": "台风天避风塘炒蟹",
        "description": "香辣避风塘炒蟹，吃完让你浑身发热。专为台风天设计，让你在狂风暴雨中也能感受到火辣的热情。",
    },
    {
        "name": "初雪热红酒炖梨",
        "description": "红酒慢炖香梨，加入肉桂和丁香。适合在第一场雪飘落时品尝，温暖你的胃和心。",
    },
    {
        "name": "大雾天能见度零馄饨",
        "description": "薄皮大馅的鲜肉馄饨，汤清味鲜。专为能见度不足的大雾天准备，让你在朦胧中感受家的温暖。",
    },
    {
        "name": "雷暴夜晚安神莲子汤",
        "description": "银耳莲子百合汤，清甜润燥。适合在电闪雷鸣的夜晚享用，帮你平复被雷声吓到的小心脏。",
    },
    {
        "name": "高温预警凉拌面",
        "description": "冰镇荞麦面配黄瓜丝、鸡丝和芝麻酱。专为高温天气设计，让你在三伏天也能胃口大开。",
    },
    {
        "name": "回南天祛湿红豆沙",
        "description": "陈皮红豆沙，祛湿健脾。适合在潮湿闷热的回南天食用，帮你赶走体内湿气。",
    },
    {
        "name": "寒潮来袭羊肉火锅",
        "description": "内蒙古羊肉涮锅，配韭菜花酱。专为寒潮预警准备，让你在大降温时也能暖到脚底。",
    },
    {
        "name": "霜降时节柿子饼",
        "description": "陕西临潼火晶柿子制成的柿子饼，软糯香甜。适合在霜降节气品尝，让你体验秋天的最后一抹甜。",
    },
    {
        "name": "沙尘暴清肺雪梨羹",
        "description": "川贝炖雪梨，润肺止咳。专为沙尘暴天气设计，帮你清理被沙尘伤害的呼吸道。",
    },
    {
        "name": "梅雨季节霉豆腐",
        "description": "安徽毛豆腐，外酥内嫩。适合在绵绵梅雨季享用，让你体验'长霉'也能如此美味的神奇。",
    },
    {
        "name": "极光出现驯鹿肉串",
        "description": "北欧风味驯鹿肉串，配越莓酱。适合在极光出现的极寒夜晚品尝，让你感受北极圈的美味。",
    },
    {
        "name": "冰雹天护身糖醋里脊",
        "description": "酸甜可口的糖醋里脊，外酥内嫩。专为冰雹天气准备，让你在'天降小冰球'时也能保持好心情。",
    },
    {
        "name": "干旱时节仙人掌沙拉",
        "description": "墨西哥仙人掌沙拉，清爽解腻。适合在久旱无雨时享用，让你体验沙漠植物的顽强生命力。",
    },
    {
        "name": "暴风雪夜热巧克力",
        "description": "比利时黑巧热可可，配棉花糖。专为暴风雪夜晚设计，让你在零下20度也能感受温暖甜蜜。",
    },
    {
        "name": "春雷惊醒韭菜盒子",
        "description": "初春第一茬韭菜做的盒子，鲜香扑鼻。适合在春雷初响时品尝，唤醒你被冬天麻痹的味蕾。",
    },
    {
        "name": "秋老虎酸梅汤",
        "description": "老北京酸梅汤，生津止渴。专为'秋老虎'高温天气准备，让你在立秋后也能消暑解渴。",
    },
    {
        "name": "冻雨天气防滑猪脚姜",
        "description": "广东猪脚姜，驱寒暖身。适合在路面结冰的冻雨天气享用，让你从内到外暖起来，小心路滑哦。",
    },
    {
        "name": "晴空万里云朵面包",
        "description": "日式云朵面包，松软如天上的白云。适合在碧空如洗的好天气享用，让你感受如云朵般的轻盈幸福。",
    },
    {
        "name": "闷热午后薄荷绿豆沙",
        "description": "新鲜薄荷叶加入绿豆沙，清凉解暑。专为闷热潮湿的午后设计，让你瞬间降温5度。",
    },
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
