import { Card } from "./card.model";

export class Player{
    bonusList: number[];
    reservedCards: Card[];
    tokenList: number[];
    victoryPoints: number;
    currentPlayer: boolean;
}
