import requests

cookies = {
    "session_id": "4nv52887bzzfui52fuuwjxs78wminwq0"
}

def get_token(cookies):
    try:
        response = requests.get("https://chessify.me/user_account/user_plans_info", cookies=cookies)
        response.raise_for_status()
        return response.json().get("token")
    except requests.RequestException as e:
        print(f"Error fetching token: {e}")
        return None

def get_fen(image_file, token):
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
        return data.get("fen") or "Error: No FEN found. The image may not be a valid chessboard."
    except requests.RequestException as e:
        print(f"Error fetching FEN: {e}")
        return None

token = get_token(cookies)

def flip_board(fen):
    rows = fen.split("/")
    return "/".join([row[::-1] for row in rows[::-1]])

def expand_fen_rank(rank):
    expanded = []
    for c in rank:
        expanded.extend([' '] * int(c) if c.isdigit() else [c])
    return expanded

def get_castling_rights(position):
    castling = []
    ranks = position.split('/')

    if len(ranks) >= 8:
        white_rank = expand_fen_rank(ranks[7])
        if white_rank[4] == 'K':
            if white_rank[7] == 'R': castling.append('K')
            if white_rank[0] == 'R': castling.append('Q')

    if len(ranks) >= 1:
        black_rank = expand_fen_rank(ranks[0])
        if black_rank[4] == 'k':
            if black_rank[7] == 'r': castling.append('k')
            if black_rank[0] == 'r': castling.append('q')
    
    return ''.join(castling) or '-'

def ensure_standard_orientation(position):
    rows = position.split('/')
    if len(rows) != 8:
        return position
    return flip_board(position) if 'K' not in rows[7] else position

def get_fen_from_image(image_path, color):
    try:
        with open(image_path, "rb") as image_file:
            original_fen = get_fen(image_file, token)
            if original_fen:
                fen_parts = original_fen.split()
                position = fen_parts[0] if fen_parts else original_fen
                position = ensure_standard_orientation(position)
                castling_rights = get_castling_rights(position)
                return f"{position} {color} {castling_rights} - 0 1"
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
    color = input("Is it White or Black to move? (w/b): ").strip().lower()
    
    if color not in ['w', 'b']:
        print("Invalid input. Please enter 'w' for White or 'b' for Black.")
    else:
        fen = get_fen_from_image(image_path, color)
        print("Generated FEN:", fen)
