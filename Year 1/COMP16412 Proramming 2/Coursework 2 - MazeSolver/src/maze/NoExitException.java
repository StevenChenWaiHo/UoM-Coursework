package maze;

/** Exception for when a maze structure with no exits is inputted*/

public class NoExitException extends InvalidMazeException{
    public NoExitException(String message){
        super(message);
    }
}
