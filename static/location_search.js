document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById('location-search');
    const searchResults = document.getElementById('search-results');

    const locations = [
        "서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"
    ];

    searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase();
        searchResults.innerHTML = '';
        if (query) {
            const filteredLocations = locations.filter(location => location.toLowerCase().includes(query));
            filteredLocations.forEach(location => {
                const li = document.createElement('li');
                li.textContent = location;
                searchResults.appendChild(li);
            });
        }
    });

    searchResults.addEventListener('click', (event) => {
        if (event.target.tagName === 'LI') {
            searchInput.value = event.target.textContent;
            searchResults.innerHTML = '';
        }
    });
});