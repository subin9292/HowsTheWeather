document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    const cities = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "수원", "고양", "성남", "청주", "용인", "창원", "천안", "안산", "전주", "안양", "김해", "평택", "포항"];

    searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase();
        searchResults.innerHTML = '';
        if (query) {
            const filteredCities = cities.filter(city => city.toLowerCase().includes(query));
            filteredCities.forEach(city => {
                const li = document.createElement('li');
                li.textContent = city;
                li.addEventListener('click', () => {
                    alert(`You selected ${city}`);
                });
                searchResults.appendChild(li);
            });
        }
    });
});
