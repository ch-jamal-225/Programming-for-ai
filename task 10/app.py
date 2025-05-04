from flask import Flask, render_template, request, jsonify
import re
import random

app = Flask(__name__)

pairs = [
    [r"(?i).*hello.*|.*hi.*|.*hey.*",
     ["Hello! How can I assist you with admissions?",
      "Hi there! Do you need admission information?",
      "Hey! Welcome to Superior University Admissions, how can I help?"]],

    [r"(?i).*programs.*offer.*|.*degree programs.*|.*courses available.*",
     ["Superior University offers undergraduate, graduate, and PhD programs in Engineering, Business, IT, Social Sciences, and more.",
      "We offer a variety of programs, including BS, MS, and PhD in multiple fields. You can visit our website for a complete list.",
      "Our university provides degrees in disciplines such as Computer Science, Business Administration, Media Studies, and Engineering."]],

    [r"(?i).*admission requirements.*|.*entry requirements.*|.*eligibility.*",
     ["Admission requirements vary by program. Generally, you need academic transcripts, an entry test (if applicable), and supporting documents.",
      "You must have the required qualifications based on your desired program. Some programs also require an entry test.",
      "Each program has specific requirements. Visit our website or contact the admission office for details."]],

    [r"(?i).*apply.*admission.*|.*admission process.*|.*steps to apply.*",
     ["You can apply online through the official Superior University website or visit the admission office for assistance.",
      "The admission process is simple: fill out the online application form, submit required documents, and appear for an entry test (if required).",
      "To apply, visit our website, choose your program, and follow the instructions to complete the application process."]],

    [r"(?i).*last date.*apply.*|.*admission deadline.*|.*when.*admission.*close.*",
     ["Admission deadlines vary each semester. Please check the official website or contact the admission office for updated information.",
      "The last date to apply depends on the academic session. Keep an eye on our website for important dates.",
      "Superior University announces deadlines for each intake separately. Visit our admissions page for the latest updates."]],

    [r"(?i).*bye.*|.*goodbye.*|.*see you later.*",
     ["Goodbye! Feel free to ask anytime.",
      "See you later! Good luck with your admission.",
      "Alright, take care! Let us know if you have more questions."]]
]

def get_response(user_input):
    for pattern, responses in pairs:
        if re.search(pattern, user_input):
            return random.choice(responses)
    return "I'm sorry, I don't have information on that. Please ask about university admissions."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]
    response = get_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

