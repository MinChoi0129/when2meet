
import { GetUser } from "/static/js/getUser.js";

class Login {
    constructor() {
        this.getUser= new GetUser;

        this.login();
    }

    login() {
        const loginBtn = document.querySelector('.submit');
        loginBtn.addEventListener('click', async (event) => {
            event.preventDefault();
    
            const loginUsername = document.getElementById('userID').value;
            const loginPassword = document.getElementById('userPassword').value;

            console.log(loginUsername)
    
            try {
                const response = await fetch('http://127.0.0.1:8099/', {
              
                method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `grant_type=&username=${encodeURIComponent(loginUsername)}&password=${encodeURIComponent(loginPassword)}&scope=&client_id=&client_secret=`,
                });
                if (!response.ok) {
                    throw new Error('로그인 실패');
                }
                const data = await response.json();
                // Store the token or do something with the data
                document.cookie = `access_token=${data.access_token}; expires=${new Date(data.exp)}; path=/`;
                console.log("로그인 성공");
                // 리디렉션 처리
                window.location.href = "/" ;
                this.getUser.getCookie();

            } catch (error) {
                console.error('로그인 에러:', error);
            }
        });
    }
}

window.addEventListener('load', function() {
    new Login();
});
