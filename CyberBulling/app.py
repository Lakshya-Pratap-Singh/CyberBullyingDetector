from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Load bully words from file
with open("bully_words.txt", "r") as f:
    bully_words = set([line.strip().lower() for line in f.readlines()])

# In-memory log
message_log = []

def get_severity_score(message):
    words = message.lower().split()
    flagged_words = [word for word in words if word in bully_words]
    score = len(flagged_words)
    return score, flagged_words

@app.route('/')
def index():
    return render_template('index.html', log=message_log)

@app.route('/check', methods=['POST'])
def check():
    message = request.form['message']
    score, flagged_words = get_severity_score(message)

    # Determine status and color
    if score >= 5:
        status = "⚠️ Highly Harmful"
        color = "rgba(255, 0, 0, 0.2)"
    elif score >= 2:
        status = "🚨 Harmful"
        color = "rgba(255, 165, 0, 0.2)"
    elif score > 0:
        status = "⚠️ Slightly Harmful"
        color = "rgba(255, 255, 0, 0.2)"
    else:
        status = "✅ Safe"
        color = "rgba(0, 255, 0, 0.2)"

    # Add entry to memory
    entry = {
        'message': message,
        'status': status,
        'score': score,
        'color': color,
        'flagged': flagged_words
    }
    message_log.append(entry)

    # Save to file
    with open("logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"Message: {message}\n")
        log_file.write(f"Status: {status}, Score: {score}, Flagged Words: {', '.join(flagged_words)}\n")
        log_file.write("----\n")

    return render_template('index.html', log=message_log)

@app.route('/clear', methods=['POST'])
def clear_log():
    message_log.clear()
    open("logs.txt", "w").close()  # Clear the file
    return render_template('index.html', log=message_log)

if __name__ == '__main__':
    app.run(debug=True)
