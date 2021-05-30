<h1> Dashboard using Flask</h1>
<br>
<p>
    This app uses Flask as the framework for web-development.
    <br>    
    <small>
        (I have attached "data.csv" file from the required (<a href="https://raw.githubusercontent.com/mengchoontan/school-239/master/complaints-2020-02-08_03_28.csv">link</a>) and the other file is "footballersComplaints.csv" slightly custom modified by me to see the changes and stuff)
    </small>

</p>
<div>
    <h3 style='font-weight:650;text-decoration:underline;'>Setting up a development environment</h3>
    
    # Clone the code repository
    git clone https://github.com/lingthio/Flask-User-starter-app.git

    # Create virtual environment
    python -m venv venv

    # Install required dependencies
    pip install -r requirements.txt
    
</div>

```python
def hello():
    print('hello')
```

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
        <p><span style='color:orange;'>Major App Upgrade:</span><br> From the discussion forums and this ECA which asked us to query from models, I made use of Feedback model.<br>DataSource Model Stores the files uploaded information with relationship to Feedback model (one-to-many) where the Feedback model stores all the feedback information from  the file that is uploaded. Feedback model has a "datasrc_id" ForeignKey that contains the data file id it belongs to.</p>           
    </p>
</div>
<br>
<div>
    <h3 style='font-weight:650;text-decoration:underline;'>Application Interface :</h3>      
    <div style='border:1px solid orange;padding:2%;'>         
        <p style='color:orange;font-weight:bolder;'>
            New Features and Assumptions demanded by ECA:                                    
        </p>
        <ul>
            <span style="font-weight:bolder;text-decoration:underline;">Word Cloud Tab</span>
            <li>
                Once Clicked on Word Cloud tab it will chart "word cloud" for the keywords.<br>
                I query the feedbacks from the data source model for the latest uploaded file / selected file.<br>
                For this I show top 100, most frequently used words in complaints. I did the cleaning and filter out words which are not considered as keywords for any business feedback for the management.Then using the finalised formatted data I send it to front-end and charted it.
                <br>
                <br>
            </li>            
            <span style="font-weight:bolder;text-decoration:underline;">Sample Data Tab</span>
            <li>
                Once Clicked on Sample Data Tab it will dynamically chart the table.<br>
                I query the feedbacks from the data source model for the latest uploaded file / selected file. As asked I generate either 'Positive' or 'Negative' sentiment for each feedback randomly.<br>
                As from the discussion forum minmum rows to shows was 11, I showed 100 feedbacks in the table.
                <br>
                <br>
            </li>            
            <li>
                When a file is selected in the Upload Ui the selected file greys out. But if I select another file then it removes the grey highlight of previously selected file and changes the highlight of the newly selected file to grey color.<br>
                Then when the train button is selected after a file has been selected in the upload ui, the selected file gets updated in the "Trained UI" and greys out.<br>
                Then when the user select another file in the upload ui and clicks train button the new selected file gets updated in the "Trained UI" and greys out, while previously greyed out file in the "Trained Ui" gets it grey highlight removed.<br>
                Each time a train button is selected, using the selected file in the upload ui Sample Data Table gets updated using ajax.<br>
                Just to keep in mind if the user selects a file thats already been pushed to "Trained UI" then none of the files in the "Trained UI" gets greyed out, although the updating of the Sample Data Table still continues respectively.<br>                
                For Q2(c) as mentioned in the discussion group when the train button is clicked the Sample Data Table is refreshed according to the data of the file selected in upload ui
                and the Sentiment status ,as discussed in the forum, gets randomly assigned either 'Positive' or 'Negative' to each feedback.
                <br>
                <br>
            </li>
            <li>
                For Q2(e) my sub-routine is found in "analysisWithPandas.py" file named "computeSentiment(array)".<br> I used regx keyword searching to conduct Sentimental Analysis for each feedback, which is retrieved from the feedbacks relationship found in an instance of the DataSource model.
            </li>
        </ul>
    </div>    
    <br>
    <br>
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
