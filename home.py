from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
def home():
    html = """
    <html>
        <head>
            <style>
                body {
                    background-color: #F0F0F0; /* Light grey background */
                    font-family: Arial, sans-serif; /* Modern font */
                }
                h2 {
                    color: #333; /* Dark grey text */
                }
                p {
                    color: #666; /* Medium grey text */
                }
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
                }
            </style>
        </head>
        <body style="text-align: center; padding-top: 30px;">
            <h2> dmr bot </h2>
            <p>invite link !</p>
            <a href="https://discord.com/oauth2/authorize?client_id=836219688164917338" target="_blank">
                <button class="invite-button">Invite Bot to Server</button>
            </a>
        </body>
    </html>
    """
    return render_template_string(html)
