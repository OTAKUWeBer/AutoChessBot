import requests

# Go to chessify.me, log in, and get the session_id from the cookies
cookies = {
    "session_id": "romk2hiw1nxu19vns4s0v9ehiv8wctrl"
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


def get_fen_from_image(image_path, color_indicator):
    """Read an image file and retrieve FEN from Chessify website."""
    try:
        with open(image_path, "rb") as image_file:
            fen = get_fen(image_file, token)
            if fen:
                if color_indicator == 'b':
                    fen = flip_board(fen)

                fen_with_color = f"{fen} {color_indicator}"
                return fen_with_color
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
    image_path = input("Enter the path to the chessboard image: ").strip()
    color_indicator = input("Is it White or Black to move? (w/b): ").strip().lower()
    
    if color_indicator not in ['w', 'b']:
        print("Invalid input. Please enter 'w' for White or 'b' for Black.")
    else:
        get_fen_from_image(image_path, color_indicator)
