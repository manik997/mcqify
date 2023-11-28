document.getElementById('input_type').addEventListener('change', function() {
    var value = this.value;
    var fileInput = document.getElementById('fileInput');
    var supportedFormats = document.getElementById('supportedFormats');

    fileInput.style.display = value === 'file' ? 'block' : 'none';
    supportedFormats.style.display = value === 'file' ? 'block' : 'none';
    document.getElementById('textInput').style.display = value === 'text' ? 'block' : 'none';
    document.getElementById('urlInput').style.display = value === 'url' ? 'block' : 'none';
    document.getElementById('youtube').style.display = value === 'youtube' ? 'block' : 'none';

});

document.getElementById('tryDifferentTopic').addEventListener('click', function() {
    window.location.reload(); // Refresh the page
});

document.getElementById('mcqForm').addEventListener('submit', function(e) {
    e.preventDefault();
    showLoading();
    var inputType = document.getElementById('input_type').value;
    if (inputType === 'file') {
        var fileInput = document.getElementById('fileInput');
        var file = fileInput.files[0];
        if (file) {
            var allowedExtensions = /(\.jpeg|\.txt|\.pdf|\.docx|\.csv|\.html|\.mp3)$/i;
            if (!allowedExtensions.exec(file.name)) {
                hideLoading();
                alert('File type not supported');
                e.preventDefault(); 
                return;
            }
        }
    }

    var formData = new FormData(this);
    fetch('/generate_mcqs', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (!response.ok) {
            throw new Error('Server error');
        }
        return response.json();
    }).then(data => {
        hideLoading();
        displayMCQs(data);
    }).catch(error => {
        hideLoading();
        displayError('Something went wrong, please try again.');
        console.error('Error:', error);
    });
});

function showLoading() {
    document.getElementById('loader').style.display = 'block';
    
}

function hideLoading() {
    document.getElementById('loader').style.display = 'none';
    
}

function displayMCQs(mcqs) {
    var display = document.getElementById('mcqDisplay');
    display.innerHTML = ''; 

    mcqs.forEach((mcq, index) => {
        var qnum = 1
        var questionNumber = index + 1; 
        var mcqElement = document.createElement('div');
        mcqElement.className = 'mcq';
        mcqElement.innerHTML = `
            <h3>Question ${questionNumber}</h3>
            <p>${mcq[`Question${questionNumber}`]}</p>
            <ul>
                <li>A: ${mcq['A']}</li>
                <li>B: ${mcq['B']}</li>
                <li>C: ${mcq['C']}</li>
                <li>D: ${mcq['D']}</li>
            </ul>
            <p><b>Answer:</b> ${mcq['Answer']}</p>
        `;
        display.appendChild(mcqElement);
    });
    showTryDifferentTopicButton();
}

function displayError(message) {
    var errorDiv = document.getElementById('errorMessage');
    errorDiv.innerHTML = message; // Set the error message
    errorDiv.style.display = 'block'; // Show the error message div

    showTryDifferentTopicButton();
}

function showTryDifferentTopicButton() {
    var tryDifferentButton = document.getElementById('tryDifferentTopic');
    tryDifferentButton.style.display = 'block';
}

document.getElementById('tryDifferentTopic').addEventListener('click', function() {
    window.location.reload(); // Refresh the page
});

