import { Card } from "./card.model";
import { Patron } from "./patron.model";

export class Player{
    cards:Card[];
    nobles: Patron[];
    object:any;

    reserved: [Card, Card, Card];
    tokens: number [];

}