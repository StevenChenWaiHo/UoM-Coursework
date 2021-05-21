package chess;

public class Knight extends Piece {

    public Knight(PieceColour c){
        colour = c;
        if(c == PieceColour.WHITE){
            setSymbol("♘");
        }
        else{
            setSymbol("♞");   
        }
    }

    public boolean isLegitMove(int i0, int j0, int i1, int j1){
        if((Math.abs(i1-i0) == 2 && Math.abs(j1-j0) == 1)^(Math.abs(j1-j0) == 2 && Math.abs(i1-i0) == 1)){
            // Have Piece at Destination
            if(Board.hasPiece(i1,j1)){
                // Destination Piece is an Opponent
                if(colour != Board.getPiece(i1,j1).getColour()){
                    return true;                
                }
                // Destination Piece is a Ally
                else{
                    return false;                
                }
            }
            // No Piece at Destination
            else{
                return true;
            }  
        }
        // Moving in Invalid Direction
        else{
            return false;
        }
    }	
}
