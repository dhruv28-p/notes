from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import pymysql
import io

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL database configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'dhruv@2808',
    'database': 'notelab'
}

@app.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("All fields are required!", "error")
            return redirect(url_for("login_page"))

        try:
            # Connect to the database
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()

            # Check if the user is an admin
            cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
            admin_row = cursor.fetchone()

            if admin_row:
                session['username'] = username
                session['role'] = 'admin'
                flash(f"Welcome, Admin {username}!", "success")
                return redirect(url_for("admin_page"))

            # Check if the user is a regular user
            cursor.execute("SELECT * FROM user WHERE username=%s AND password=%s", (username, password))
            user_row = cursor.fetchone()

            if user_row:
                session['username'] = username
                session['role'] = 'user'
                flash(f"Welcome, {username}!", "success")
                return redirect(url_for("user_page"))

            flash("Invalid Username or Password!", "error")
            return redirect(url_for("login_page"))

        except Exception as e:
            flash(f"Error connecting to the database: {str(e)}", "error")
            return redirect(url_for("login_page"))

        finally:
            connection.close()

    return render_template("login.html")

@app.route("/admin", methods=["GET", "POST"])
def admin_page():
    if 'role' in session and session['role'] == 'admin':
        if request.method == "POST":
            if 'file' not in request.files:
                flash("No file selected for upload!", "error")
                return redirect(url_for("admin_page"))

            file = request.files['file']
            if file:
                try:
                    connection = pymysql.connect(**db_config)
                    cursor = connection.cursor()

                    # Insert file data into the database
                    cursor.execute(
                        "INSERT INTO file (filename, filedata) VALUES (%s, %s)",
                        (file.filename, file.read())
                    )
                    connection.commit()
                    flash("File uploaded successfully!", "success")
                except Exception as e:
                    flash(f"Error uploading file: {str(e)}", "error")
                finally:
                    connection.close()

        # Fetch all uploaded files from the database
        try:
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT id, filename FROM file")
            files = cursor.fetchall()
        except Exception as e:
            flash(f"Error fetching files: {str(e)}", "error")
            files = []
        finally:
            connection.close()

        return render_template("admin.html", files=files)

    flash("Unauthorized access!", "error")
    return redirect(url_for("login_page"))

@app.route("/user")
def user_page():
    if 'role' in session and session['role'] == 'user':
        # Fetch all uploaded files from the database
        try:
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT id, filename FROM file")
            files = cursor.fetchall()
        except Exception as e:
            flash(f"Error fetching files: {str(e)}", "error")
            files = []
        finally:
            connection.close()

        return render_template("home.html", files=files)

    flash("Unauthorized access!", "error")
    return redirect(url_for("login_page"))

@app.route("/download/<int:file_id>")
def download_file(file_id):
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT filename, filedata FROM file WHERE id=%s", (file_id,))
        file = cursor.fetchone()

        if file:
            filename, filedata = file
            return send_file(
                io.BytesIO(filedata),
                as_attachment=True,
                download_name=filename
            )
        else:
            flash("File not found!", "error")
    except Exception as e:
        flash(f"Error downloading file: {str(e)}", "error")
    finally:
        connection.close()

    return redirect(url_for("admin_page" if session.get("role") == "admin" else "user_page"))

@app.route("/home")
def dashboard_page():
    return render_template("home.html")

@app.route('/cs')
def computer_science():
    return render_template('cs.html')  # Ensure cs.html exists in templates folder.

@app.route('/cyber')
def cyber_security():
    return render_template('cyber.html')  # Ensure cyber.html exists in templates
@app.route("/logout")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login_page"))


if __name__ == "__main__":
    app.run(debug=True)


