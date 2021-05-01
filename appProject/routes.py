import os
from appProject import app , db
from flask import (render_template , request , make_response , jsonify , session)
from werkzeug.utils import secure_filename
from appProject.analysisWithPandas import (getDropDowns , getMeData , getMeWordCloudData)
from appProject.models import DataSource , Feedback
import pandas as pd
import random

# function to check for valid file extension
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Renders index.html
@app.route('/')
def index():
    filename = DataSource.query.order_by(DataSource.dateUploaded.desc()).first().fileName
    filePath = f'./data/files/{filename}'
    banks , periods = getDropDowns(filePath)
    session['fileSelected'] = filename
    return render_template('index.html',banks=banks,periods=periods)

# Responsible for charting
@app.route('/charting',methods=['POST'])
def data():
    response = request.get_json()    
    percent  = response.get('selectedPercent') or 'All'
    bank     = response.get('selectedBank')  or 'All'
    period   = response.get('selectedPeriod') or 'All'    
    filename = response.get('filename') or DataSource.query.order_by(
    	DataSource.dateUploaded.desc()).first().fileName           
    data     = getMeData(percent,bank,period,filePath=f'./data/files/{filename}')
    data     = make_response(data)
    data.content_type = 'application/json'        
    return data

#Responsible for uploading   
@app.route('/uploadFile', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'Error:': 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('files[]')
    errors  = {}
    success = False    

    for file in files:
        #checks if there is a file and belongs to a valid file extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            session['fileSelected'] = filename
            #checks if file exsists in the DataSource model
            if not DataSource.query.filter_by(fileName = filename).first():
                datasrc = DataSource(fileName=filename, fileDescription = f"This is a file. Name is {filename}")                                
                db.session.add(datasrc)
                db.session.commit()                                
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))                                
                feedback_list = []
                df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename),encoding="ISO-8859-1")
                for i in range(len(df)):
                    row = df.iloc[i]
                    feedback_instace = Feedback(
                        customerName = row['Company'],
                        feedbackInformation = row['Consumer complaint narrative'],
                        feedbackType = None                        
                    )
                    feedback_list.append(feedback_instace)
                datasrc.feedbacks = feedback_list                
                db.session.commit()                
                success = True            
            else:
                errors[file.filename] = 'File already exsists in DataBase'   
        else:
            errors[file.filename] = 'File type is not allowed'
    #If file uploaded successfully & there are error as well
    if success and errors:
    	errors['message'] = 'File(s) successfully uploaded'
    	resp = jsonify(errors)
    	resp.status_code = 206
    	return resp
    #If all files have been uploaded successfully
    if success:
    	resp = jsonify({'message': 'All Files are successfully uploaded'})
    	resp.status_code = 201
    	return resp
    else:
    	resp = jsonify(errors)
    	resp.status_code = 400
    	return resp

#Responsible for returning back all the files that exists in the database
@app.route("/listFiles")
def list_files():
    """Endpoint to list files on the server."""
    files = DataSource.query.order_by(DataSource.dateUploaded.desc()).all()
    files = [f.fileName for f in files]    
    return jsonify(files)

#Responsible for returning banks and periods for the selected file
@app.route('/getLatestDropDown',methods=['GET'])
def getLatestDropDown():
    filename = request.args.get('filename') or DataSource.query.order_by(DataSource.dateUploaded.desc()).first().fileName
    session['fileSelected'] = filename
    filePath = f'./data/files/{filename}'
    banks , periods = getDropDowns(filePath)
    response = {'banks':banks,'periods':periods}
    return jsonify(response)

# Responsible for charting Word Cloud
@app.route('/chartCloudData')
def chartCloudData():
    # get the filname which is then going to be used for charting
    # very crucial. This allows me to train the data of the selected
    # file in q2, making it very modular.
    
    filename  = session['fileSelected']
    try:    
        feedbacks = DataSource.query.filter_by(fileName = filename)\
                            .first().feedbacks.all()        
        if not feedbacks:
            raise Exception        
    except:
        return jsonify('<ERROR>') , 500
    # we get the feedback information stored in the feedback instance
    # of the data source file    
    data = []
    for f in feedbacks:
        data.append(f.feedbackInformation)  
    try:
        array= getMeWordCloudData(data)
    except:
        return jsonify('<ERROR>') , 500
    return jsonify(array)

# Responsible for charting Sample Data Table
@app.route('/chartSampleDataTable')
def chartSampleDataTable():
    # get the filname which is then going to be used for charting
    # very crucial. This allows me to train the data of the selected
    # file in q2, making it very modular.    
    
    filename  =  session['fileSelected']
    try:
        # get back top 100 feedbacks of the file from backend model
        feedbacks = DataSource.query.filter_by(fileName = filename)\
                                .first().feedbacks.all()[:100]
        if not feedbacks:
            raise Exception
    except:
        return jsonify('<ERROR>') , 500
    data = []
    # randomly assign a “Positive” or “Negative” value to each of the feedback.    
    for f in feedbacks:
        data.append([f.feedbackInformation,random.choice(['Negative','Positive'])])       
    return jsonify(data)

# Responsible to update the refresh the Sample Data Tab.
# This will refresh the Sample Data Tab on fly with the data of  trained file.
@app.route('/changeFileSelectedAfterTrain')
def changeFileSelectedAfterTrain():
    # This  ensure that when the Sample Data tab is 
    # clicked the data used to process & chart the table
    # will be of the data source file that was clicked in the upload ui.    
    session['fileSelected'] =  request.args.get('fileSelected')
    return jsonify('Success')
