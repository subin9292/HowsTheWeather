document.addEventListener("DOMContentLoaded", () => {
    const weatherApiKey = 'a71cf8f55278a20a0840a3e6fcba9384'; // OpenWeatherMap API 키
    const cityId = 1835848; // 서울의 도시 ID

    // OpenWeatherMap API 호출 - 현재 날씨
    fetch(`http://api.openweathermap.org/data/2.5/weather?id=${cityId}&appid=${weatherApiKey}&units=metric`)
        .then(response => response.json())
        .then(data => {
            const minTemp = data.main.temp_min.toFixed(1); // 최저 온도
            const maxTemp = data.main.temp_max.toFixed(1); // 최고 온도
            const currentTemp = data.main.temp.toFixed(1); // 현재 온도
            const weatherIcon = data.weather[0].icon;
            const now = new Date();
            const formattedDate = `${now.getFullYear()}/${now.getMonth() + 1}/${now.getDate()} ${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}`;

            // HTML 요소 업데이트
            document.querySelector('.low-temp').textContent = `${minTemp}°C`;
            document.querySelector('.high-temp').textContent = `${maxTemp}°C`;
            document.getElementById('current-temp').textContent = `${currentTemp}°C`;
            document.querySelector('.weather-icon').innerHTML = `<img src="https://openweathermap.org/img/wn/${weatherIcon}@2x.png" alt="Weather icon">`;
            document.getElementById('current-date').textContent = formattedDate;
        })
        .catch(error => console.error('Error fetching weather data:', error));

    // OpenWeatherMap API 호출 - 주간 예보
    fetch(`https://api.openweathermap.org/data/2.5/forecast/daily?id=${cityId}&cnt=7&appid=${weatherApiKey}&units=metric`)
        .then(response => response.json())
        .then(data => {
            const weeklyForecast = document.getElementById('weekly-forecast');
            weeklyForecast.innerHTML = ''; // 기존 내용 삭제

            data.list.forEach(day => {
                const date = new Date(day.dt * 1000);
                const dayOfWeek = `${date.getMonth() + 1}/${date.getDate()} (${['일', '월', '화', '수', '목', '금', '토'][date.getDay()]})`;
                const temp = day.temp.day.toFixed(1);
                const weatherDescription = translateWeatherDescription(day.weather[0].description);
                const weatherIcon = day.weather[0].icon;

                const listItem = document.createElement('li');
                listItem.innerHTML = `${dayOfWeek}: ${temp}°C, ${weatherDescription} <img src="https://openweathermap.org/img/wn/${weatherIcon}.png" alt="Weather icon">`;
                weeklyForecast.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error fetching weekly forecast:', error));

    // 댓글 기능
    const commentForm = document.getElementById('comment-form');
    commentForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(commentForm);
        fetch('/comments/', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('Failed to submit comment');
            }
        })
        .then(() => {
            window.location.reload();
        })
        .catch(error => console.error('Error submitting comment:', error));
    });
});

function translateWeatherDescription(description) {
    const descriptions = {
        "clear sky": "맑음",
        "few clouds": "구름 조금",
        "scattered clouds": "구름 낌",
        "broken clouds": "구름 많음",
        "shower rain": "소나기",
        "rain": "비",
        "thunderstorm": "천둥번개",
        "snow": "눈",
        "mist": "안개",
        "light rain": "약한 비",
        "moderate rain": "보통 비",
        "heavy intensity rain": "강한 비",
        "overcast clouds": "흐림"
    };
    return descriptions[description] || description;
}