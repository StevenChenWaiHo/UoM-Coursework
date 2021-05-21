package chess;

import java.io.Console;

public class Game {
	private static boolean gameEnd = false;

	//This method requires your input
	public static void play(){
        int i0,j0,i1,j1;
        i0 = j0 = i1 = j1 = -1;
        PieceColour player = PieceColour.WHITE;
        Console con = System.console();
        CheckInput check = new CheckInput();
		while (!gameEnd){
            // Get Valid Input
            boolean endWhile =true;
            do{
                i0 = j0 = i1 = j1 = -1;
                endWhile = true;

                // Prompt Input
                if(player == PieceColour.WHITE){
                    System.out.println("\n------ Whites move ------"); 
                }
                else{
                    System.out.println("\n------ Blacks move ------");
                }
                String ori = con.readLine(">Enter Origin:\n");

                // Check user End Game
                if(ori.equals("END")){
                    Board.printBoard();
                    System.out.println("\nPlayer Ended Game");
                    endWhile = true;
                    gameEnd = true;
                    break;
                }

                String des = con.readLine(">Enter Destination:\n"); 

                // Check user End Game
                if(des.equals("END")){
                    Board.printBoard();
                    System.out.println("\nPlayer Ended Game");
                    endWhile = true;
                    gameEnd = true;
                    break;
                }


                // Check Input have two Character
                else if(ori.length() != des.length() || ori.length() != 2){
                    Board.printBoard();
                    System.out.println("\nInvalid Input");
                    endWhile = false;
                    continue;
                }
                
                // Change to int
                i0 = (int) ori.charAt(0) - 49;
                j0 = (int) ori.charAt(1) - 97;
                i1 = (int) des.charAt(0) - 49;
                j1 = (int) des.charAt(1) - 97;

                if(!check.checkCoordinateValidity(ori) || !check.checkCoordinateValidity(des)){
                    Board.printBoard();
                    System.out.println("\nInvalid Origin/Destination");
                    endWhile = false;
                    continue;
                }
                else if(!Board.hasPiece(i0, j0)){
                    Board.printBoard();
                    System.out.println("\nNo Piece is Selected");
                    endWhile = false;
                    continue;
                }
                else if(Board.getPiece(i0, j0).getColour() != player){
                    Board.printBoard();
                    System.out.println("\nIt is not your chess piece");
                    endWhile = false;
                    continue;
                }
                else if(!Board.getPiece(i0,j0).isLegitMove(i0,j0,i1,j1)){
                    Board.printBoard();
                    System.out.println("\nDoes Not Follow Chess Rule");
                    endWhile = false;
                    continue;
                }                
            }while(endWhile == false);
            
            // END is not typed
            if(gameEnd == false){
                gameEnd = Board.movePiece(i0,j0,i1,j1,Board.getPiece(i0,j0));
                if(gameEnd == true){
                    Board.printBoard();
                    System.out.println("\n" + ((player==PieceColour.WHITE)?"White":"Black") + " Wins");
                    break;
                }
            }
            // END is typed
            else{
                break;
            }
        
            Board.printBoard();
            
            // Changes Player Turn
            if(player == PieceColour.WHITE){
                player = PieceColour.BLACK; 
            }
            else{
                player = PieceColour.WHITE;
            }
		}		
	}
	
	//This method should not be edited
	public static void main (String args[]){
		Board.initialiseBoard();
		Board.initialisePieces();
		Board.printBoard();
		Game.play();	
    }
}
