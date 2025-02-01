import time
from pathlib import Path
import subprocess
import os
from pynput.mouse import Listener
from threading import Thread
from getfen import get_fen_from_image


# Screenshot path
screenshot_path = Path("chess-screenshot.png")

# Function to capture screen (ss)
def capture_screenshot(path):
    """Capture a screenshot and save it to the specified path."""
    try:
        if "WAYLAND_DISPLAY" in os.environ:
            subprocess.run(["grim", str(path)], check=True)
        else:
            import mss
            import mss.tools

            with mss.mss() as sct:
                monitor = sct.monitors[1]  # Capture the primary screen
                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=str(path))
    except Exception as e:
        print(f"Screenshot failed: {e}")


# Get the next best move
def get_best_move(fen):
    """Run Stockfish to determine the best move from a given FEN."""
    try:
        stockfish = subprocess.Popen(
            ["stockfish"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stockfish.stdin.write(f"position fen {fen}\n")
        stockfish.stdin.write("go depth 21\n")
        stockfish.stdin.flush()

        output = ""
        while True:
            line = stockfish.stdout.readline()
            if line.startswith("bestmove"):
                output = line.strip()
                break

        stockfish.stdin.write("quit\n")
        stockfish.stdin.flush()
        stockfish.stdout.close()
        stockfish.stderr.close()
        stockfish.wait()

        return output.split()[1] if output else None
    except Exception as e:
        print(f"Stockfish error: {e}")
        return None

# Double click sensor
def on_click(x, y, button, pressed):
    """Detects double-click and captures the chessboard image."""
    if button.name == "left" and pressed:
        current_time = time.time()
        if current_time - on_click.last_click_time < 0.3:  # Double-click detected
            print("Double-click detected, capturing screenshot!")

            try:
                screenshot_path.unlink(missing_ok=True)  # Delete old screenshot
                capture_screenshot(screenshot_path)

                if screenshot_path.exists():
                    fen_with_color = get_fen_from_image(str(screenshot_path), color_indicator)

                    if fen_with_color is None:
                        print("Failed to extract FEN from image.")
                        return

                    print(f"FEN: {fen_with_color}")

                    best_move = get_best_move(fen_with_color)
                    if best_move:
                        print(f"Best move: {best_move}")
                    else:
                        print("Failed to determine the best move.")
                else:
                    print("Screenshot not found!")

            except Exception as e:
                print(f"Error: {e}")

        on_click.last_click_time = current_time

# click reset
on_click.last_click_time = 0

# Ask for color only once
while True:
    color_input = input("Is it your turn to move? (1 for White, 2 for Black): ").strip()
    if color_input == "1":
        color_indicator = "w"
        break
    elif color_input == "2":
        color_indicator = "b"
        break
    else:
        print("Invalid input. Please enter '1' for White or '2' for Black.")

# Start mouse listener on a separate thread
listener = Listener(on_click=on_click)
listener_thread = Thread(target=listener.start)
listener_thread.daemon = True
listener_thread.start()

# Keep the script running
while True:
    time.sleep(1)