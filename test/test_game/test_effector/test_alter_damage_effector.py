# coding=utf-8
# @Time : 2020/8/26 12:08
# @Author : 胡泽勇
# ${Description}

from game.concept.card import Card
from game.concept.card import CardType
from game.concept.cast_info import CastInfo
from game.effector.alter_damage_effector import AlterDamageByPercentEffector
from game.effector.alter_damage_effector import ImmuneDeadDamageOnceEffector
from game.effector.damage_effector import DamageEffector, DamageType
from game.modifier.turned_modifier.damage_relevant_modifier import ModifierAlterType
from game.world_event.decision_event import ClientCastEvent
from test.data_prepared_test import WorldPreparedTest


class TestTurnedAlterDamageByPercent(WorldPreparedTest):
    def testEffect(self):
        percent, damage = 0.5, 2
        desLife = self.desLc.lifeState.current

        self.turnSystem.beginTurn()
        # 使对方受到的伤害设置为percent
        effector = AlterDamageByPercentEffector(percent=percent, turn=1, alterType=ModifierAlterType.Suffer)
        # 打出该效果
        castInfo = CastInfo(self.srcEntity, self.desLattice, 0, Card.card(CardType.Support, [effector]))
        self.world.eventCenter.fire(ClientCastEvent(castInfo))
        # 对对方造成伤害
        damageEffector = DamageEffector(value=damage, damageType=DamageType.Normal)
        # 打出该效果
        castInfo = CastInfo(self.srcEntity, self.desLattice, 0, Card.card(CardType.Damage, [damageEffector]))
        self.world.eventCenter.fire(ClientCastEvent(castInfo))
        # 进入结算
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        self.world.eventCenter.fire(ClientCastEvent(castInfo))
        self.turnSystem.endTurn()
        desLife -= 2
        self.assertEqual(self.desLc.lifeState.current, desLife)


class TestImmuneDeadDamageOnceEffector(WorldPreparedTest):
    def testAliveEffect(self):
        # 满血值
        original = desLife = self.desLc.lifeState.current
        # 直接给目标角色施加免疫伤害
        effector = ImmuneDeadDamageOnceEffector(turn=-1)
        effector.effect(self.desEntity, self.desLattice)

        self.turnSystem.beginTurn()
        # 尝试施加不致死伤害
        damageEffector = DamageEffector(value=1, damageType=DamageType.Normal)
        damageEffector.effect(self.srcEntity, self.desLattice)
        self.turnSystem.endTurn()
        # 正常计算伤害
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        # 施加不致死伤害
        damageEffector = DamageEffector(value=3, damageType=DamageType.Normal)
        damageEffector.effect(self.srcEntity, self.desLattice)
        # 尝试施加致死伤害
        damageEffector = DamageEffector(value=original, damageType=DamageType.Normal)
        damageEffector.effect(self.srcEntity, self.desLattice)
        # 并施加后续伤害
        damageEffector = DamageEffector(value=1, damageType=DamageType.Normal)
        damageEffector.effect(self.srcEntity, self.desLattice)
        self.turnSystem.endTurn()
        # 只收到了之前的不致死伤害
        desLife -= 3
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        # 施加不至死伤害
        damageEffector = DamageEffector(value=2, damageType=DamageType.Normal)
        damageEffector.effect(self.srcEntity, self.desLattice)
        self.turnSystem.endTurn()
        # 正常计算伤害，说明buff没有后向影响
        desLife -= 2
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        # 施加致死伤害
        damageEffector = DamageEffector(value=original, damageType=DamageType.Normal)
        damageEffector.effect(self.srcEntity, self.desLattice)
        self.turnSystem.endTurn()
        # 检测死亡
        self.desLc.checkDead()
        # 确认死亡，说明buff不再存在
        self.assertTrue(self.desLc.dead())
