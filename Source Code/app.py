from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'
feedback_data = []
recent_issues = []  # ✅ store all submitted issues

users = {
    "sathya@gmail.com": {"name": "Sathya", "password": "1234"},
    "deepa@gmail.com": {"name": "Deepa", "password": "5678"}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.get(email)

        if user and user['password'] == password:
            session['username'] = user['name']
            flash(f"Welcome, {user['name']}!")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if email in users:
            flash("User already exists.")
            return redirect(url_for('login'))

        users[email] = {"name": name, "password": password}
        flash("Signup successful! Please login.")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    response = None
    if request.method == 'POST':
        question = request.form['question'].lower()

        if "voter" in question and "id" in question:
            response = (
                "Here's how to apply for a Voter ID:\n"
                "1. Visit the official portal: https://www.nvsp.in\n"
                "2. Click on “Form 6 – Register as a New Elector”\n"
                "3. Fill in your details like name, age, address, etc.\n"
                "4. Upload required documents (photo, proof of age, and address)\n"
                "5. Submit the form\n"
                "6. You will receive an application reference number to track status"
            )

        elif "aadhar" in question and ("correction" in question or "update" in question):
            response = (
                "To update/correct your Aadhar details:\n"
                "1. Visit: https://ssup.uidai.gov.in/ssup/\n"
                "2. Login with your Aadhar number and OTP\n"
                "3. Choose fields to update (e.g., address, name, DOB)\n"
                "4. Upload valid proof documents\n"
                "5. Submit and note the URN (Update Request Number)"
            )

        elif "pan" in question and ("apply" in question or "card" in question):
            response = (
                "To apply for a PAN card:\n"
                "1. Visit: https://www.onlineservices.nsdl.com/paam/endUserRegisterContact.html\n"
                "2. Select application type as 'New PAN – Indian Citizen'\n"
                "3. Fill the form with correct personal details\n"
                "4. Upload identity and address proof\n"
                "5. Pay the fee and submit the form\n"
                "6. You’ll receive an acknowledgment for tracking"
            )

        elif "birth" in question and "certificate" in question:
            response = (
                "To get a birth certificate:\n"
                "1. Visit your local municipal or state e-district website\n"
                "2. Fill the birth certificate application form\n"
                "3. Upload hospital birth slip or other proof\n"
                "4. Submit and download once approved"
            )

        elif "caste" in question and "certificate" in question:
            response = (
                "To apply for a caste certificate:\n"
                "1. Visit your state’s MeeSeva or eDistrict portal\n"
                "2. Login or register as a citizen\n"
                "3. Fill in caste details and upload required proof\n"
                "4. Submit the application and note the reference number\n"
                "5. Once approved, download the certificate online"
            )

        else:
            response = (
                "Sorry, I didn't understand that.\n"
                "You can ask about: Voter ID, Aadhar update, PAN card, Birth Certificate, or Caste Certificate."
            )

    return render_template('chat.html', response=response)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    sentiment = None
    if request.method == 'POST':
        user_feedback = request.form['feedback'].lower()
        if any(word in user_feedback for word in ["good", "great", "awesome", "helpful", "love"]):
            sentiment = "Positive 😊"
        elif any(word in user_feedback for word in ["bad", "poor", "worst", "hate", "slow"]):
            sentiment = "Negative 😞"
        else:
            sentiment = "Neutral 😐"
        feedback_data.append(sentiment)
    return render_template('feedback.html', sentiment=sentiment)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash("Please log in to view the dashboard.")
        return redirect(url_for('login'))

    sentiment_counts = {
        'positive': feedback_data.count("Positive 😊"),
        'neutral': feedback_data.count("Neutral 😐"),
        'negative': feedback_data.count("Negative 😞")
    }
    return render_template('dashboard.html', sentiments=sentiment_counts, issues=recent_issues)

@app.route('/report-issue', methods=['POST'])
def report_issue():
    if 'username' not in session:
        flash("Please log in to report an issue.")
        return redirect(url_for('login'))

    issue = request.form['issue'].strip()
    if issue:
        recent_issues.append(issue)
        flash("Your issue has been submitted.")
    else:
        flash("Issue cannot be empty.")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
