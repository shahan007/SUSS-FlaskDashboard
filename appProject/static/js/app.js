let selectDropDown = ['bank', 'percentDataset', 'period'];
// Area to update upon click
let updateArray = ['chosenBank', 'chosenPercent', 'chosenPeriod'];
// store call back functions to event listener so it can be later removed
let ids = [];

function addingEventToDropDown(filename=''){
    selectDropDown.forEach(function (option, i) {
        let updateArea = document.getElementById(updateArray[i]);
        function selectListner() {
            updateArea.textContent = this.value;
            updateChart(filename);            
        }
        ids.push(selectListner)
        document.getElementById(option).addEventListener('click', selectListner);
    });

}
function removeEventFromDropDown() {
    selectDropDown.forEach(function (option, i) {
        document.getElementById(option).removeEventListener('click', ids[i]);
    });
}

addingEventToDropDown();

function getChart(data) {
    let dataLabel = data['banks'];
    
    let dataValues = data['complaints'];
    // Data to pass in to Chart object
    let chartData = {
        labels: dataLabel,
        datasets: [{
            label: '# of Complaints',
            data: dataValues,
            backgroundColor: 'rgba(255, 99, 132, 0.6)',
            borderWidth: 1,
            hoverBorderWidth: 3,
            hoverBorderColor: 'rgba(190, 121, 233,0.85)'

        }]
    }
    let optionData = {
        scales: {
            xAxes: [{
                ticks: {
                    beginAtZero: true                    
                }
            }]
        }
    }
    // Charting
    let canvas = document.getElementById('myChart').getContext('2d');
    Chart.defaults.global.defaultFontFamily = 'Roboto';
    var myChart = new Chart(canvas, {
        type: 'horizontalBar',
        data: chartData,
        options: optionData
    })
}

// Updates the chart when drop down menu is clicked
function updateChart(filename='') {
    let selectedBank = document.getElementById('chosenBank');
    let selectedPercent = document.getElementById('chosenPercent');
    let selectedPeriod = document.getElementById('chosenPeriod');
    $.ajax({
        method: 'POST',
        url: '/charting',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({
            selectedPercent: selectedPercent.textContent,
            selectedBank: selectedBank.textContent,
            selectedPeriod: selectedPeriod.textContent,
            filename : filename
        })
    }).done(res => {
        $('#myChart').remove();
        $('#chartContainer').append('<canvas id="myChart"></canvas>');
        getChart(res);
    })
}

updateChart();

function updateLatestData(filename='') {

    // Removing All the options for bank and period tags
    $('#bank').empty();
    $('#period').empty();
    // setting all the chosen tags to be null
    updateArray.forEach(x => {
        $(`#${x}`).text('');
    })
    // make call to route to give me back latest file drop downs
    $.ajax({
        url: '/getLatestDropDown?filename='+ filename ,
        method: 'GET',
        dataType: 'json'
    }).done(res => {
        let bankArray = res.banks;
        let periodArray = res.periods;
        bankArray.forEach(bank => {
            $('#bank').append(`<option value="${bank}">${bank}</option>`);
        });
        periodArray.forEach(period => {
            $('#period').append(`<option value="${period}">${period}</option>`);
        });
        updateChart(filename);
    }).fail(error => {
        console.log(error);
    })
}

function updateFiles() {
    $.ajax({
        url: '/listFiles',
        method: 'GET',
        dataType: 'json'
    }).done(res => {
        $('#listFiles').children().remove();
        res.forEach(x => {
            let p = document.createElement('p');
            p.className = 'filename'
            p.textContent = x;
            p.addEventListener('click',function(){  
                $('#listFiles > p').css({ 'background-color': 'white', 'color': 'rgb(90, 89, 89)'});                
                $(this).css({'background-color': 'grey','color':'white'});
                removeEventFromDropDown();                
                updateLatestData(this.textContent);                                
                ids=[];                
                addingEventToDropDown(this.textContent);                
            })                        
            $('#listFiles').append(p);
            $('#listFiles').append('<hr>');
        });
    }).fail(error => {
        console.log(error);
    });
}

updateFiles();

$('#customFileUpload').on('click', function () {
    $('#uploadFile').click()
});

$('#uploadFile').on("change", function () {
    if ($(this).val()) {
        let files = document.getElementById('uploadFile').files;
        if (files.length > 1) {
            $('#customText').html(`${files.length} files chosen`);
        }
        else {
            $('#customText').html(files[0].name);
        }                
    } else {
        $('#customText').html("No file chosen, yet.");
    }
});

$('#upload').on('click', function () {
    $('#msg').html('');
    var form_data = new FormData();
    var ins = document.getElementById('uploadFile').files.length;

    if (ins == 0) {
        $('#msg').html('<span style="color:red">Select at least one file</span>');
        return;
    }
    for (var x = 0; x < ins; x++) {
        form_data.append("files[]", document.getElementById('uploadFile').files[x]);
    }

    $.ajax({
        url: '/uploadFile', 
        dataType: 'json', 
        cache: false,
        contentType: false,
        processData: false,
        data: form_data,
        type: 'POST',
    }).done(function (response) {            
        $.each(response, function(key,data){
            if (key === 'message'){
                $('#msg').append(`<span class='green'>${data}</span>` + '<br/><br/>');
            }
        });                
        $.each(response, function (key, data) {
            if (key !== 'message') {
                $('#msg').append(`<span class='red'>${key}</span>` + ` -> <span class='grey'>${data}</span> ` + '<br/>');
            }
        });
        updateFiles();
        updateLatestData();
        removeEventFromDropDown();
        ids=[];
        addingEventToDropDown();
    }).fail(function (error) {        
        let msg = JSON.parse(error.responseText);
        $.each(msg, (k, d) => {
            $('#msg').append(`<span class='red'>${k}</span>` + ` -> <span class='grey'>${d}</span> ` + '<br><br>');
        });                    
    })    
});

