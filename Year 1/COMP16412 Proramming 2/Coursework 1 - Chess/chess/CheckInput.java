package chess;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class CheckInput {
	
	//This method requires your input
	public boolean checkCoordinateValidity(String input){
		Pattern pattern = Pattern.compile("[12345678][abcdefgh]", Pattern.CASE_INSENSITIVE);
        Matcher matcher = pattern.matcher(input);
        return matcher.matches();
	}
}
