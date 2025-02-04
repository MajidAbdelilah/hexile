$(document).ready(function() {
    // Get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Set up AJAX to include CSRF token in headers
    $.ajaxSetup({
        xhrFields: {
            withCredentials: true
        },
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        statusCode: {
            401: function() {
                window.location.href = '/accounts/login/?next=' + window.location.pathname;
            },
            403: function() {
                window.location.href = '/accounts/login/?next=' + window.location.pathname;
            }
        }
    });

    // Validate form input before submitting
    $('#rent-form').on('submit', function(event) {
        event.preventDefault();
        const instanceName = $('#instance-name').val().trim();
        if (instanceName.length === 0) {
            alert('Please enter an instance name.');
            return;
        }
        const formData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: 'http://localhost:8000/api/rent-ghost/',
            data: formData,
            dataType: 'json',
            success: function(response) {
                alert('Ghost instance rented successfully!');
                // Show payment section with instance details
                $('#payment').show();
                $('#instance-id').val(response.instance_id);
                $('#amount').val(response.amount || '20.00'); // Default amount or from response
            },
            error: function(error) {
                alert('Error renting Ghost instance: ' + error.responseText);
            }
        });
    });

    // Remove duplicate PayPal buttons initialization.
    // PayPal buttons are now initialized inline in index.html.
});