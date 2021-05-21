package chess;

public class Bishop extends Piece {

    public Bishop(PieceColour c){
        colour = c;
        if(c == PieceColour.WHITE){
            setSymbol("♗");
        }
        else{
            setSymbol("♝");   
        }
    }

    @Override
    public boolean isLegitMove(int i0, int j0, int i1, int j1){
        // Moving Diagonally and not Moving to the same place
        if(Math.abs(i1-i0) == Math.abs(j1-j0) && Math.abs(j1-j0) > 0){
            // Get Bishop Direction
            int dI = Math.abs(i1-i0)/(i1-i0);
            int dJ = Math.abs(j1-j0)/(j1-j0);
            // Iterate thorugh the Path
            for(int i=i0+dI,j=j0+dJ;i!=i1||j!=j1;i+=dI,j+=dJ){
                // A Piece is Blocking Bishop's Path
                if(Board.hasPiece(i,j)){
                    return false;                
                }
            }
            // Have Piece at Destination and No Piece Blocking
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
        // Not Moving Diagonally
        else{
            return false;
        }
    }	
}
