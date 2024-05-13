from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
def home():
    html = """
    <html>
        <body style="text-align: center; padding-top: 30px;">
            <h2>Welcome to My Website!</h2>
            <p>invite!</p>
            <a href="https://discord.com/oauth2/authorize?client_id=836219688164917338" target="_blank">
                <button>invite bot to Server</button>
            </a>
        </body>
    </html>
    """
    return render_template_string(html)
