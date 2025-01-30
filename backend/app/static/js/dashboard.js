$(document).ready(function() {
    $('.delete-instance').on('click', function() {
        const instanceId = $(this).data('id');
        if (confirm('Are you sure you want to delete this instance?')) {
            $.ajax({
                url: `/api/delete-instance/${instanceId}/`,
                type: 'POST',
                success: function(response) {
                    alert('Instance deleted successfully');
                    location.reload();
                },
                error: function(error) {
                    alert('Error deleting instance: ' + error.responseText);
                }
            });
        }
    });
});
