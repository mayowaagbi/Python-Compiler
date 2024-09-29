# Overview 


# Setting Up the Virtual Environment (venv)
## Step 1: Create a Virtual Environment
Navigate to your project directory where you want the virtual environment to be created:

`cd /path/to/project-directory`  
Create the virtual environment using the following command:

`python -m venv venv`  
This will create a new directory called venv in your project folder, which contains the isolated environment.

## Step 2: Activate the Virtual Environment
For Windows: Run the following command to activate the virtual environment:

`venv\Scripts\activate`    

For macOS/Linux: Use this command to activate the virtual environment:   

`source venv/bin/activate`

Once activated, you should see (venv) at the beginning of your terminal prompt.

## Step 3: Install Dependencies
After activating the virtual environment, you can install the necessary dependencies (like PLY) inside this environment.

Install PLY inside the virtual environment:

`pip install ply`

## Step 4: Running the Lexer in the Virtual Environment
After setting up the environment and installing dependencies:

Ensure the virtual environment is activated. If not, run the activation command from Step 2.

Run your lexer.py file:

`python lexer.py`

Now the lexer will execute using the isolated Python environment from the virtual environment you created.

Deactivating the Virtual Environment
To deactivate the virtual environment, simply run the command:

`deactivate`

This will return you to the system's default Python environment.

# Setup Instructions      
## Step 1: Install PLY
First, make sure you have the PLY library installed. If not, install it using pip:

`pip install ply`

## Step 2: Clone or Download the Project
Clone this repository or download the project files to your local machine.

## Step 3: Running the Lexer
Navigate to the project directory where your lexer.py file is located.

### Example:

`cd /path/to/project-directory`
Run the lexer script: Use Python to run the lexer.py script:


`python lexer.py`
Testing the Lexer
The lexer.py script contains a test_lexer() function. This function takes a block of code as input, tokenizes it using the lexer, and prints the tokens.

After running the script, the lexer will output tokens that represent the structure of the input code.

Requirements
Python 3.x (Make sure Python is installed and set up on your machine)
PLY library (installed via pip as described in Step 1)
