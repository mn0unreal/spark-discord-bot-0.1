from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
def home():
    html = """ <html>
    <head>
        <style>
            /* ...existing CSS... */

            /* CSS for the spinner */
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #3498db;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                animation: spin 2s linear infinite;
                display: none;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
        <script>
            function showSpinner() {
                var btn = document.getElementById('invite-button');
                var spinner = document.getElementById('spinner');
                btn.disabled = true; // disable the button
                spinner.style.display = 'inline-block'; // show the spinner
            }
        </script>
    </head>
    <body style="text-align: center; padding-top: 30px;">
        <h2>Welcome to My Modern Website!</h2>
        <p>Join us and explore the possibilities!</p>
        <a href="https://discord.com/oauth2/authorize?client_id=836219688164917338" target="_blank">
            <button id="invite-button" class="invite-button" onclick="showSpinner()">Invite Bot to Server</button>
            <div id="spinner" class="spinner"></div>
        </a>
    </body>
</html> """
    return render_template_string(html)
