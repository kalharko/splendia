import { Cpu } from "./cpu.model";
import { GameState } from "./game_state.model";
import { Player } from "./player.model";
import { Patron} from "./patron.model";
import { Rank } from "./rank.model";

export interface BoardState{
    CPUS: Cpu[];
    bank: number[];
    gameState: GameState;
    humanPlayer: Player;
    patrons: Patron[];
    shop: Rank[];
    logs: string[];
}

