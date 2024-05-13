from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
def home():
    html = """
<html>
    <head>
        <style>
            .invite-button {
                background-color: #007BFF; /* Blue background */
                color: white; /* White text */
                border: none; /* Remove default button border */
                padding: 15px 32px; /* Increase button size */
                text-align: center; /* Center button text */
                text-decoration: none; /* Remove default button underline */
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 4px; /* Rounded button corners */
                transition: background-color 0.3s, transform 0.3s; /* Transition effects */
            }

            .invite-button:hover {
                background-color: #0056b3; /* Darker blue background on hover */
            }

            .invite-button:active {
                transform: scale(0.95); /* Slightly reduce size when clicked */
            }
        </style>
    </head>
    <body style="text-align: center; padding-top: 30px;">
        <h2>Welcome to My Modern Website!</h2>
        <p>Join us and explore the possibilities!</p>
        <a href="https://discord.com/oauth2/authorize?client_id=836219688164917338" target="_blank">
            <button class="invite-button">Invite Bot to Server</button>
        </a>
    </body>
</html>
    """
    return render_template_string(html)
