document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('filter-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission
        
        // Get filter criteria
        const minArea = document.getElementById('min_area').value.trim();
        const maxArea = document.getElementById('max_area').value.trim();
        const minRooms = document.getElementById('min_rooms').value.trim();
        const maxRooms = document.getElementById('max_rooms').value.trim();
        const floor = document.getElementById('floor').value.trim();
        const market = document.getElementById('market').value.trim();

        // Filter results
        const results = document.querySelectorAll('.box');
        results.forEach(function(result) {
            const area = result.querySelector('.area').textContent.trim();
            const rooms = result.querySelector('.rooms').textContent.trim();
            const floorValue = result.querySelector('.floor').textContent.trim();
            const marketValue = result.querySelector('.market').textContent.trim();

            // Check if result meets filter criteria
            const meetsCriteria = (
                (minArea === '' || parseFloat(area) >= parseFloat(minArea)) &&
                (maxArea === '' || parseFloat(area) <= parseFloat(maxArea)) &&
                (minRooms === '' || parseInt(rooms) >= parseInt(minRooms)) &&
                (maxRooms === '' || parseInt(rooms) <= parseInt(maxRooms)) &&
                (floor === '' || floorValue === floor) &&
                (market === '' || marketValue === market)
            );

            // Show/hide result based on filter criteria
            if (meetsCriteria) {
                result.style.display = 'block';
            } else {
                result.style.display = 'none';
            }
        });
    });
});
