<h1> Dashboard using Flask</h1>
<br>
<p>
    This app uses Flask as the framework for web-development.
    <br>    
    <small>
        (I have attached "data.csv" file from the required (<a href="https://raw.githubusercontent.com/mengchoontan/school-239/master/complaints-2020-02-08_03_28.csv">link</a>) and the other file is "footballersComplaints.csv" slightly custom modified by me to select file)
    </small>

</p>
<div>
    <h3>Setting up a development environment</h3>
   
    # Clone the code repository
    git clone https://github.com/shahan007/SUSS-FlaskDashboard
    
    # Create virtual environment
    python -m venv venv
    
    # Install required dependencies
    pip install -r requirements.txt    
</div>
<br>
<div>
    <h3>Running the app</h3>
    
    #setting environment variables
    export FLASK_APP=run.py
    export FLASK_DEBUG=1 (optional)
    
    #run the file
    flask run
</div>
<br>
<div>
    <h3 style='font-weight:650;text-decoration:underline;'>Breif App Info:</h3>
    <p>    
        <strong>appProject</strong> package contains all the files required for the development of this app.
        <br>
        App's configuration is stored in config.py.
        <br>
        Data used by the app for charting and its interface is stored in ./data/files directory (stores all the file after successfull upload).
        <br>
        DataSource & Feedback models have already been created and stored in ./data/data/data.sqlite.    
        <br>    
        App relies on pandas for data analysis and Flask-Sqlalchemy & Flask-Migrate for storing and migration of data models.
        <p><span style='color:orange;'
    </p>
</div>
<br>
<div>
    <h3 style='font-weight:650;text-decoration:underline;'>Application Interface :</h3>      
    <p>
        When the file is first run this app will show top 10 banks using the entire file.
        <br>        
        When the drop-down menu is clicked app will update the <i>"blue-text"</i> and fetch the data accordingly for charting.    
    </p>
    <p>
        <span style='text-decoration:underline;font-weight:500;'>Upload feature:</span>
        <br>        
        App also allows to upload <i>one</i> or <strong><i>multiple</i></strong> file(s) for charting. To confirm upload user must click submit button.<br>
        There is also a message box below submit button. If a file already exsist in the database or
        the file is of invalid extension respective error message will be displayed in the message box.<br>
        If any of the file has been successfully uploaded an appropiate message will be displayed in the message box.
        <br>
        <span style='font-weight:600;color:#ff5722 ;font-size:18px;'>! Valid file extensions</span> <span style='color:green;font-weight:550;font-style:italic;'> ---> ".tx",".csv"</span> (i trust the user will upload delimited .txt file)        
    </p>    
    <p>
        During the uploading phase successfuly uploaded files relative information as described in 
        the DataSource model will be stored. The feedback data and relative column as defined in Feedback model is also stored in the Feedback model from the uploaded file.<br>
        When file(s) has/have been successfuly uploaded, app will update the interface (charts & dropdown) using the data of the latest file that has been uploaded & stored (in ./data./file), retrieving file info from (DataSource model) to update the interface.
    </p>
    <p>
        <span style='text-decoration:underline;font-weight:500;'>Listing File Names feature:</span><br>
        App will always be showcasing all the files stored in the app near the bottom of the sidebar.<br>
        <span style='color : green;font-style:italic;text-decoration:underline;font-weight:480;'>
            In addition, to make this app more user-friendly, a user can click on a filename which will also update the user-interface (drop-down & chart) using the data of that selected filename !
        </span>
    </p>
</div>
