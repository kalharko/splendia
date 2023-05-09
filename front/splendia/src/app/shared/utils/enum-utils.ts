import { ColorsEnum } from "../enums/colors.enum";

export class ColorsEnumUtils {
    public static toString(color: ColorsEnum): string {
        switch(color) {
            case ColorsEnum.RED: return "red";
            case ColorsEnum.BLUE: return "blue";
            case ColorsEnum.BLACK: return "black";
            case ColorsEnum.GOLD: return "gold";
            case ColorsEnum.WHITE: return "white";
            case ColorsEnum.GREEN: return "green";
        }

        return '';
    }
}