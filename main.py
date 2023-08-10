from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
#We are creating a querry to creating the table and table columns(3 column)

#we are connecing to the database we created above
conn = sqlite3.connect('items.db')

conn.execute('''
  
  CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
  )
''')



@app.route('/') 
def index():
    conn = sqlite3.connect('items.db')

    # Retrieve all items from the database
    cursor = conn.execute('SELECT * FROM items')
    items = cursor.fetchall()
  #we are displaying all the items from the database to html.
    return render_template('index.html', items=items)

@app.route('/create', methods=['GET', 'POST'])
def create():
  #getting user data
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        # Insert the new item into the database
        conn = sqlite3.connect('items.db')
        conn.execute('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
        conn.commit()
        
        return redirect(url_for('index'))
    
    return render_template('create.html')
  
#we are editing our items
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    conn = sqlite3.connect('items.db')
    cursor = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    item = cursor.fetchone()
        # Handle the form submission for editing the item
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        # Update the item in the database
        conn.execute('UPDATE items SET name = ?, description = ? WHERE id = ?', (name, description, item_id))
        conn.commit()
        
        return redirect(url_for('index'))
    
    return render_template('edit.html', item=item)
  
#we are posting the item we want to delete.
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    # Delete the item from the database
    conn = sqlite3.connect('items.db')
    conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
        # Redirect to the home page after deleting the item
    return redirect(url_for('index'))
#we are executing the app to run
app.run(host='0.0.0.0', port=8080)