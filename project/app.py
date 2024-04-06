from flask import Flask, render_template, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('construction_dataset1.csv')

# Feature engineering: Convert categorical variables into dummy/indicator variables
df = pd.get_dummies(df, columns=['Location', 'Type', 'Soil Type', 'Period of the Month', 'Number of Floors'])

# Split the dataset into features and target variable
X = df.drop(['Project Name', 'Time Spent (Months)'], axis=1)
y = df['Time Spent (Months)']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Function to visualize time spent on 10 last projects
def visualize_last_projects():
    # Assuming `last_projects_data` contains data of the last 10 projects
    # Replace this with actual data retrieval logic
    
    # Sample data
    last_projects_data = {
        'Project Name': ['Project 1', 'Project 2', 'Project 3', 'Project 4', 'Project 5', 
                         'Project 6', 'Project 7', 'Project 8', 'Project 9', 'Project 10'],
        'Time Spent (Months)': [12, 15, 10, 18, 20, 14, 16, 13, 17, 19]
    }
    
    # Plotting the time spent on last projects
    plt.figure(figsize=(8, 6))
    plt.barh(last_projects_data['Project Name'], last_projects_data['Time Spent (Months)'], color='skyblue')
    plt.xlabel('Time Spent (Months)')
    plt.ylabel('Project Name')
    plt.title('Time Spent on Last 10 Projects')
    plt.gca().invert_yaxis()  # Invert y-axis to display projects from top to bottom
    plt.savefig('static/last_projects_plot.png')  # Save the plot as a static file

# Function to predict time spent based on user input
@app.route('/', methods=['GET', 'POST'])
def predict_time_spent():
    if request.method == 'POST':
        # Retrieve user input from form
        location = request.form['location']
        project_type = request.form['project_type']
        square_meters = float(request.form['square_meters'])
        num_rooms = int(request.form['num_rooms'])
        soil_type = request.form['soil_type']
        budget = float(request.form['budget'])
        period_of_month = request.form['period_of_month']
        num_floors = request.form['num_floors']  # No need to convert to int here
        
        # Create a DataFrame with user input
        user_data = pd.DataFrame({'Location': [location], 'Type': [project_type], 'Square Meters': [square_meters],
                                  'Number of Rooms': [num_rooms], 'Soil Type': [soil_type], 'Budget': [budget],
                                  'Period of the Month': [period_of_month], 'Number of Floors': [num_floors]})
        
        # Convert categorical variables into dummy/indicator variables
        user_data = pd.get_dummies(user_data)
        
        # Align user input data with the columns used during model training
        missing_cols = set(X_train.columns) - set(user_data.columns)
        for col in missing_cols:
            user_data[col] = 0
        
        # Ensure the order of columns is consistent with model training data
        user_data = user_data[X_train.columns]
        
        # Make predictions
        prediction = model.predict(user_data)
        
        # Display the predicted time spent
        return render_template('result.html', prediction=prediction[0])

    return render_template('index.html')

if __name__ == '__main__':
    visualize_last_projects()  # Visualize last projects before running the app
    app.run(debug=True)
