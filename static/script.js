document.addEventListener("DOMContentLoaded", () => {
    const apiKey = "a71cf8f55278a20a0840a3e6fcba9384"; // 여기에 OpenWeatherMap API 키를 입력하세요.
    const cityId = 1835848; // 서울의 도시 ID

    // OpenWeatherMap API 호출
    fetch(`http://api.openweathermap.org/data/2.5/weather?id=${cityId}&appid=${apiKey}&units=metric`)
        .then(response => response.json())
        .then(data => {
            const minTemp = data.main.temp_min.toFixed(1); // 최저 온도
            const maxTemp = data.main.temp_max.toFixed(1); // 최고 온도
            const currentTemp = data.main.temp.toFixed(1); // 현재 온도
            const weatherIcon = data.weather[0].icon;
            const now = new Date();
            const currentDate = `${now.getFullYear()}/${now.getMonth() + 1}/${now.getDate()} ${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}`;

            // HTML 요소 업데이트
            document.getElementById('low-temp').textContent = `${minTemp}°C`;
            document.getElementById('high-temp').textContent = `${maxTemp}°C`;
            document.getElementById('current-temp').textContent = `현재 온도: ${currentTemp}°C`;
            document.getElementById('current-icon').innerHTML = `<img src="https://openweathermap.org/img/w/${weatherIcon}.png" alt="Weather icon">`;
            document.getElementById('current-date').textContent = currentDate;
        })
        .catch(error => console.error('Error fetching weather data:', error));

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
