# coding=utf-8
# @Time : 2020/9/6 17:27
# @Author : 胡泽勇
# ${Description}

from game.concept.card import Card, CardType
from game.effector.card_relevant_effector import TempModifyCardLimitEffector
from game.effector.heal_effector import HealEffector
from test.data_prepared_test import WorldPreparedTest


class TestTempModifyCardLimitEffector(WorldPreparedTest):
    def testEffect(self):
        desCardLimit = self.desCardController.cardLimit

        self.turnSystem.beginTurn()
        effector = TempModifyCardLimitEffector(value=1, turn=-1)
        testCard = Card.card(CardType.Support, [effector])
        self.srcCardController.addCard(testCard)

        effector = HealEffector(value=1)
        self.desCardController.addCard(Card.card(CardType.Support, [effector]))
        self.desCardController.addCard(Card.card(CardType.Support, [effector]))
        self.desCardController.addCard(Card.card(CardType.Support, [effector]))
        self.desCardController.addCard(Card.card(CardType.Support, [effector]))
        self.desCardController.addCard(Card.card(CardType.Support, [effector]))
        self.desCardController.addCard(Card.card(CardType.Support, [effector]))
        self.desCardController.addCard(Card.card(CardType.Support, [effector]))

        self.turnSystem.beginTurn()
        self.turnSystem.endTurn()
        self.assertEqual(len(self.desCardController.cardsInHand()), desCardLimit)

        self.desCardController.addCard(Card.card(CardType.Support, [effector]))
        self.desCardController.addCard(Card.card(CardType.Support, [effector]))
        self.turnSystem.beginTurn()
        self.srcCardController.castCard(testCard.serial, self.desLattice)
        self.turnSystem.endTurn()
        self.assertEqual(len(self.desCardController.cardsInHand()), desCardLimit)

        self.desCardController.addCard(Card.card(CardType.Support, [effector]))
        self.desCardController.addCard(Card.card(CardType.Support, [effector]))
        self.turnSystem.beginTurn()
        self.srcCardController.castCard(testCard.serial, self.desLattice)
        self.turnSystem.endTurn()
        desCardLimit += 1
        self.assertEqual(len(self.desCardController.cardsInHand()), desCardLimit)
