from flask import Flask, render_template, request, redirect
import pickle
import os

app = Flask(__name__)

DATA_FILE = "todo_data.pkl"

# Load saved data if available
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "rb") as f:
        todo_list = pickle.load(f)
else:
    todo_list = []   # A list of dicts: {task, email, priority}

# Main Page
@app.route("/")
def index():
    return render_template("index.html", items=todo_list)

# Add New To Do Item
@app.route("/submit", methods=["POST"])
def submit():
    task = request.form.get("task", "").strip()
    email = request.form.get("email", "").strip()
    priority = request.form.get("priority", "").strip()

    # Validation
    if "@" not in email or priority not in ["Low", "Medium", "High"]:
        return redirect("/")

    todo_list.append({
        "task": task,
        "email": email,
        "priority": priority
    })

    return redirect("/")

# Delete a Single Item
@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    if 0 <= index < len(todo_list):
        del todo_list[index]
    return redirect("/")

# Clear List
@app.route("/clear", methods=["POST"])
def clear():
    todo_list.clear()
    return redirect("/")

# Save List to File (Extra Credit)
@app.route("/save", methods=["POST"])
def save():
    with open(DATA_FILE, "wb") as f:
        pickle.dump(todo_list, f)
    return redirect("/")


# Run App
if __name__ == "__main__":
    app.run(debug=True)