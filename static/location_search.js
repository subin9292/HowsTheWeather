document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const searchResults = document.getElementById('search-results');

    const locations = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"];

    searchButton.addEventListener('click', () => {
        const query = searchInput.value.toLowerCase();
        const results = locations.filter(location => location.toLowerCase().includes(query));
        displayResults(results);
    });

    searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase();
        const results = locations.filter(location => location.toLowerCase().includes(query));
        displayResults(results);
    });

    function displayResults(results) {
        searchResults.innerHTML = '';
        results.forEach(result => {
            const li = document.createElement('li');
            li.textContent = result;
            searchResults.appendChild(li);
        });
    }
});
