package maze;

/** Exception for when a maze structure with multiple entrances is inputted*/

public class MultipleEntranceException extends InvalidMazeException{
    public MultipleEntranceException(String message){
        super(message);
    }
}
