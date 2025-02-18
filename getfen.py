import requests

cookies = {
    "session_id": "4nv52887bzzfui52fuuwjxs78wminwq0"
}

def get_token(cookies):
    """Fetch the user token using session cookies."""
    try:
        response = requests.get("https://chessify.me/user_account/user_plans_info", cookies=cookies)
        response.raise_for_status()
        return response.json().get("token")
    except requests.RequestException as e:
        print(f"Error fetching token: {e}")
        return None

def get_fen(image_file, token):
    """Send an image file to Chessify to retrieve the FEN notation."""
    if not token:
        print("Error: No token provided.")
        return None

    files = {
        "file": ("image_0.jpeg", image_file, "image/jpeg"),
        "token": (None, token),
    }

    try:
        response = requests.post("https://chessify.me/fen", files=files)
        response.raise_for_status()
        data = response.json()
        if "fen" in data:
            return data["fen"]
        else:
            print("Error: No FEN found in response. The image may not be a valid chessboard.")
            return None
    except requests.RequestException as e:
        print(f"Error fetching FEN: {e}")
        return None

token = get_token(cookies)  # Fetch token once and reuse

def flip_board(fen):
    """Flip the chessboard FEN notation (reverse ranks and each rank's content)."""
    rows = fen.split("/")
    flipped_rows = [row[::-1] for row in rows[::-1]]
    return "/".join(flipped_rows)

def expand_fen_rank(rank):
    """Expand a FEN rank string into individual squares."""
    expanded = []
    for c in rank:
        if c.isdigit():
            expanded.extend([' '] * int(c))
        else:
            expanded.append(c)
    return expanded

def get_castling_rights(position_part):
    """Determine castling rights based on piece positions in a standard-orientation board.
    
    Assumes:
      - White's home rank is the last rank (index 7) and Black's home rank is the first rank (index 0).
    """
    castling = []
    ranks = position_part.split('/')
    
    # Check White castling (White's king should be on the 1st rank, i.e. last row)
    if len(ranks) >= 8:
        white_rank = expand_fen_rank(ranks[7])
        if len(white_rank) >= 8:
            if white_rank[4] == 'K':
                if white_rank[7] == 'R':
                    castling.append('K')
                if white_rank[0] == 'R':
                    castling.append('Q')
    
    # Check Black castling (Black's king should be on the 8th rank, i.e. first row)
    if len(ranks) >= 1:
        black_rank = expand_fen_rank(ranks[0])
        if len(black_rank) >= 8:
            if black_rank[4] == 'k':
                if black_rank[7] == 'r':
                    castling.append('k')
                if black_rank[0] == 'r':
                    castling.append('q')
    
    return ''.join(castling) if castling else '-'

def ensure_standard_orientation(position_part):
    """
    Ensure the board is in standard FEN orientation (White on the bottom).
    
    In a standard FEN the 8th rank is listed first and the 1st rank last.
    Therefore, the 1st rank (last in the string) should contain White's king ("K").
    If not, we assume the board is flipped and we flip it.
    """
    rows = position_part.split('/')
    if len(rows) != 8:
        return position_part  # Not a valid board; skip flipping.
    # If the last row does not contain the White king, flip the board.
    if 'K' not in rows[7]:
        return flip_board(position_part)
    return position_part

def get_fen_from_image(image_path, color_indicator):
    """
    Read an image file and retrieve FEN from Chessify.
    
    This version always returns a FEN in standard orientation (White on bottom)
    regardless of how Chessify returned it.
    
    The `color_indicator` (either 'w' or 'b') is still used to set the side to move.
    """
    try:
        with open(image_path, "rb") as image_file:
            original_fen = get_fen(image_file, token)
            if original_fen:
                # Split into position part and extra fields (if any)
                fen_parts = original_fen.split()
                position_part = fen_parts[0] if fen_parts else original_fen

                # Normalize orientation: ensure White is on the bottom (1st rank).
                position_part = ensure_standard_orientation(position_part)

                # Get castling rights based on the normalized board.
                castling_rights = get_castling_rights(position_part)

                # Construct full FEN (the turn, castling, en passant, move counts remain as given/assumed).
                full_fen = f"{position_part} {color_indicator} {castling_rights} - 0 1"
                return full_fen
            else:
                print("Failed to retrieve FEN.")
                return None
    except FileNotFoundError:
        print(f"Error: File '{image_path}' not found.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    image_path = "test.png"
    color_indicator = input("Is it White or Black to move? (w/b): ").strip().lower()
    
    if color_indicator not in ['w', 'b']:
        print("Invalid input. Please enter 'w' for White or 'b' for Black.")
    else:
        result = get_fen_from_image(image_path, color_indicator)
        print("Generated FEN:", result)