// Responsible for charting of Word Cloud
function chartCloudData(){
    // Makes an ajax call to get the data for Word Cloud Chart
    $.ajax({
        url: '/chartCloudData',
        method: 'GET',
        dataType: 'json'
    }).done(res => {
        $('#chartCloudOrData').remove();
        let div = document.createElement('div');
        div.setAttribute('id', 'chartCloudOrData');
        $('#cloud_data_container').append(div);
        $('#chartCloudOrData').jQCloud(res);        
    }).fail(error => {        
        // Errror Handling        
        console.log(error.responseJSON);
        alert(`Ooops! Something went wrong when charting World Cloud\n<Error>StatusCode: ${error.status} StatusMessage${error.statusText}`);
    })
}

chartCloudData();

// add click listener to Word Cloud tab
$('#WordCloudBtn').on('click',function(){
    chartCloudData();
})

// Responsible for charting Sample Data Table
function chartSampleDataTable(){
    // Makes an ajax call to get the data for Sample Data Table
    $.ajax({
        url: '/chartSampleDataTable',
        method : 'GET',
        dataType:'json'
    }).done(res=>{
        $('#chartCloudOrData').remove();
        let div = document.createElement('div');        
        div.setAttribute('id', 'chartCloudOrData');
        div.style.display = 'table';            
        $('#cloud_data_container').append(div);
        let table = document.createElement('table');
        let thead = document.createElement('thead')
        let theadtr = document.createElement('tr');
        let theadth1 = document.createElement('th')
        let theadth2 = document.createElement('th')
        theadth1.textContent = 'Feedback';
        theadth2.textContent = 'Sentiment';        
        let tbody = document.createElement('tbody');
        $(div).append(table);  
        $(table).append(thead);   
        $(thead).append(theadtr);
        $(theadtr).append(theadth1);
        $(theadtr).append(theadth2);
        $(table).append(tbody)
        res.forEach(function (info) { 
            let tr = document.createElement('tr');
            let td1 = document.createElement('td');
            let td2 = document.createElement('td');            
            td1.textContent = info[0];
            td2.textContent = info[1];
            td2.style.fontWeight = 'bolder';
            if (info[1] == 'Negative'){
                td2.style.color ='Red';
            } else {
                td2.style.color = 'Green';
            }
            $(tbody).append(tr)
            $(tr).append(td1);
            $(tr).append(td2);
         });
    }).fail(error =>{        
        // Errror Handling
        console.log(error.responseJSON);
        alert(`Ooops! Something went wrong when creating Sample Data Table\n<Error>StatusCode: ${error.status} StatusMessage${error.statusText}`);        
    })
}

// add click listener to Sample Data tab
$('#SampleDataBtn').on('click',function(){
    chartSampleDataTable()
})

// add click listener to Train Button
// updates the ui.
// updates the sample data chart on the spot with the correct file.
$('#trainButton').on('click',function(){
    p_files = document.querySelectorAll('#listFiles > .filename');
    for (let i = 0 ; i<p_files.length;i++){
        let file = p_files[i];                
        if (file.style.backgroundColor == 'grey'){
            let trainDataFilesChildren = document.querySelectorAll('#listTrainedData > p')
            if (trainDataFilesChildren.length){    
                let have = false;            
                for (let i = 0; i < trainDataFilesChildren.length;i++){
                    let child = trainDataFilesChildren[i];
                    if (child.textContent == file.textContent){                        
                        child.nextSibling.remove();
                        child.remove();                        
                        $('#listTrainedData').append(`<p style='background-color:white;font-size: 13px;padding:1%;color:black;'>${file.textContent}</p>`);
                        $('#listTrainedData').append('<hr>');    
                        have = true;
                    } 
                }
                if (!have){
                    $('#listTrainedData').append(`<p style='background-color:grey;font-size: 13px;padding:1%;color:white;'>${file.textContent}</p>`);
                    $('#listTrainedData').append('<hr>');
                    $.ajax({
                        url: '/changeFileSelectedAfterTrain',
                        method: 'GET',
                        data: {
                            'fileSelected': file.textContent
                        }
                    }).done(res=>{
                        chartSampleDataTable();
                    });
                } else{
                    $.ajax({
                        url: '/changeFileSelectedAfterTrain',
                        method: 'GET',
                        data: {
                            'fileSelected': file.textContent
                        }
                    }).done(res => {
                        chartSampleDataTable();
                    });
                }  
            } else {
                $('#listTrainedData').append(`<p style='background-color:grey;font-size: 13px;padding:1%;color:white;'>${file.textContent}</p>`);
                $('#listTrainedData').append('<hr>');
                $.ajax({
                    url: '/changeFileSelectedAfterTrain',
                    method :'GET',
                    data : {
                        'fileSelected': file.textContent 
                    }
                }).done(res=>{
                    chartSampleDataTable();
                });
            }
        } else {
            let trainDataFilesChildren = document.querySelectorAll('#listTrainedData > p')
            if (trainDataFilesChildren.length) {                
                for (let i = 0; i < trainDataFilesChildren.length; i++) {
                    let child = trainDataFilesChildren[i];
                    if (child.textContent == file.textContent) {
                        child.nextSibling.remove();
                        child.remove();
                        $('#listTrainedData').append(`<p style='background-color:white;font-size: 13px;padding:1%;color:black;'>${file.textContent}</p>`);
                        $('#listTrainedData').append('<hr>');                        
                    }
                }
            }
        }
    }

})