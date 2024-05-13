from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
def home():
    html = """ <html>
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

            .success-message {
                color: green; /* Green text */
                display: none; /* Initially hidden */
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            body {
                /* Replace 'background.jpg' with the path to your image */
                /* background-image: url('/image/DMR.png'); */
                background-image: url("{{ url_for('images', filename='DMR.png') }}");
                background-repeat: no-repeat;
                background-size: cover; /* Resize the background image to cover the entire container */
            }

        </style>
        <script>
            function showSpinner() {
                var btn = document.getElementById('invite-button');
                var spinner = document.getElementById('spinner');
                btn.disabled = true; // disable the button
                spinner.style.display = 'inline-block'; // show the spinner

                // Simulate an asynchronous operation (e.g., inviting the bot to the server)
                setTimeout(function() {
                    spinner.style.display = 'none'; // hide the spinner
                    successMessage.style.display = 'block'; // show the success message
                }, 2000); // 2 seconds delay
            }
        </script>
    </head>
    <body style="text-align: center; padding-top: 30px;">
    
        <h2>Welcome to DMR Bot!</h2>
        
        <p>Join us and explore the possibilities!</p>
        
        <a href="https://discord.com/oauth2/authorize?client_id=836219688164917338" target="_blank">
        
            <button id="invite-button" class="invite-button" onclick="showSpinner()">Invite Bot to Server</button>
            
            <div id="spinner" class="spinner"></div>

            <p id="success-message" class="success-message">Bot successfully invited to server!</p>

        </a>
    </body>
</html> """
    return render_template_string(html)
