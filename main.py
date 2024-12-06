import tkinter as tk
import random
from tkinter import messagebox

# The paragraph used to extract random words for the typing test
# This is the paragraph that you can change If you want other words generated
paragraph = """The Clown Car invariably drives toward addiction, narcissism, and
 compulsion. People whose minds are Clown Cars are easily manipulated
 by whatever person or group makes them feel good consistently whether
 it is a religious leader, politician, self help guru, or sinister internet forum.
 A Clown Car will gladly steamroll other Consciousness Cars i.e., other
 people with its big, red rubbery tires because its Thinking Brain will
 justify this by saying they deserved it,they were evil, inferior, or part of
 some made up problem.
 Some Clown Cars merely drive toward fun they’re all about drinking
 and fucking and partying. Others drive toward power. These are the most
 dangerous Clown Cars, as their Thinking Brains set to work justifying
 their abuse and subjugation of others through intellectual sounding
 theories about economics, politics, race, genetics, gender, biology, history,
 and so on. A Clown Car will sometimes pursue hate, too, because hate
 brings its own odd satisfaction and self assurance. Such a mind is prone to
 self righteous anger, as having an external target reassures it of its own
 moral superiority. Inevitably, it drives toward the destruction of others
 because it is only through the destruction and subjugation of the outer
 world that its endless inner impulses can be satisfied.
 It is hard to pull someone out of the Clown Car once they are in it. In the
 Clown Car, the Thinking Brain has been bullied and abused by the Feeling
 Brain for so long that it develops a sort of Stockholm syndrome it can not
 imagine a life beyond pleasing and justifying the Feeling Brain. It can not
 fathom contradicting the Feeling Brain or challenging it on where it is
 going, and it resents you for suggesting that it should. With the Clown Car,
 there is no independent thought and no ability to measure contradiction or
 switch beliefs or opinions. In a sense, the person with a Clown Car mind
 ceases to have an individual identity at all.
 This is why cultish leaders always start by encouraging people to shut
 off their Thinking Brains as much as possible. Initially, this feels profound
to people because the Thinking Brain is often correcting the Feeling Brain,
 showing it where it took a wrong turn. So, silencing the Thinking Brain
 will feel extremely good for a short period. And people are always
 mistaking what feels good for what is good.
"""

# Preprocess the paragraph to clean and normalize text
paragraph = paragraph.replace(".", "")
paragraph = paragraph.replace("’", " ")
paragraph = paragraph.replace(",", "")
paragraph = paragraph.replace(":", "")
paragraph = paragraph.replace('"', '')
paragraph = paragraph.replace("\n", " ")
paragraph = paragraph.replace("?", "").lower()
words = paragraph.split(" ")  # Split paragraph into individual words
unique = list(set(words))  # Get a list of unique words

# Randomly select 200 unique words for the typing test
random_words = random.sample(unique, 200)

# Define font style for UI elements
font = ("Helvetica", 24)

# Create the main application window
window = tk.Tk()
window.title("Typing Speed Test")
window.config(padx=100, pady=100)

# Canvas to display instructions and timer
canvas = tk.Canvas(window, width=600, height=400)
canvas.pack()
c_text = canvas.create_text(
    300, 200,
    text="How many words can you \ntype correctly in 1 minute?\n"
         "Press 'Start!' button to begin the test...\n"
         "Press 'enter' to load more words.",
    fill='black', font=font
)
timer_text = canvas.create_text(300, 50, text="1:00", fill="black", font=('Helvetica', 35))

# Entry widget for typing input
entry = tk.Entry(window, width=50, font=("Helvetica", 24))
entry.pack(padx=20, pady=20)

# Global variables
current_index = 0
words_to_type = []
total_score = 0


def calculate_score():
    """
    Calculates the number of correct words typed by the user.
    Returns the score for the current batch of words.
    """
    typed_text = entry.get().strip()
    typed_words = typed_text.split()
    correct_words = [word for word in typed_words if word in words_to_type[:5]]
    return len(correct_words)


def end_game():
    """
    Ends the game, displays the total score, and resets the UI.
    """
    global total_score
    score = calculate_score()
    total_score += score
    messagebox.showinfo("Time's up!", f"Your total score: {total_score} correct words in 1 minute.")
    entry.delete(0, tk.END)
    canvas.itemconfig(c_text, text="How many words can you \ntype correctly in 1 minute?\n"
                                   "Press 'Start!' button to begin the test...")
    canvas.itemconfig(timer_text, text="1:00", font=('Helvetica', 35))
    total_score = 0


def timer(count):
    """
    Countdown timer that updates the canvas every second.
    Ends the game when the timer reaches zero.
    """
    seconds = count % 60
    canvas.itemconfig(timer_text, text=f"{seconds:02}")
    if count > 0:
        window.after(1000, timer, count - 1)
    else:
        end_game()


def start_game():
    """
    Starts the typing speed test by resetting variables and displaying the first batch of words.
    """
    global current_index, words_to_type, total_score
    current_index = 0
    total_score = 0
    entry.delete(0, tk.END)
    entry.focus()
    words_to_type = random_words[:20]
    display_words = ' '.join(words_to_type[:5])
    canvas.itemconfig(c_text, text=display_words)
    timer(60)


def update_words(event):
    """
    Loads the next batch of words when the user presses Enter.
    Updates the total score and displayed words.
    """
    global current_index, words_to_type, total_score
    score = calculate_score()
    total_score += score
    current_index += 5
    if current_index < len(random_words):
        words_to_type = random_words[current_index:current_index + 20]
        display_words = ' '.join(words_to_type[:5])
        canvas.itemconfig(c_text, text=display_words)
        entry.delete(0, tk.END)


# Button to start the game
btn = tk.Button(window, text="Start!", command=start_game, font=font)
btn.pack()

# Bind the Enter key to load the next batch of words
entry.bind("<Return>", update_words)

# Run the application
window.mainloop()
