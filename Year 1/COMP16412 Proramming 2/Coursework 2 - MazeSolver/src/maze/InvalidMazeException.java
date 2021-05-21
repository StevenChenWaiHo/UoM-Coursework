package maze;

/** Exception for when invalid maze structure is inputted*/

public class InvalidMazeException extends Exception{
    public InvalidMazeException(String message){
        super(message);
    }
}
