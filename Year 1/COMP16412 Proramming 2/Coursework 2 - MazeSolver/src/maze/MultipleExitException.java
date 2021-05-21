package maze;

/** Exception for when a maze structure with multiple exit is inputted*/

public class MultipleExitException extends InvalidMazeException{
    public MultipleExitException(String message){
        super(message);
    }
}
