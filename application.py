from flask import Flask, request, render_template, jsonify
import traceback
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

## Route for home page
@app.route('/')
def index():
    return render_template('index.html')

## Route for prediction
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            print("Form values:", request.form)

            # Collecting data from form inputs
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental level of education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test preparation course'),
                reading_score=float(request.form.get('reading score')),
                writing_score=float(request.form.get('writing score'))

            )

            # Convert input data to DataFrame
            pred_df = data.get_data_as_data_frame()
            print("Input DataFrame:\n", pred_df)

            # Prediction pipeline
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)

            print("Prediction result:", results)

            return render_template('home.html', results=results[0])

        except Exception as e:
            print("Error occurred during prediction:\n", traceback.format_exc())
            return render_template('home.html', results="Prediction Failed")

if __name__ == "__main__":
    app.run(debug=True)  # Turn on debug mode for detailed errors
