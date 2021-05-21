package maze.visualisation;

import maze.*;

import javafx.scene.layout.HBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;

public class VisualTile extends HBox{

    public VisualTile(char c, double recXSize, double recYSize){
        super();
        Rectangle shape = new Rectangle(recXSize, recYSize);
        switch(c){
            case '#':
            shape.setFill(Color.BLACK);
            break;
            case '.':
            shape.setFill(Color.WHITE);
            break;
            case 'e':
            shape.setFill(Color.BLUE);
            break;
            case 'x':
            shape.setFill(Color.BLUE);
            break;
            case '*':
            shape.setFill(Color.GREEN);
            break;
            case '-':
            shape.setFill(Color.RED);
            break;
        }
        this.getChildren().addAll(shape);
    }
}
