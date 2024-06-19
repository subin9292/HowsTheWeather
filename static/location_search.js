// 지역검색에서 지역을 선택하여도 선택한 지역의 정보 화면으로 넘어가지지 않는 상황은 개선해야할 부분임
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById('location-search');
    const searchResults = document.getElementById('search-results');

    searchInput.addEventListener('input', async () => {
        const query = searchInput.value.toLowerCase();
        searchResults.innerHTML = '';
        if (query) {
            const response = await fetch(`/search?query=${query}`);
            const data = await response.json();
            const filteredLocations = data.places;
            filteredLocations.forEach(location => {
                const li = document.createElement('li');
                li.textContent = location;
                searchResults.appendChild(li);
            });
        }
    });

    searchResults.addEventListener('click', async (event) => {
        if (event.target.tagName === 'LI') {
            const placeName = event.target.textContent;
            const response = await fetch(`/coordinates?place=${placeName}`);
            const data = await response.json();
            if (data.coordinates) {
                const coordinates = data.coordinates;
                const lat = coordinates.lat;
                const lon = coordinates.lon;
                window.location.href = `/main.html?lat=${lat}&lon=${lon}&place=${encodeURIComponent(placeName)}`;
            }
        }
    });
});
