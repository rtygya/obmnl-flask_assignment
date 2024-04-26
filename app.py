# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/", methods = ['GET'])
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Search transactions
@app.route("/search", methods = ['GET', 'POST'])
def search_transactions():
    if request.method == "POST":
        min = float(request.form['min_amount'])
        max = float(request.form['max_amount'])
        filtered_transactions = [t for t in transactions if (t['amount'] >= min and t['amount'] <= max)]
        return render_template("transactions.html", transactions=filtered_transactions)
    if request.method == "GET":
        return render_template("search.html")

# Create operation: Add transaction
@app.route("/add", methods = ['GET', 'POST'])
def add_transaction():
    if request.method == "POST":
        # Create a new transaction object using form field values
        t = {
              'id': len(transactions)+1,
              'date': request.form['date'],
              'amount': float(request.form['amount'])
        }
        # Append the new transaction to the list
        transactions.append(t)

        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))
    if request.method == "GET":
        # Render the form template to display the add transaction form
        return render_template("form.html")
        

# Update operation: Edit existing transaction
@app.route("/edit/<int:transaction_id>", methods = ['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == "POST":
        # Extract the updated values from the form fields
        date = request.form['date']
        amount = float(request.form['amount'])

        # Find the transaction with the matching ID and update its values
        for t in transactions:
            if t['id'] == transaction_id:
                t['date'] = date
                t['amount'] = amount
                break
        
        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))

    if request.method == "GET":
        # Find the transaction and display 
        for t in transactions:
            if (t['id'] == transaction_id):
                return render_template("edit.html", transaction=t)
        

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from list
    for t in transactions:
        if t['id'] == transaction_id:
            transactions.remove(t)
            break
        
    # Redirect to the transactions list page
    return redirect(url_for("get_transactions"))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)    