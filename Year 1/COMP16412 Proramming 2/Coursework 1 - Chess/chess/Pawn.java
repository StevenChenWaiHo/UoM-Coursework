package chess;

public class Pawn extends Piece {

    public Pawn(PieceColour c){
        colour = c;
        if(c == PieceColour.WHITE){
            setSymbol("♙");
        }
        else{
            setSymbol("♟︎");
        }
    }

    public boolean isLegitMove(int i0, int j0, int i1, int j1){
        // Not moving horzontally & Destination no Piece
        if(j1 == j0 && !Board.hasPiece(i1,j1)){
            // Move one Square Vertically
            if(Math.abs(i1-i0) == 1){
                // Pawn is White and Moving Upwards
                if(colour == PieceColour.WHITE && i0 > i1){
                    return true;                
                }
                // Pawn is Black and Moving Downwards
                else if(colour == PieceColour.BLACK && i1 > i0){
                    return true;                
                }
                // Pawn is Moving in the Wrong Direction
                else{
                    return false;                
                }
            }
            // Moving 2 Square Vertically
            else if(Math.abs(i1-i0) == 2){
                // Pawn is White and is First Move and No Piece in Between and Move in the Right Direction
                if(colour == PieceColour.WHITE && i0 == 6 && !Board.hasPiece(i1+1,j0) && i0 > i1){
                    return true;                
                }
                // Pawn is Black and is First Move
                else if(colour == PieceColour.BLACK && i0 == 1 && !Board.hasPiece(i1-1,j0) && i1 > i0){
                    return true;                
                }
                // Pawn is not in First Move or Piece in Between or in Wrong Direction
                else{
                    return false;                
                }  
            }
            // Pawn is not Moving 1 or 2 Square Vertically
            else{
                return false;                
            }
        }
        // 1 Square Horizontally and Destination have an Opponent Piece
        else if(Math.abs(j1-j0) == 1 && Board.hasPiece(i1,j1) && colour != Board.getPiece(i1,j1).getColour()){
                // White 1 Square Up (Diagonal)
                if(i0-i1 == 1){
                        return true;
                }
                // Black 1 Square Down (Diagonal)
                else if(i1-i0 == 1){
                    return true;
                }
                // Pawn is not Moving Diagonally
                else{
                    return false;            
                }
        }
        // Not Moving in 1 or 2 Square Vertically or Moving 1 or 2 Sqaure Vertically to a Opponent Piece or Not Moving 1 Square Diagonally or Moving 1 Square Horizontally to a Empty Square
        else{
            return false;
        }
    }	
}
