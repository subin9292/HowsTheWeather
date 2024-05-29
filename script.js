document.addEventListener("DOMContentLoaded", () => {
    // 예시 API 데이터를 가져오는 함수
    const fetchWeatherData = async () => {
        // 현재 날씨 데이터 가져오기 (실제 API 엔드포인트로 변경 필요)
        const weatherResponse = await fetch('https://api.example.com/weather/current');
        const weatherData = await weatherResponse.json();

        // 날씨 데이터 업데이트
        document.getElementById('current-temp').textContent = `${weatherData.temperature}°C`;
        document.querySelector('.low-temp').textContent = `${weatherData.lowTemp}°C`;
        document.querySelector('.high-temp').textContent = `${weatherData.highTemp}°C`;
    };

    const fetchWeeklyForecast = async () => {
        // 주간 예보 데이터 가져오기 (실제 API 엔드포인트로 변경 필요)
        const weeklyResponse = await fetch('https://api.example.com/weather/weekly');
        const weeklyData = await weeklyResponse.json();

        // 주간 예보 데이터 업데이트
        const weeklyForecast = document.getElementById('weekly-forecast');
        weeklyForecast.innerHTML = ''; // 기존 데이터 초기화
        weeklyData.forEach(day => {
            const listItem = document.createElement('li');
            listItem.textContent = `${day.day} ${day.temperature}°C`;
            weeklyForecast.appendChild(listItem);
        });
    };

    const fetchHourlyForecast = async () => {
        // 시간별 예보 데이터 가져오기 (실제 API 엔드포인트로 변경 필요)
        const hourlyResponse = await fetch('https://api.example.com/weather/hourly');
        const hourlyData = await hourlyResponse.json();

        // 시간별 예보 데이터 업데이트
        const hourlyForecast = document.getElementById('hourly-forecast');
        hourlyForecast.innerHTML = ''; // 기존 데이터 초기화
        hourlyData.forEach(hour => {
            const listItem = document.createElement('li');
            listItem.textContent = `${hour.time} ${hour.temperature}°C`;
            hourlyForecast.appendChild(listItem);
        });
    };

    const fetchLiveComments = async () => {
        // 실시간 댓글 데이터 가져오기 (실제 API 엔드포인트로 변경 필요)
        const commentsResponse = await fetch('https://api.example.com/comments/live');
        const commentsData = await commentsResponse.json();

        // 댓글 데이터 업데이트
        const commentsList = document.getElementById('comments-list');
        commentsList.innerHTML = ''; // 기존 댓글 초기화
        commentsData.forEach(comment => {
            const listItem = document.createElement('li');
            listItem.textContent = comment.text;
            commentsList.appendChild(listItem);
        });
    };

    // 데이터 가져오기 호출
    fetchWeatherData();
    fetchWeeklyForecast();
    fetchHourlyForecast();
    fetchLiveComments();
});
