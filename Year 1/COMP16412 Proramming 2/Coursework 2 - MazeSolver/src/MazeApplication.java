import maze.*;
import maze.routing.*;
import maze.visualisation.*;

import javafx.application.Application;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonBar;
import javafx.scene.layout.VBox;
import javafx.scene.layout.HBox;
import javafx.scene.layout.GridPane;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;

import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;

import java.io.IOException;
import java.io.FileNotFoundException;
import java.io.StreamCorruptedException;

/** Maze Application Driver*/
public class MazeApplication extends Application {
    private Maze maze;
    private RouteFinder r;
    private Label statusLabel;
    private VisualMaze mazeV;
    private VBox vBox;
    private VBox textFieldBox;
    private TextField textField;
    private Label textFieldLabel;

    private int StageXSize = 500;
    private int StageYSize = 700;
    private int btnSize = 25;
    private int txtSize = 1;


    /** Starting the application
    @param The stage*/
    @Override
    public void start(Stage stage){
        // Initialize backend
        maze = fromTxtHandler("src/maze/initMaze.txt");
        r = new RouteFinder(maze);
        mazeV = new VisualMaze(maze.getTiles().get(0).size(), maze.getTiles().size(), r.toString(), StageXSize, StageYSize - btnSize * 7);

        // VBox for entrire scene
        vBox = new VBox(10);
        vBox.setAlignment(Pos.CENTER);


        // Status Label
        statusLabel = new Label("Empty");
        statusLabel.setVisible(false);

        // TextField
        VBox textFieldBox = new VBox();
        textFieldBox.setVisible(false);
        HBox textFieldBtnBox = new HBox();
        textFieldLabel = new Label();
        textField = new TextField("resources/mazes/maze.txt");
        textField.setMinSize(StageXSize - btnSize * 6, btnSize);
        MazeButton submit = new MazeButton("Submit", btnSize, txtSize);
        submit.setOnAction(e->{
            switch(textFieldLabel.getText()){
                case "Load Maze:":
                    maze = loadMazeHandler(textField.getText());
                    break;
                case "Load Route:":
                    r = loadRouteHandler(textField.getText());
                    refreshMaze();
                    break;
                case "Save Route:":
                    saveRouteHandler(textField.getText());
                    break;
            }
            textFieldBox.setVisible(false);
        });
        MazeButton close = new MazeButton("Close", btnSize, txtSize);
        close.setOnAction(e->{
            textFieldBox.setVisible(false);
        });
        textFieldBtnBox.getChildren().addAll(textField, submit, close);
        textFieldBox.getChildren().addAll(textFieldLabel, textFieldBtnBox);

        // HBox for Buttons
        HBox topButtons = new HBox();
        topButtons.setAlignment(Pos.CENTER);

        // Create Buttons
        MazeButton loadMaze = new MazeButton("Load Maze", btnSize, txtSize);
        loadMaze.setOnAction(e->{
            statusLabel.setVisible(false);
            textFieldLabel.setText("Load Maze:");
            textFieldBox.setVisible(true);
        });
        MazeButton loadRoute = new MazeButton("Load Route", btnSize, txtSize);
        loadRoute.setOnAction(e->{
            statusLabel.setVisible(false);
            textFieldLabel.setText("Load Route:");
            textFieldBox.setVisible(true);
        });
        MazeButton saveRoute = new MazeButton("Save Route", btnSize, txtSize);
        saveRoute.setOnAction(e->{
            statusLabel.setVisible(false);
            textFieldLabel.setText("Save Route:");
            textFieldBox.setVisible(true);
        });

        MazeButton stepBtn = new MazeButton("Step", btnSize, txtSize);
        stepBtn.setOnAction(e->{
            statusLabel.setVisible(false);
            textFieldBox.setVisible(false);
            stepHandler();
            refreshMaze();
        });

        // Populating panes
        topButtons.getChildren().addAll(loadMaze, loadRoute, saveRoute);
        vBox.getChildren().addAll(topButtons, mazeV, statusLabel, textFieldBox, stepBtn);

        Scene scene = new Scene(vBox,StageXSize,StageYSize);
        stage.setScene(scene);
        stage.setTitle("Maze Solver");
        stage.show();
    }

    /** Refreshing VisualMaze*/
    public void refreshMaze(){
        if(r != null){
            vBox.getChildren().set(1, new VisualMaze(maze.getTiles().get(0).size(), maze.getTiles().size(), r.toString(), StageXSize, StageYSize - btnSize * 7));
        }
    }

    /** Step Handler*/
    public void stepHandler(){
        try{
            r.step();
        } catch(NoRouteFoundException e){
            statusLabel.setText("No Route Found");
            statusLabel.setVisible(true);
        }
    }

    /** Load Maze Handler
    @param path The path to the txt File
    @return The maze in the txt file*/
    public Maze loadMazeHandler(String path){
        try{
            maze = Maze.fromTxt(path);
        } catch(InvalidMazeException e){
            statusLabel.setText("Invalaid maze");
            statusLabel.setVisible(true);
            return maze;
        } catch(FileNotFoundException e){
            statusLabel.setText("File not found");
            statusLabel.setVisible(true);
            return maze;
        } catch(IOException e){
            statusLabel.setText("IOException");
            statusLabel.setVisible(true);
            return maze;
        }
        r = new RouteFinder(maze);
        refreshMaze();
        return maze;
    }

    /** Load Route Handler
    @param path The path to the object file of route
    @return The route*/
    public RouteFinder loadRouteHandler(String path){
        RouteFinder temp = null;
        try{
            temp = RouteFinder.load(path);
        } catch(FileNotFoundException err){
            statusLabel.setText("File Not Found. Try again.");
            statusLabel.setVisible(true);
            return r;
        } catch(ClassNotFoundException err){
            statusLabel.setText("ClassNotFoundException");
            statusLabel.setVisible(true);
            return r;
        } catch(StreamCorruptedException err){
            statusLabel.setText("StreamCorruptedException");
            statusLabel.setVisible(true);
            return r;
        } catch(IOException err){
            statusLabel.setText("IOException");
            statusLabel.setVisible(true);
            return r;
        }
        if(!temp.getMaze().toString().equals(maze.toString())){
            statusLabel.setText("Route incompatible with maze");
            statusLabel.setVisible(true);
            return r;
        }
        else{
            refreshMaze();
            return temp;
        }
    }

    /** Save Route Handler
    @param path The path to store route*/
    public void saveRouteHandler(String path){
        try{
            r.save(path);
        } catch(IOException err){
            statusLabel.setText("IOException");
            statusLabel.setVisible(true);
        }
    }

    /** Maze.fromTxt Handler
    @param path The path to the txt file of maze*/
    public Maze fromTxtHandler(String path){
       try{
           return Maze.fromTxt(path);
       } catch(InvalidMazeException err){
           statusLabel.setText("Invalid Maze");
           return maze;
       } catch(IOException err){
           statusLabel.setText("IOException");
           return maze;
       }
   }


    /** Main
    @param args[] */
    public static void main(String args[]){
        launch(args);
    }
}
