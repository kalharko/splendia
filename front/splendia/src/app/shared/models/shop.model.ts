import { Patron } from "./patron.model";
import { Rank } from "./rank.model";
import { TokenArray } from "./token_array.model";

export class Shop{
    nobles:Patron[];
    rank1:Rank;
    rank2:Rank;
    rank3:Rank;

    tokens:TokenArray;
}