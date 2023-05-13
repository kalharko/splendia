import { ColorsEnum } from "../enums/colors.enum";

/**
 * Converts a color from colors enum as a string
 * @param color color to convert
 * @return string color
 */
export function colorsEnumToString(color: ColorsEnum) {
    switch (color) {
        case ColorsEnum.WHITE: return "white";
        case ColorsEnum.RED: return "red";
        case ColorsEnum.BLUE: return "blue";
        case ColorsEnum.GREEN: return "green";
        case ColorsEnum.GOLD: return "gold";
        case ColorsEnum.BLACK: return "black";
        default: return "";
    }
}
