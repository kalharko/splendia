import { ColorsEnum } from "../enums/colors.enum";

export class ColorsEnumUtil {

    /**
     * Get the css token class for a given color.
     * The css token classes can be found in app.component.scss
     * @param color used to get a token class
     */
    static getCssTokenClassOfColor(color: ColorsEnum) {    
        switch(color) {
            case ColorsEnum.WHITE: return 'white-token';
            case ColorsEnum.BLUE: return 'blue-token';
            case ColorsEnum.GREEN: return 'green-token';
            case ColorsEnum.RED: return 'red-token';
            case ColorsEnum.BLACK: return 'black-token';
            case ColorsEnum.GOLD: return 'gold-token';
            default: return '';
        }
    }
}