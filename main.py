import cv2
import pyautogui
import time
from pynput import mouse
from pathlib import Path
import subprocess
import mss
import mss.tools
import platform
from getfen import get_fen_from_image


# Detect OS
IS_WINDOWS = platform.system() == "Windows"

# Set Stockfish executable path
if IS_WINDOWS:
    stockfish_path = "stockfish.exe"  # Change to your actual path
else:
    stockfish_path = "stockfish"  # Linux default

# Global variables
last_click_time = 0
last_automated_click_time = 0  # Track automated clicks
double_click_threshold = 0.3
color_indicator = "w"

def capture_screenshot(path):
    """Capture a screenshot and save it to the specified path."""
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=str(path))
        return True
    except Exception as e:
        print(f"Screenshot failed: {e}")
        return False

def get_best_move(fen):
    """Run Stockfish to determine the best move from a given FEN."""
    try:
        stockfish = subprocess.Popen(
            [stockfish_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stockfish.stdin.write(f"position fen {fen}\n")
        stockfish.stdin.write("go depth 15\n")
        stockfish.stdin.flush()

        output = ""
        while True:
            line = stockfish.stdout.readline()
            if line.startswith("bestmove"):
                output = line.strip()
                break

        stockfish.stdin.write("quit\n")
        stockfish.stdin.flush()
        stockfish.wait()
        return output.split()[1] if output else None
    except Exception as e:
        print(f"Stockfish error: {e}")
        return None

def process_chessboard(image):
    """Process image to find chessboard and create board positions."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    chessboard_contour = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / h
            if 0.8 <= aspect_ratio <= 1.2 and w > 300 and h > 300:
                chessboard_contour = approx
                break

    if chessboard_contour is not None:
        x, y, w, h = cv2.boundingRect(chessboard_contour)
        board_size = 8
        square_width = w // board_size
        square_height = h // board_size

        board_positions = {}
        for row in range(board_size):
            for col in range(board_size):
                square_x = x + col * square_width
                square_y = y + row * square_height
                board_positions[(col, row)] = (square_x + square_width // 2, square_y + square_height // 2)
        return board_positions
    return None

def chess_notation_to_index(move, board_positions, color_indicator):
    """Convert chess notation (e2e4) to board indices considering player color."""
    # Column and row mappings based on player's color
    if color_indicator == "w":
        col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        row_map = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    else:  # Black player (flipped board)
        col_map = {'a':7, 'b':6, 'c':5, 'd':4, 'e':3, 'f':2, 'g':1, 'h':0}
        row_map = {'1':0, '2':1, '3':2, '4':3, '5':4, '6':5, '7':6, '8':7}
    
    try:
        start_col = col_map[move[0]]
        start_row = row_map[move[1]]
        end_col = col_map[move[2]]
        end_row = row_map[move[3]]
        return board_positions[(start_col, start_row)], board_positions[(end_col, end_row)]
    except KeyError:
        print(f"Invalid move notation: {move}")
        return None, None

def move_piece(move, board_positions, color_indicator):
    """Simulate mouse movements to make the chess move considering player color."""
    global last_automated_click_time
    start_pos, end_pos = chess_notation_to_index(move, board_positions, color_indicator)
    if not start_pos or not end_pos:
        return

    start_x, start_y = start_pos
    end_x, end_y = end_pos

    # Perform clicks and track automation time
    pyautogui.click(start_x, start_y)
    last_automated_click_time = time.time()
    time.sleep(0.25)
    pyautogui.click(end_x, end_y)
    last_automated_click_time = time.time()
    print(f"Executed move: {move}")

def on_click(x, y, button, pressed):
    """Handle double-click events and process moves."""
    global last_click_time, last_automated_click_time
    if button == mouse.Button.left and pressed:
        current_time = time.time()
        
        # Ignore clicks that happen within 0.5 seconds of automated actions
        if current_time - last_automated_click_time < 0.5:
            return
            
        if (current_time - last_click_time) <= double_click_threshold:
            print("\nProcessing move...")
            try:
                # Capture screenshot
                screenshot_path = Path("chess-screenshot.png")
                if screenshot_path.exists():
                    screenshot_path.unlink()
                
                if not capture_screenshot(screenshot_path):
                    return
                
                # Process chessboard
                image = cv2.imread(str(screenshot_path))
                board_positions = process_chessboard(image)
                if not board_positions:
                    print("Chessboard not detected!")
                    return
                
                # Get FEN and best move
                fen = get_fen_from_image(str(screenshot_path), color_indicator)
                if not fen:
                    print("FEN extraction failed!")
                    return
                
                best_move = get_best_move(fen)
                if best_move:
                    print(f"Recommended move: {best_move}")
                    move_piece(best_move, board_positions, color_indicator)
                else:
                    print("No valid move found!")
            
            except Exception as e:
                print(f"Error processing move: {str(e)}")
            
            finally:
                last_click_time = 0
                return
        
        last_click_time = current_time

# Get player color
while True:
    color_input = input("What color are you playing? (1 for White, 2 for Black): ").strip()
    if color_input == "1":
        color_indicator = "w"
        break
    elif color_input == "2":
        color_indicator = "b"
        break

# Start mouse listener
print("\nDouble-click anywhere to make a move (keep this window open)...")
print("Press Ctrl+C to exit...\n")
print("The script will now wait for your explicit double-clicks!")

# Continuous listener
with mouse.Listener(on_click=on_click) as listener:
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting program...")
        listener.stop()