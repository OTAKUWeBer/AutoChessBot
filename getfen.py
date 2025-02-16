import requests

cookies = {
    "session_id": "b075pmwiukzf7vj72h0vswod5lkbfkac"
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
    """Flip the chessboard FEN notation for the opposite perspective."""
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
    """Determine castling rights based on piece positions."""
    castling = []
    ranks = position_part.split('/')
    
    # Check white castling
    if len(ranks) >= 8:
        white_rank = expand_fen_rank(ranks[7])  # 1st rank (white's home)
        if len(white_rank) >= 8:
            if white_rank[4] == 'K':
                if white_rank[7] == 'R':
                    castling.append('K')
                if white_rank[0] == 'R':
                    castling.append('Q')
    
    # Check black castling
    if len(ranks) >= 1:
        black_rank = expand_fen_rank(ranks[0])  # 8th rank (black's home)
        if len(black_rank) >= 8:
            if black_rank[4] == 'k':
                if black_rank[7] == 'r':
                    castling.append('k')
                if black_rank[0] == 'r':
                    castling.append('q')
    
    return ''.join(castling) if castling else '-'

def get_fen_from_image(image_path, color_indicator):
    """Read an image file and retrieve FEN from Chessify website."""
    try:
        with open(image_path, "rb") as image_file:
            original_fen = get_fen(image_file, token)
            if original_fen:
                # Split into position part and other components
                fen_parts = original_fen.split()
                position_part = fen_parts[0] if fen_parts else original_fen
                
                # Flip the board if needed
                if color_indicator == 'b':
                    position_part = flip_board(position_part)
                
                # Get castling rights from the (possibly flipped) position
                castling_rights = get_castling_rights(position_part)
                
                # Construct full FEN with all required components
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
    image_path = "chess-screenshot.png"
    color_indicator = input("Is it White or Black to move? (w/b): ").strip().lower()
    
    if color_indicator not in ['w', 'b']:
        print("Invalid input. Please enter 'w' for White or 'b' for Black.")
    else:
        result = get_fen_from_image(image_path, color_indicator)
        print("Generated FEN:", result)