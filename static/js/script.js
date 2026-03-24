$(document).ready(function() {
    // 1. Auto-hide flash messages after 4 seconds using jQuery fadeOut
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 4000);

    // 2. Client-side Form Validation
    $('#expenseForm').on('submit', function(event) {
        let isValid = true;

        // Reset previous validation states
        $('.form-control, .form-select').removeClass('is-invalid');

        // Validate Title
        const title = $('#title').val().trim();
        if (title === '') {
            $('#title').addClass('is-invalid');
            isValid = false;
        }

        // Validate Amount
        const amount = parseFloat($('#amount').val());
        if (isNaN(amount) || amount <= 0) {
            $('#amount').addClass('is-invalid');
            isValid = false;
        }

        // Validate Category
        const category = $('#category').val();
        if (category === '') {
            $('#category').addClass('is-invalid');
            isValid = false;
        }

        // Validate Date
        const date = $('#date').val();
        if (date === '') {
            $('#date').addClass('is-invalid');
            isValid = false;
        }

        // Prevent submission if invalid and show simple animation
        if (!isValid) {
            event.preventDefault();
            // Provide a small shake animation to the form as feedback
            $(this).addClass('shake');
            setTimeout(() => $(this).removeClass('shake'), 400);
        }
    });

    // 3. Pre-fill date with today's date if empty
    if ($('#date').length && !$('#date').val()) {
        const today = new Date().toISOString().split('T')[0];
        $('#date').val(today);
    }
});
