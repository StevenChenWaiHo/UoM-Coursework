package maze.visualisation;

import maze.*;
import javafx.scene.layout.GridPane;
import javafx.geometry.Insets;

public class VisualMaze extends GridPane{

    public VisualMaze(int xsize, int ysize, String maze, int boardXSize, int boardYSize){
        super();
        double recXSize = boardXSize / xsize;
        double recYSize = boardYSize / ysize;
        this.setPadding(new Insets(0, 10, 0, 10));
        this.setHgap(1);
        this.setVgap(1);
        maze = maze.replaceAll("[0-9]|\\s","");
        for(int row = 0; row < ysize; row++){
            for (int col = 0; col < xsize; col++) {
                this.add(new VisualTile(maze.charAt(xsize * row + col), recXSize, recYSize), col, row, 1, 1);
            }
        }
    }
}
