import { Player } from "./player.model";
import { Shop } from "./shop.model";

export interface BoardState{
    player1: Player;
    player2: Player;


    shop:Shop;

}

