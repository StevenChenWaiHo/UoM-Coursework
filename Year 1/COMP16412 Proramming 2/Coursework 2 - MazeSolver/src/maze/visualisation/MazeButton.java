package maze.visualisation;

import javafx.scene.control.Button;

public class MazeButton extends Button{

    public MazeButton(String function, int size, int txtsize){
        super(function);
        this.setMinSize(size*2, size);
        this.setStyle("-fx-font-size: " + txtsize + "em; ");
    }
}
